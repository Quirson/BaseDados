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
    """Validador centralizado para todos os CRUDS"""

    # Padrões regex
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^(\+258|0)[1-9]\d{7,8}$'
    FISCAL_PATTERN = r'^\d{9,12}$'  # 🆕 CORREÇÃO: 9-12 dígitos

    @staticmethod
    def validate_anunciante(data):
        """Valida dados de anunciante - VERSÃO CORRIGIDA"""
        errors = []

        # Nome/Razão Social
        nome = data.get('nome', '').strip()
        if not nome or len(nome) < 3:
            errors.append("Nome deve ter pelo menos 3 caracteres")
        if len(nome) > 200:
            errors.append("Nome não pode exceder 200 caracteres")

        # Número de identificação fiscal - 🆕 CORREÇÃO
        fiscal = data.get('fiscal', '').strip()
        if not fiscal or not fiscal.isdigit():
            errors.append("NIF deve conter apenas dígitos numéricos")
        elif len(fiscal) < 9 or len(fiscal) > 12:  # 🆕 CORREÇÃO: 9-12 dígitos
            errors.append("NIF deve ter entre 9 e 12 dígitos")

        # Categoria de negócio
        categoria = data.get('categoria', '').strip()
        categorias_validas = ['Telecomunicações', 'Varejo', 'Alimentação', 'Saúde', 'Educação', 'Tecnologia', 'Outro']
        if not categoria or categoria not in categorias_validas:
            errors.append(f"Categoria inválida. Válidas: {', '.join(categorias_validas)}")

        # Porte
        porte = data.get('porte', '').strip()
        if not porte:
            errors.append("Porte é obrigatório")

        # Endereço
        endereco = data.get('endereco', '').strip()
        if not endereco:
            errors.append("Endereço é obrigatório")

        # Contactos
        contactos = data.get('contactos', '').strip()
        if not contactos:
            errors.append("Contactos são obrigatórios")

        # Representante Legal
        rep_legal = data.get('rep_legal', '').strip()
        if not rep_legal:
            errors.append("Representante legal é obrigatório")

        # Limite de crédito
        try:
            limite = float(data.get('limite', 0))
            if limite < 0:
                errors.append("Limite de crédito não pode ser negativo")
            if limite > 10000000:
                errors.append("Limite de crédito excede o máximo permitido")
        except:
            errors.append("Limite de crédito deve ser numérico")

        # Classificação
        classif = data.get('classif', '').strip()
        classif_validas = ['Confidencial', 'Público', 'Interno']
        if not classif or classif not in classif_validas:
            errors.append(f"Classificação inválida. Válidas: {', '.join(classif_validas)}")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_campanha(data):
        """Valida dados de campanha - JÁ ESTÁ FUNCIONANDO, MANTIDO"""
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
        """Valida dados de espaço - VERSÃO CORRIGIDA"""
        errors = []

        # Localização
        local = data.get('local', '').strip()
        if not local or len(local) < 3:
            errors.append("Localização deve ter pelo menos 3 caracteres")

        # Tipo - 🆕 CORREÇÃO COM VALORES CORRETOS
        tipo = data.get('tipo', '').strip()
        tipos_validos = ['Painel Digital', 'Espaco em Aplicativo', 'Banner em Site']
        if not tipo or tipo not in tipos_validos:
            errors.append(f"Tipo inválido. Válidos: {', '.join(tipos_validos)}")

        # Dimensões
        dimensoes = data.get('dimensoes', '').strip()
        if not dimensoes or len(dimensoes) < 2:
            errors.append("Dimensões inválidas")

        # Preço base - 🆕 CORREÇÃO: campo correto 'preco_base'
        try:
            preco = float(data.get('preco_base', 0))
            if preco <= 0:
                errors.append("Preço deve ser maior que zero")
            if preco > 500000:
                errors.append("Preço excede o máximo permitido")
        except:
            errors.append("Preço deve ser numérico")

        # Visibilidade
        visibilidade = data.get('visibilidade', '').strip()
        if not visibilidade:
            errors.append("Visibilidade é obrigatória")

        # Disponibilidade
        disponibilidade = data.get('disponibilidade', '')
        valores_validos = ['Disponível', 'Indisponível', 'Em Manutenção']
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
        """Valida dados de peça criativa - VERSÃO CORRIGIDA E SIMPLIFICADA"""
        errors = []

        # Título
        titulo = data.get('titulo', '').strip()
        if not titulo or len(titulo) < 3:
            errors.append("Título deve ter pelo menos 3 caracteres")

        # Descrição
        descricao = data.get('descricao', '').strip()
        if not descricao or len(descricao) < 10:
            errors.append("Descrição deve ter pelo menos 10 caracteres")

        # Criador
        criador = data.get('criador', '').strip()
        if not criador:
            errors.append("Criador é obrigatório")

        # Status
        status = data.get('status', '').strip()
        status_validos = ['Pendente', 'Aprovado', 'Rejeitado', 'Em Revisão']
        if not status or status not in status_validos:
            errors.append(f"Status inválido. Válidos: {', '.join(status_validos)}")

        # Classificação
        try:
            classif = int(data.get('classif', 0))
            if classif < 0 or classif > 18:
                errors.append("Classificação deve ser entre 0 e 18")
        except:
            errors.append("Classificação deve ser numérica (0-18)")

        # 🆕 REMOVIDA VALIDAÇÃO DE CAMPOS QUE NÃO EXISTEM NO FORMULÁRIO
        # (tipo, formato, campanha)

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_pagamento(data):
        """Valida dados de pagamento - VERSÃO CORRIGIDA"""
        errors = []

        # Preço dinâmico - 🆕 CORREÇÃO: campo correto 'preco_dinam'
        try:
            valor = float(data.get('preco_dinam', 0))
            if valor <= 0:
                errors.append("Valor deve ser maior que zero")
            if valor > 10000000:
                errors.append("Valor excede o máximo permitido")
        except:
            errors.append("Valor deve ser numérico")

        # Método
        metodo = data.get('metodo', '').strip()
        metodos_validos = ['Transferência Bancária', 'Dinheiro', 'Cheque', 'Cartão de Crédito', 'Outra']
        if not metodo or metodo not in metodos_validos:
            errors.append(f"Método inválido. Válidos: {', '.join(metodos_validos)}")

        # Reconciliação
        reconc = data.get('reconc', '').strip()
        status_validos = ['Pendente', 'Conciliado', 'Não Conciliado', 'Em Revisão']
        if not reconc or reconc not in status_validos:
            errors.append(f"Reconciliação inválida. Válidas: {', '.join(status_validos)}")

        # 🆕 REMOVIDA VALIDAÇÃO DE CAMPANHA (não existe no formulário)

        if errors:
            raise ValidationError("\n".join(errors))

        return True