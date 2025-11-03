"""
MÓDULO CENTRALIZADO DE VALIDAÇÃO - REGRAS DE NEGÓCIO SÓLIDAS
VERSÃO CORRIGIDA - CAMPOS CORRETOS
"""

import re
from datetime import datetime
from logger_config import app_logger


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass


class CRUDValidator:
    """Validador centralizado para todos os CRUDs - VERSÃO CORRIGIDA"""

    @staticmethod
    def validate_anunciante(data):
        """Valida dados de anunciante - versão compatível com constraint Oracle"""
        errors = []

        # Nome/Razão Social
        nome = data.get('nome', '').strip()
        if not nome or len(nome) < 3:
            errors.append("Nome deve ter pelo menos 3 caracteres.")

        # Categoria de negócio
        categoria = data.get('categoria', '').strip()
        categorias_validas = [
            'Telecomunicações', 'Varejo', 'Alimentação',
            'Saúde', 'Educação', 'Tecnologia', 'Outro'
        ]
        if not categoria or categoria not in categorias_validas:
            errors.append(f"Categoria inválida. Valores válidos: {', '.join(categorias_validas)}.")

        # Porte da empresa
        porte = data.get('porte', '').strip()
        portes_validos = ['Pequeno', 'Médio', 'Grande']
        if not porte or porte not in portes_validos:
            errors.append(f"Porte inválido. Valores válidos: {', '.join(portes_validos)}.")

        # Endereço
        endereco = data.get('endereco', '').strip()
        if not endereco:
            errors.append("Endereço é obrigatório.")

        # Contactos
        contactos = data.get('contactos', '').strip()
        if not contactos:
            errors.append("Contactos são obrigatórios.")

        # Representante Legal
        rep_legal = data.get('rep_legal', '').strip()
        if not rep_legal:
            errors.append("Representante legal é obrigatório.")

        # Limite de crédito
        try:
            limite = float(data.get('limite', 0))
            if limite < 0:
                errors.append("Limite de crédito não pode ser negativo.")
        except:
            errors.append("Limite de crédito deve ser um número válido.")

        # Classificação confidencial (respeitando constraint Oracle)
        classif = data.get('classif', '').strip()
        classif_validas = [
            'AAA - Excelente',
            'AA - Muito Bom',
            'A - Bom',
            'B - Regular',
            'C - Baixo'
        ]
        if not classif or classif not in classif_validas:
            errors.append(f"Classificação inválida. Valores válidos: {', '.join(classif_validas)}.")

        # Preferência de comunicação
        pref_com = data.get('pref_com', '').strip()
        prefs_validas = ['Email', 'Telefone', 'SMS', 'Presencial']
        if not pref_com or pref_com not in prefs_validas:
            errors.append(f"Preferência de comunicação inválida. Valores válidos: {', '.join(prefs_validas)}.")

        # Resultado final
        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_campanha(data):
        """Valida dados de campanha - VERSÃO CORRIGIDA"""
        errors = []

        # Título
        titulo = data.get('titulo', '').strip()
        if not titulo or len(titulo) < 3:
            errors.append("Título deve ter pelo menos 3 caracteres")

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
        except:
            errors.append("Orçamento deve ser numérico")

        # Datas
        try:
            data_inicio = datetime.strptime(data.get('data_inicio', ''), '%d/%m/%Y')
            data_termino = datetime.strptime(data.get('data_termino', ''), '%d/%m/%Y')

            if data_termino <= data_inicio:
                errors.append("Data de término deve ser posterior à data de início")
        except:
            errors.append("Datas inválidas. Use formato DD/MM/YYYY")

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

        # Tipo - VALORES CORRETOS
        tipo = data.get('tipo', '').strip()
        tipos_validos = ['Painel Digital', 'Espaco em Aplicativo', 'Banner em Site']
        if not tipo or tipo not in tipos_validos:
            errors.append(f"Tipo inválido. Válidos: {', '.join(tipos_validos)}")

        # Dimensões
        dimensoes = data.get('dimensoes', '').strip()
        if not dimensoes:
            errors.append("Dimensões são obrigatórias")

        # Preço base - CAMPO CORRETO
        try:
            preco = float(data.get('preco_base', 0))
            if preco <= 0:
                errors.append("Preço deve ser maior que zero")
        except:
            errors.append("Preço deve ser numérico")

        # Visibilidade
        visibilidade = data.get('visibilidade', '').strip()
        if not visibilidade:
            errors.append("Visibilidade é obrigatória")

        # Disponibilidade - VALORES CORRETOS
        disponibilidade = data.get('disponibilidade', '')
        valores_validos = ['Disponível', 'Indisponível', 'Em Manutenção']
        if not disponibilidade or disponibilidade not in valores_validos:
            errors.append(f"Disponibilidade inválida. Válidas: {', '.join(valores_validos)}")

        # Proprietário
        proprietario = data.get('proprietario', '').strip()
        if not proprietario:
            errors.append("Proprietário é obrigatório")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_peca(data):
        """Valida dados de peça criativa - VERSÃO SIMPLIFICADA"""
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

        # Status - VALORES CORRETOS
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

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_pagamento(data):
        """Valida dados de pagamento - VERSÃO CORRIGIDA"""
        errors = []

        # Preço dinâmico - CAMPO CORRETO
        try:
            valor = float(data.get('preco_dinam', 0))
            if valor <= 0:
                errors.append("Valor deve ser maior que zero")
        except:
            errors.append("Valor deve ser numérico")

        # Método - VALORES CORRETOS
        metodo = data.get('metodo', '').strip()
        metodos_validos = ['Transferência Bancária', 'Dinheiro', 'Cheque', 'Cartão de Crédito', 'Outra']
        if not metodo or metodo not in metodos_validos:
            errors.append(f"Método inválido. Válidos: {', '.join(metodos_validos)}")

        # Reconciliação - VALORES CORRETOS
        reconc = data.get('reconc', '').strip()
        status_validos = ['Pendente', 'Conciliado', 'Não Conciliado', 'Em Revisão']
        if not reconc or reconc not in status_validos:
            errors.append(f"Reconciliação inválida. Válidas: {', '.join(status_validos)}")

        if errors:
            raise ValidationError("\n".join(errors))

        return True

    @staticmethod
    def validate_anunciante_sem_fiscal(data):
        """Valida dados de anunciante para CRIAÇÃO (sem NIF)"""
        return CRUDValidator.validate_anunciante(data)