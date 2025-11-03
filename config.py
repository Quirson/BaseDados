"""
CONFIGURAÇÕES GLOBAIS - CORES E ESTILOS UNIFICADOS
Centraliza todas as configurações do aplicativo
"""

import logging

# =============================================================================
# CORES E ESTILOS
# =============================================================================

COLORS = {
    # Cores principais
    'primary': '#1a237e',
    'primary_light': '#534bae',
    'primary_dark': '#000051',
    'secondary': '#d32f2f',
    'secondary_light': '#ff6659',
    'secondary_dark': '#9a0007',

    # Cores de apoio
    'accent': '#2979ff',
    'success': '#00c853',
    'warning': '#ffab00',
    'danger': '#ff1744',
    'info': '#00b8d4',

    # Cores de fundo
    'dark_bg': '#0d1117',
    'dark_surface': '#161b22',
    'dark_card': '#21262d',
    'dark_border': '#30363d',

    # Cores de texto
    'text_primary': '#f0f6fc',
    'text_secondary': '#8b949e',
    'text_disabled': '#484f58',

# 🆕 ADICIONE ESTAS NOVAS CORES:
    'dark_hover': '#4A4A4A',
}

FONTS = {
    'title': ('Arial', 20, 'bold'),
    'subtitle': ('Arial', 16, 'bold'),
    'normal': ('Arial', 12),
    'small': ('Arial', 10)
}

# =============================================================================
# CONFIGURAÇÕES DE LOGGING
# =============================================================================

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO
LOG_FILE = 'logs/app.log'


def setup_logging():
    """Configura o sistema de logging"""
    import os
    os.makedirs('logs', exist_ok=True)

    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


# =============================================================================
# CONFIGURAÇÕES DE BASE DE DADOS
# =============================================================================

DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service': 'XEPDB1',
    'user': 'Gestao_Publicidade',
    'password': 'ISCTEM',
    'timeout': 30  # Added timeout to prevent hanging connections
}

# =============================================================================
# CONFIGURAÇÕES DE INTERFACE
# =============================================================================

WINDOW_CONFIG = {
    'width': 1200,
    'height': 700,
    'min_width': 1100,
    'min_height': 650,
    'title': 'INC Publicidade - Sistema de Gestão'
}

# Estados de validação
VALIDATION_STATES = {
    'valid': 'success',
    'invalid': 'danger',
    'warning': 'warning',
    'neutral': 'info'
}
