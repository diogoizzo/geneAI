# Aplicação de Chat com Ollama

## Visão Geral

Esta aplicação utiliza a biblioteca Ollama para processar recibos e realizar a análise de risco da hospitalidade, conforme a fórmula atualmente utilizada pelo jurídico. Primeiro, realiza a otimização da imagem passada (recibo), depois realiza o OCR (Reconhecimento Óptico de Caracteres) dessa imagem. O texto resultante é passado para a Gemma 2 8B do Google, rodado localmente para realizar as inferências necessárias.

## Instalação

### 1. Instalar Ollama

Para instalar Ollama, você pode usar o pip:

Acessando o site https://ollama.com/download e realizando o download da versão compatível com a plataforma desejada (Windows, Linux ou Mac).

### 2. Baixar o Modelo Gemma 2 8b

Após instalado o ollama, acesse o prompt de comando ou power shell e execute o comando abaixo:

ollama run gemma2:9b

Esse comando irá instalar a rede neural mencionada.

### 2. Iniciando o servidor ollama

Após a instalação, basta iniciar a aplicação desktop ou rodar o comando abaixo:

ollama serve

## Configuração

### 1. Ativar o Ambiente Virtual

Navegue até o diretório do projeto e ative o ambiente virtual:

```bash
cd /Users/dizzo/Dev/testeAi/chatollama
source bin/activate
```

### 2. Executar o Script Principal

Após ativar o ambiente virtual, você pode executar o script principal:

```bash
python main.py
```

## Uso

### 1. Fornecer o Caminho do Arquivo do Recibo

Quando solicitado, forneça o caminho do arquivo do recibo. Se o arquivo estiver localizado dentro do diretório do projeto, você pode apenas especificar o nome do arquivo.

Exemplo:

```bash
Digite o caminho do arquivo do recibo: recibo.jpg
```

## Como Funciona

A aplicação utiliza a biblioteca Ollama para processar a imagem do recibo. Ela realiza OCR para extrair texto da imagem e, em seguida, processa o texto extraído para gerar a saída necessária.

## Dependências

-   Python 3.11
-   Ollama
-   Modelo Gemma 2 8b
-   Outras dependências listadas em `requirements.txt`

## Licença

Este projeto está licenciado sob a Licença MIT.
