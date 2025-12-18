# 🚀 Como Executar o Framework

Este documento explica como executar o Sistema de Matrícula Escolar 2026.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação das Dependências

Antes de executar o framework, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Formas de Executar

### Opção 1: Usando o Script de Inicialização (Recomendado)

Execute o script shell que inicia o framework automaticamente:

```bash
./run.sh
```

### Opção 2: Comando Direto do Streamlit

Execute diretamente com o comando Streamlit:

```bash
streamlit run app.py
```

### Opção 3: Especificando Porta

Execute em uma porta específica:

```bash
streamlit run app.py --server.port 8080
```

### Opção 4: Modo Headless (Sem Browser)

Para ambientes de servidor sem interface gráfica:

```bash
streamlit run app.py --server.headless true
```

### Opção 5: Background/Daemon

Para executar em segundo plano:

```bash
nohup streamlit run app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
```

## Acessando a Aplicação

Após iniciar o framework, acesse a aplicação no navegador:

```
http://localhost:8501
```

Se você especificou uma porta diferente, use:

```
http://localhost:<PORTA>
```

## Verificação de Execução

Para verificar se o framework está rodando:

```bash
# Verificar processo
ps aux | grep streamlit

# Verificar porta
netstat -tlnp | grep 8501
```

## Parar a Execução

### Se iniciou no terminal (Ctrl+C)
Pressione `Ctrl+C` no terminal onde o Streamlit está rodando.

### Se está rodando em background
```bash
# Encontrar o PID do processo
ps aux | grep streamlit

# Parar o processo (substitua PID pelo número do processo)
kill <PID>
```

## Funcionalidades Disponíveis

Após executar o framework, você terá acesso a:

- 📝 **Cadastro Geral**: Dados pessoais e escolares
- ♿ **PEI**: Plano Educacional Individualizado
- 💰 **Socioeconômico**: Questionário socioeconômico
- 📋 **Questionário SAEB**: Questionário SAEB/SPAECE
- 🏥 **Saúde**: Ficha de saúde
- 📸 **Registro de Presença**: Cadastro facial
- ✅ **Frequência de Aula**: Reconhecimento facial
- 📊 **Dashboard**: Estatísticas e gráficos
- ⚙️ **Gerenciamento (CRUD)**: Editar e deletar registros
- 🔍 **Busca Inteligente**: Busca avançada
- 📄 **Gerar PDF Individual**: Fichas em PDF
- 📦 **Exportar em Lote**: Exportação múltipla
- 💾 **Backup e Restauração**: Segurança dos dados

## Solução de Problemas

### Erro: "streamlit: command not found"
```bash
pip install streamlit==1.29.0
```

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Porta já em uso
```bash
# Use uma porta diferente
streamlit run app.py --server.port 8502
```

### Erro de permissão no run.sh
```bash
chmod +x run.sh
```

## Reconhecimento Facial (Opcional)

Para habilitar o reconhecimento facial, consulte o arquivo `FACE_RECOGNITION_INSTALLATION.md`.

## Dados e Persistência

Os dados são armazenados automaticamente na pasta `/data` em formato CSV. Backups podem ser criados através do menu "💾 Backup e Restauração".

## Suporte

Para mais informações, consulte o `README.md` principal do projeto.
