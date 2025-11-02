"""
MÓDULO CENTRALIZADO DE VALIDAÇÃO - REGRAS DE NEGÓCIO SÓLIDAS
Todas as validações de dados passam por aqui antes de inserir na BD
"""

import re
from datetime import datetime
from logger_config import app_logger


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass


class CRUDValidator:
    """Validador centralizado para todos os CRUDs"""

    # Padrões regex
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^(\+258|0)[1-9]\d{7,8}$'
    FISCAL_PATTERN = r'^\d{12}$'

    @staticmethod
    def validate_anunciante(data):
        """Valida dados de anunciante"""
        errors = []

        # Nome/Razão Social
        nome = data.get('nome', '').strip()
        if not nome or len(nome) < 3:
            errors.append("Nome deve ter pelo menos 3 caracteres")
        if len(nome) > 200:
            errors.append("Nome não pode exceder 200 caracteres")

        # Número de identificação fiscal
        fiscal = data.get('fiscal', '').strip()
        if not fiscal or not re.match(CRUDValidator.FISCAL_PATTERN, fiscal):
            errors.append("NIF deve conter 12 dígitos numéricos")

        # Categoria de negócio
        categoria = data.get('categoria', '').strip()
        categorias_validas = ['Tecnologia', 'Varejo', 'Alimentação', 'Saúde', 'Educação', 'Outro']
        if not categoria or categoria not in categorias_validas:
            errors.append(f"Categoria inválida. Válidas: {', '.join(categorias_validas)}")

        # Email
        email = data.get('email', '').strip()
        if email and not re.match(CRUDValidator.EMAIL_PATTERN, email):
            errors.append("Email inválido")

        # Telefone
        telefone = data.get('telefone', '').strip()
        if telefone and not re.match(CRUDValidator.PHONE_PATTERN, telefone):
            errors.append("Telefone inválido (formato: +258... ou 0...)")

        # Limite de crédito
        try:
            limite = float(data.get('limite', 0))
            if limite < 0:
                errors.append("Limite de crédito não pode ser negativo")
            if limite > 10000000:
                errors.append("Limite de crédito excede o máximo permitido")
        except:
            errors.append("Limite de crédito deve ser numérico")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_campanha(data):
        """Valida dados de campanha"""
        errors = []

        # Título
        titulo = data.get('titulo', '').strip()
        if not titulo or len(titulo) < 3:
            errors.append("Título deve ter pelo menos 3 caracteres")
        if len(titulo) > 150:
            errors.append("Título não pode exceder 150 caracteres")

        # Objetivo
        objectivo = data.get('objectivo', '').strip()
        if not objectivo or len(objectivo) < 10:
            errors.append("Objetivo deve ter pelo menos 10 caracteres")

        # Público-alvo
        pub_alvo = data.get('pub_alvo', '').strip()
        if not pub_alvo or len(pub_alvo) < 5:
            errors.append("Público-alvo deve ter pelo menos 5 caracteres")

        # Orçamento
        try:
            orc = float(data.get('orc_alocado', 0))
            if orc <= 0:
                errors.append("Orçamento deve ser maior que zero")
            if orc > 100000000:
                errors.append("Orçamento excede o máximo permitido")
        except:
            errors.append("Orçamento deve ser numérico")

        # Datas
        try:
            data_inicio = datetime.strptime(data.get('data_inicio', ''), '%d/%m/%Y')
            data_termino = datetime.strptime(data.get('data_termino', ''), '%d/%m/%Y')

            if data_termino <= data_inicio:
                errors.append("Data de término deve ser posterior à data de início")

            if (data_termino - data_inicio).days > 365:
                errors.append("Campanha não pode durar mais de 365 dias")
        except:
            errors.append("Datas inválidas. Use formato DD/MM/YYYY")

        # Anunciante
        if not data.get('anunciante'):
            errors.append("Selecione um anunciante")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_espaco(data):
        """Valida dados de espaço"""
        errors = []

        # Localização
        local = data.get('local', '').strip()
        if not local or len(local) < 3:
            errors.append("Localização deve ter pelo menos 3 caracteres")

        # Tipo
        tipo = data.get('tipo', '').strip()
        tipos_validos = ['Billboard', 'Painel Digital', 'Rádio', 'TV', 'Jornal', 'Online']
        if not tipo or tipo not in tipos_validos:
            errors.append(f"Tipo inválido. Válidos: {', '.join(tipos_validos)}")

        # Dimensões
        dimensoes = data.get('dimensoes', '').strip()
        if not dimensoes or len(dimensoes) < 2:
            errors.append("Dimensões inválidas")

        # Preço base
        try:
            preco = float(data.get('preco', 0))
            if preco <= 0:
                errors.append("Preço deve ser maior que zero")
            if preco > 500000:
                errors.append("Preço excede o máximo permitido")
        except:
            errors.append("Preço deve ser numérico")

        # Disponibilidade
        disponibilidade = data.get('disponibilidade', '')
        valores_validos = ['Disponível', 'Ocupado', 'Manutenção', 'Sempre Disponível']
        if not disponibilidade or disponibilidade not in valores_validos:
            errors.append(f"Disponibilidade inválida. Válidas: {', '.join(valores_validos)}")

        # Proprietário
        proprietario = data.get('proprietario', '').strip()
        if not proprietario or len(proprietario) < 3:
            errors.append("Proprietário deve ter pelo menos 3 caracteres")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_peca(data):
        """Valida dados de peça criativa"""
        errors = []

        # Título
        titulo = data.get('titulo', '').strip()
        if not titulo or len(titulo) < 3:
            errors.append("Título deve ter pelo menos 3 caracteres")

        # Descrição
        descricao = data.get('descricao', '').strip()
        if not descricao or len(descricao) < 10:
            errors.append("Descrição deve ter pelo menos 10 caracteres")

        # Tipo
        tipo = data.get('tipo', '').strip()
        tipos_validos = ['Anúncio', 'Banner', 'Spot', 'Cartaz', 'Outro']
        if not tipo or tipo not in tipos_validos:
            errors.append(f"Tipo inválido. Válidos: {', '.join(tipos_validos)}")

        # Formato
        formato = data.get('formato', '').strip()
        if not formato or len(formato) < 2:
            errors.append("Formato inválido")

        # Campanha
        if not data.get('campanha'):
            errors.append("Selecione uma campanha")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_pagamento(data):
        """Valida dados de pagamento"""
        errors = []

        # Valor
        try:
            valor = float(data.get('valor', 0))
            if valor <= 0:
                errors.append("Valor deve ser maior que zero")
            if valor > 10000000:
                errors.append("Valor excede o máximo permitido")
        except:
            errors.append("Valor deve ser numérico")

        # Método
        metodo = data.get('metodo', '').strip()
        metodos_validos = ['Transferência', 'Cheque', 'Dinheiro', 'Cartão']
        if not metodo or metodo not in metodos_validos:
            errors.append(f"Método inválido. Válidos: {', '.join(metodos_validos)}")

        # Status
        status = data.get('status', '').strip()
        status_validos = ['Pendente', 'Confirmado', 'Cancelado']
        if not status or status not in status_validos:
            errors.append(f"Status inválido. Válidos: {', '.join(status_validos)}")

        # Campanha
        if not data.get('campanha'):
            errors.append("Selecione uma campanha")

        # Data
        try:
            datetime.strptime(data.get('data_pagamento', ''), '%d/%m/%Y')
        except:
            errors.append("Data inválida. Use formato DD/MM/YYYY")

        if errors:
            raise ValidationError("\n".join(errors))

        return True
