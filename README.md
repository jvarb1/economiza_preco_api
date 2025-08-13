# Ferramenta CDBAR para Consulta de Preços em Alagoas

Esta é uma ferramenta desenvolvida pela CDBAR em Python para automatizar a consulta de preços de produtos na API pública do programa Economiza Alagoas, mantido pela Secretaria da Fazenda de Alagoas (SEFAZ/AL).

O principal objetivo é otimizar e escalar o processo de pesquisa de mercado e monitoramento de preços no varejo alagoano, fornecendo dados estratégicos para a tomada de decisão. A ferramenta lê uma lista de códigos GTIN, busca os preços mais recentes nos municípios de interesse e consolida todos os resultados em uma planilha Excel, pronta para análise.

## Principais Funcionalidades

* Consulta Automatizada: Processa múltiplos produtos (GTINs) em lote a partir de uma planilha.
* Busca Geográfica Flexível: Permite configurar um ou mais municípios de Alagoas para a pesquisa (via código IBGE).
* Pesquisa Retroativa: Define um período em dias para buscar o histórico de preços recente.
* Exportação de Dados: Salva os resultados (produto, valor, data, estabelecimento, município) em um arquivo .xlsx para fácil manipulação..
* Segurança: Utiliza um arquivo .env para gerenciar o token da API de forma segura, sem expô-lo no código.
* Robustez: Implementa um sistema de novas tentativas (retry) para lidar com eventuais instabilidades da API da SEFAZ.

## Pré-requisitos

* Python 3.8 ou superior
* Git

## Como Configurar e Executar

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### 1. Clonar o Repositório

Primeiro, clone este repositório para seu computador.

```bash
git clone [https://github.com/jvarb1/economiza_preco_api.git](https://github.com/jvarb1/economiza_preco_api.git)
cd economiza_preco_api
```

### 2. Instalar as Dependências

Este projeto requer algumas bibliotecas Python. Crie um arquivo chamado `requirements.txt` com o conteúdo abaixo ou instale-as diretamente.

**Conteúdo para `requirements.txt`:**
```text
pandas
requests
python-dotenv
openpyxl
```

**Comando para instalar as dependências:**
```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

O token da API é carregado de forma segura através de um arquivo `.env`.

1.  Crie um arquivo chamado `.env` na pasta raiz do projeto.
2.  Dentro dele, adicione a seguinte linha, substituindo `seu_token_aqui` pelo seu token real:
    ```
    SEFAZ_TOKEN="seu_token_aqui" - sem aspas
    ```

### 4. Executar a Consulta

1.  **Prepare a lista de produtos:** Abra o arquivo `gtin_list.xlsx` e adicione os códigos GTIN que deseja consultar na coluna `GTIN`.
2.  [cite_start]**Execute o script:** Dê um duplo clique no arquivo `executar.bat` para iniciar a consulta no Windows[cite: 4].
    * Alternativamente, você pode executar diretamente pelo terminal:
        ```bash
        python consulta.py
        ```
3.  [cite_start]**Verifique os resultados:** Ao final da execução, um novo arquivo chamado `precos_encontrados.xlsx` será criado na pasta com todos os dados coletados[cite: 3].

## Estrutura do Projeto

```
.
├── .env                # Arquivo com o token da API (ignorado pelo Git)
├── .gitignore          # Especifica arquivos a serem ignorados pelo Git
├── config.py           # Configurações gerais (URL, municípios, etc.)
├── consulta.py         # Script principal que executa a lógica de consulta
├── executar.bat        # Atalho para execução fácil no Windows
├── gtin_list.xlsx      # Planilha de entrada com a lista de produtos
└── README.md           # Este arquivo de instruções
```
