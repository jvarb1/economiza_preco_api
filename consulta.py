import requests
import pandas as pd
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import *

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('consulta_precos.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def criar_sessao_com_retry():
    """Cria uma sessão HTTP com mecanismo de retry automático"""
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def validar_token():
    """Valida se o token da API está configurado"""
    if not APP_TOKEN:
        logger.error("❌ Token da API não configurado. Configure a variável SEFAZ_TOKEN no arquivo .env")
        return False
    return True

def consultar_preco(gtin, cod_ibge):
    """Consulta preço de um produto específico"""
    if not validar_token():
        logger.error("❌ Token da API não configurado")
        return []
    
    headers = {
        "AppToken": APP_TOKEN
    }
    body = {
        "produto": {
            "gtin": str(gtin)
        },
        "estabelecimento": {
            "municipio": {
                "codigoIBGE": int(cod_ibge)
            }
        },
        "dias": DIAS_PESQUISA
    }
    
    session = criar_sessao_com_retry()
    
    try:
        logger.debug(f"�� Consultando GTIN {gtin} para município {cod_ibge}")
        response = session.post(API_URL, headers=headers, json=body, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for item in data.get("conteudo", []):
            produto = item.get("produto", {})
            venda = produto.get("venda", {})
            estabelecimento = item.get("estabelecimento", {})
            endereco = estabelecimento.get("endereco", {})
            
            resultado = {
                "GTIN": produto.get("gtin"),
                "Descrição": produto.get("descricao"),
                "Valor da Venda": venda.get("valorVenda"),
                "Data da Venda": venda.get("dataVenda"),
                "Estabelecimento": estabelecimento.get("nomeFantasia"),
                "Município": endereco.get("municipio"),
                "Código IBGE": cod_ibge
            }
            resultados.append(resultado)
            
        if resultados:
            logger.info(f"✅ GTIN {gtin}: {len(resultados)} preços encontrados")
        else:
            logger.debug(f"ℹ️ GTIN {gtin}: Nenhum preço encontrado")
            
        return resultados
        
    except requests.exceptions.Timeout:
        logger.error(f"⏰ Timeout ao consultar GTIN {gtin} (município {cod_ibge})")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ Erro HTTP {e.response.status_code} para GTIN {gtin}: {e.response.text}")
        return []
    except requests.exceptions.ConnectionError as e:
        logger.error(f"🌐 Erro de conexão para GTIN {gtin}: {e}")
        return []
    except Exception as e:
        logger.error(f"❌ Erro inesperado para GTIN {gtin}: {e}")
        return []

def validar_gtin(gtin):
    """Valida se um GTIN é válido"""
    gtin_str = str(gtin).strip()
    return (
        len(gtin_str) in [8, 12, 13, 14] and 
        gtin_str.isnumeric() and 
        not gtin_str.startswith('17')
    )

def carregar_gtins():
    """Carrega e valida GTINs do arquivo Excel"""
    try:
        df = pd.read_excel("gtin_list.xlsx")
    except FileNotFoundError:
        logger.error("❌ ERRO: O arquivo 'gtin_list.xlsx' não foi encontrado na pasta.")
        return []
    except Exception as e:
        logger.error(f"❌ ERRO ao ler o arquivo 'gtin_list.xlsx': {e}")
        return []

    if "GTIN" not in df.columns:
        logger.error("❌ ERRO: O arquivo 'gtin_list.xlsx' não contém uma coluna chamada 'GTIN'.")
        return []

    gtins_brutos = df["GTIN"].dropna().astype(str)
    gtins_validos = [g.strip() for g in gtins_brutos if validar_gtin(g)]
    
    logger.info(f"�� Total de GTINs carregados: {len(gtins_brutos)}")
    logger.info(f"✅ GTINs válidos: {len(gtins_validos)}")
    
    return gtins_validos

def main():
    """Função principal do programa"""
    logger.info("�� Iniciando consulta de preços SEFAZ/AL")
    
    # Carregar GTINs
    gtins = carregar_gtins()
    if not gtins:
        logger.error("❌ Nenhum GTIN válido foi encontrado no arquivo 'gtin_list.xlsx'.")
        return

    if not CODIGOS_IBGE_AL:
        logger.error("❌ A lista 'CODIGOS_IBGE_AL' no arquivo config.py está vazia.")
        return

    logger.info(f"🎯 Consultando {len(gtins)} GTINs em {len(CODIGOS_IBGE_AL)} município(s)")
    
    todos_resultados = []
    total_consultas = len(gtins) * len(CODIGOS_IBGE_AL)
    consultas_realizadas = 0

    for cod_ibge in CODIGOS_IBGE_AL:
        logger.info(f"🌎 Consultando município: {cod_ibge}")
        
        for i, gtin in enumerate(gtins, 1):
            consultas_realizadas += 1
            progresso = (consultas_realizadas / total_consultas) * 100
            
            logger.info(f"📊 Progresso: {progresso:.1f}% - GTIN {i}/{len(gtins)}: {gtin}")
            
            resultados_gtin = consultar_preco(gtin, cod_ibge)
            if resultados_gtin:
                todos_resultados.extend(resultados_gtin)
            
            # Pequena pausa para não sobrecarregar a API
            time.sleep(0.5)

    # Salvar resultados
    if todos_resultados:
        df_final = pd.DataFrame(todos_resultados)
        df_final.to_excel("precos_encontrados.xlsx", index=False)
        logger.info(f"✅ Consulta finalizada! {len(todos_resultados)} preços salvos em 'precos_encontrados.xlsx'")
        
        # Estatísticas finais
        logger.info(f"📈 Estatísticas:")
        logger.info(f"   - Total de preços encontrados: {len(todos_resultados)}")
        logger.info(f"   - GTINs únicos: {df_final['GTIN'].nunique()}")
        logger.info(f"   - Municípios consultados: {df_final['Código IBGE'].nunique()}")
    else:
        logger.warning("⚠️ Nenhum preço foi encontrado para os GTINs e municípios consultados.")

if __name__ == "__main__":
    main()