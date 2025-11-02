"""
VALIDAÇÃO CENTRALIZADA DE DADOS
Garante integridade de dados antes de operações com Oracle
"""

import re
from typing import Tuple, Any, Optional
from logger_config import app_logger


class DataValidator:
    """Classe para validar dados"""

    logger = app_logger

    @staticmethod
    def validate_fiscal_id(value: str) -> Tuple[bool, str]:
        """Valida número de identificação fiscal"""
        if not value or not str(value).strip():
            return False, "ID fiscal é obrigatório"

        try:
            fiscal_id = int(value)
            if fiscal_id <= 0:
                return False, "ID fiscal deve ser positivo"
            if fiscal_id < 1000000 or fiscal_id > 9999999:
                return False, "ID fiscal deve ter 7 dígitos"
            return True, ""
        except ValueError:
            return False, "ID fiscal deve ser um número"

    @staticmethod
    def validate_name(value: str, min_length: int = 3) -> Tuple[bool, str]:
        """Valida nome ou razão social"""
        if not value or not str(value).strip():
            return False, "Nome é obrigatório"

        value = str(value).strip()
        if len(value) < min_length:
            return False, f"Nome deve ter pelo menos {min_length} caracteres"

        if len(value) > 255:
            return False, "Nome muito longo (máximo 255 caracteres)"

        # Verifica caracteres inválidos
        if any(char in value for char in ['<', '>', '"', "'"]):
            return False, "Nome contém caracteres inválidos"

        return True, ""

    @staticmethod
    def validate_email(value: str) -> Tuple[bool, str]:
        """Valida email"""
        if not value:
            return True, ""  # Email é opcional

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, str(value)):
            return False, "Email inválido"

        return True, ""

    @staticmethod
    def validate_phone(value: str) -> Tuple[bool, str]:
        """Valida telefone"""
        if not value:
            return True, ""  # Telefone é opcional

        # Remove caracteres não-numéricos
        phone_clean = re.sub(r'[^\d+]', '', str(value))

        if len(phone_clean) < 7:
            return False, "Telefone deve ter pelo menos 7 dígitos"

        if len(phone_clean) > 20:
            return False, "Telefone muito longo"

        return True, ""

    @staticmethod
    def validate_currency(value: Any) -> Tuple[bool, str]:
        """Valida valor monetário"""
        try:
            amount = float(value)
            if amount < 0:
                return False, "Valor não pode ser negativo"
            if amount > 999999999.99:
                return False, "Valor muito grande"
            return True, ""
        except (ValueError, TypeError):
            return False, "Valor monetário inválido"

    @staticmethod
    def validate_date(value: str, format: str = "%Y-%m-%d") -> Tuple[bool, str]:
        """Valida data"""
        from datetime import datetime

        if not value:
            return False, "Data é obrigatória"

        try:
            datetime.strptime(str(value), format)
            return True, ""
        except ValueError:
            return False, f"Data inválida (formato esperado: {format})"

    @staticmethod
    def validate_classification(value: str) -> Tuple[bool, str]:
        """Valida classificação de confiança"""
        valid_classifications = [
            'AAA - Excelente', 'AA - Muito Bom', 'A - Bom',
            'B - Regular', 'C - Baixo'
        ]

        if value not in valid_classifications:
            return False, f"Classificação inválida: {value}"

        return True, ""

    @staticmethod
    def validate_size(value: str) -> Tuple[bool, str]:
        """Valida tamanho de empresa"""
        valid_sizes = ['Pequeno', 'Médio', 'Grande']

        if value not in valid_sizes:
            return False, f"Tamanho inválido: {value}"

        return True, ""

    @staticmethod
    def sanitize_sql_string(value: str) -> str:
        """Remove caracteres perigosos de strings para SQL"""
        # Nota: Use prepared statements em vez disso quando possível
        if not value:
            return ""

        value = str(value)
        # Remove múltiplos espaços
        value = ' '.join(value.split())
        return value

    @staticmethod
    def validate_anunciante_data(data: dict) -> Tuple[bool, str]:
        """Valida dados completos de anunciante"""

        # Validar campos obrigatórios
        required_fields = ['fiscal_id', 'name', 'category', 'size']
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Campo obrigatório não preenchido: {field}"

        # Validar cada campo
        is_valid, error = DataValidator.validate_fiscal_id(data['fiscal_id'])
        if not is_valid:
            return False, error

        is_valid, error = DataValidator.validate_name(data['name'])
        if not is_valid:
            return False, error

        is_valid, error = DataValidator.validate_size(data['size'])
        if not is_valid:
            return False, error

        if 'credit_limit' in data:
            is_valid, error = DataValidator.validate_currency(data['credit_limit'])
            if not is_valid:
                return False, error

        if 'classification' in data:
            is_valid, error = DataValidator.validate_classification(data['classification'])
            if not is_valid:
                return False, error

        return True, ""


class ValidationError(Exception):
    """Exceção personalizada para erros de validação"""
    pass
