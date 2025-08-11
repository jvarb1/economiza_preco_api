import os

# Configurações da API
APP_TOKEN = os.getenv('SEFAZ_TOKEN')  # Remove o fallback - deve estar no .env
API_URL = "http://api.sefaz.al.gov.br/sfz-economiza-alagoas-api/api/public/produto/pesquisa"

# Configurações de consulta
DIAS_PESQUISA = int(os.getenv('DIAS_PESQUISA', '10'))
TIMEOUT = int(os.getenv('TIMEOUT', '30'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# Códigos IBGE dos municípios de Alagoas
CODIGOS_IBGE_AL = [
    2700300,
]

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')