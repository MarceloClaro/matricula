# 🎓 Sistema de Matrícula Escolar 2026

Sistema completo de gerenciamento de matrículas escolares desenvolvido em Streamlit com persistência em CSV.

## 📋 Funcionalidades

### Módulos de Cadastro
- **Cadastro Geral**: Dados pessoais, endereço e informações escolares
  - **Novo!** 📸 Upload de fotos dos alunos (3x4)
- **PEI**: Plano Educacional Individualizado para alunos com necessidades especiais
- **Socioeconômico**: Questionário completo sobre situação socioeconômica familiar
- **Questionário SAEB/SPAECE**: Questionário completo do aluno baseado no SAEB/SPAECE com 13 seções
- **Saúde**: Ficha de saúde com dados médicos e contato de emergência

### 🆕 Reconhecimento Facial e Controle de Presença
- **Registro de Presença**: 
  - Captura automática de 30 fotos em 10 segundos via webcam
  - Data augmentation para melhor precisão (flip, rotação, escala, brilho, blur)
  - Treinamento automático de reconhecimento facial
  - Suporte para re-treinamento do modelo
- **Frequência de Aula**:
  - Marcação automática de presença via reconhecimento facial
  - Anti-spoofing (detecção de liveness) para evitar fraudes com fotos
  - Registro com data, hora e nível de confiança
  - Visualização de registros do dia e histórico completo
  - Exportação de relatórios de presença em CSV
- **Características Técnicas**:
  - Face recognition com face_recognition library
  - CNN para detecção de liveness (anti-spoofing)
  - Early stopping para evitar overfitting
  - Persistência de embeddings faciais
  - Confiança mínima de 60% para reconhecimento

### Gestão e Análise
- **Dashboard**: Visualização de estatísticas e gráficos interativos
- **CRUD Completo**: Criar, ler, atualizar e deletar registros
- **Busca Inteligente**: Busca rápida e avançada com múltiplos filtros

### Documentos e Exportação
- **PDF Individual**: Geração de ficha completa de matrícula em PDF com foto do aluno
- **Exportação em Lote**: Exportação de múltiplos PDFs e dados CSV em arquivo ZIP
- **Novo!** 📄 **Exportar Lista de Alunos**:
  - **JSON**: Exporta dados dos alunos filtrados em formato JSON
  - **PDFs em Lote**: Gera ZIP com PDFs de todos os alunos (com fotos)
  - **PDF+JSON Completo**: Exportação completa com PDFs, JSON e README

### Segurança
- **Backup e Restauração**: Sistema completo de backup e recuperação de todos os dados
- **Anti-Spoofing**: Sistema de detecção de fotos para evitar fraudes na marcação de presença

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip
- Webcam (opcional, para reconhecimento facial)
- **Sistemas Linux/Mac**: CMake e dlib dependencies (opcional, para reconhecimento facial)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
  
  # macOS
  brew install cmake
  ```

**Nota sobre Reconhecimento Facial:**
O reconhecimento facial é uma funcionalidade opcional. Se as bibliotecas `dlib` e `face-recognition` não puderem ser instaladas, o sistema funcionará normalmente sem essa funcionalidade. As demais funcionalidades (cadastro, dashboard, PDFs, etc.) continuarão disponíveis.

### Implantação no Streamlit Cloud

Para implantar no Streamlit Cloud, o arquivo `packages.txt` já está configurado com as dependências necessárias para o reconhecimento facial. Se a instalação do `dlib` falhar, o sistema funcionará sem a funcionalidade de reconhecimento facial.

### Passos para instalação

1. Clone o repositório:
```bash
git clone https://github.com/MarceloClaro/matricula.git
cd matricula
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

**Nota:** Em alguns sistemas, pode ser necessário instalar o dlib manualmente:
```bash
pip install cmake
pip install dlib
```

Se a instalação do `dlib` falhar (comum em ambientes Windows ou sistemas sem compilador C++), você pode:
1. Usar o sistema sem reconhecimento facial (outras funcionalidades continuarão funcionando)
2. Instalar uma versão pré-compilada do dlib:
   ```bash
   # Windows: baixar wheel do dlib de https://github.com/z-mahmud22/Dlib_Windows_Python3.x
   pip install dlib-19.24.2-cp310-cp310-win_amd64.whl  # ajuste para sua versão do Python
   ```
3. Remover as linhas `face-recognition==1.3.0` e `dlib==19.24.2` do `requirements.txt` se não precisar dessa funcionalidade

3. Execute a aplicação:
```bash
streamlit run app.py
```

4. Acesse no navegador:
```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
matricula/
├── app.py                      # Aplicação principal Streamlit
├── data_manager.py             # Gerenciador de dados CSV
├── requirements.txt            # Dependências do projeto
├── modulos/                    # Módulos auxiliares
│   ├── __init__.py
│   ├── cadastro_geral.py      # Módulo de cadastro geral
│   ├── pei.py                 # Módulo PEI
│   ├── socioeconomico.py      # Módulo socioeconômico
│   ├── questionario_saeb.py   # Módulo questionário SAEB/SPAECE
│   ├── saude.py               # Módulo de saúde
│   ├── reconhecimento_facial.py  # Sistema de reconhecimento facial
│   ├── registro_presenca.py   # Cadastro facial de alunos
│   ├── frequencia_aula.py     # Marcação de presença facial
│   ├── dashboard.py           # Dashboard com gráficos
│   ├── crud.py                # Gerenciamento CRUD
│   ├── busca.py               # Busca inteligente
│   ├── pdf_generator.py       # Gerador de PDF
│   ├── export_zip.py          # Exportação em lote
│   └── backup.py              # Backup e restauração
└── data/                       # Dados CSV (criado automaticamente)
    ├── fotos/                 # Fotos dos alunos (3x4)
    ├── faces/                 # Fotos para reconhecimento facial
    │   └── aluno_{id}/       # 30 fotos por aluno
    ├── models/                # Modelos treinados
    │   ├── face_embeddings.pkl   # Encodings faciais
    │   └── liveness_model.h5     # Modelo anti-spoofing
    ├── cadastro_geral.csv
    ├── pei.csv
    ├── socioeconomico.csv
    ├── questionario_saeb.csv
    ├── saude.csv
    ├── face_embeddings.csv    # Registro de embeddings
    └── attendance.csv         # Registros de presença
```

## 💾 Persistência de Dados

Os dados são armazenados em arquivos CSV na pasta `data/`:
- **fotos/**: Fotos dos alunos em formato JPEG (3x4, otimizadas)
- **faces/**: Fotos capturadas para reconhecimento facial (30 fotos por aluno)
- **models/**: Modelos de ML treinados (embeddings e anti-spoofing)
- **cadastro_geral.csv**: Dados pessoais e escolares dos alunos
- **pei.csv**: Informações do Plano Educacional Individualizado
- **socioeconomico.csv**: Dados socioeconômicos
- **face_embeddings.csv**: Registro de cadastros faciais
- **attendance.csv**: Registros de presença com data/hora/confiança
- **questionario_saeb.csv**: Questionário SAEB/SPAECE do aluno
- **saude.csv**: Informações de saúde

Os arquivos são criados automaticamente na primeira execução.

## 📊 Dashboard

O dashboard inclui:
- Métricas principais (total de alunos, ativos, com PEI, cadastros completos)
- Gráficos de distribuição por ano escolar, turno e status
- Análise socioeconômica (renda familiar, recursos tecnológicos, benefícios)
- Análise de saúde (tipo sanguíneo, vacinação, plano de saúde)
- Lista de alunos com cadastro incompleto

## 🔍 Busca Inteligente

Duas modalidades de busca:
- **Busca Rápida**: Por nome ou ID do aluno
- **Busca Avançada**: Múltiplos filtros (ano, turno, cidade, status, etc.)

## 📄 Geração de PDF

### PDFs com Foto do Aluno
Os PDFs individuais agora incluem a foto do aluno (se disponível) junto com:
- Foto 3x4 no topo do documento
- Dados pessoais e de contato
- Endereço completo
- Informações escolares
- PEI (se aplicável)
- Dados socioeconômicos
- Ficha de saúde
- Anamnese Pedagógica (se aplicável)

Layout similar à ficha municipal com formatação profissional.

## 📦 Exportação em Lote

A **Lista de Alunos** agora oferece três opções de exportação:

### 1. 📥 Exportar JSON
- Exporta dados dos alunos filtrados em formato JSON
- Ideal para integração com outros sistemas
- Mantém toda a estrutura de dados

### 2. 📄 Gerar PDFs em Lote
- Cria arquivo ZIP com PDFs individuais de todos os alunos
- Cada PDF inclui a foto do aluno (se disponível)
- Nome dos arquivos: `ficha_{id}_{nome}.pdf`

### 3. 📦 Exportar PDF+JSON
- Exportação completa em ZIP contendo:
  - `pdfs/` - Fichas de matrícula de todos os alunos em PDF (com fotos)
  - `dados/` - Arquivo JSON com todos os dados dos alunos
  - `README.txt` - Informações sobre o conteúdo da exportação

Permite exportar (modo antigo ainda disponível em "Exportar em Lote (ZIP)"):
- PDFs de múltiplos alunos
- Dados CSV filtrados
- Relatório resumido com estatísticas
- Tudo compactado em arquivo ZIP

## 💾 Backup e Restauração

O sistema inclui funcionalidade completa de backup e restauração:

### Criar Backup
- Cria arquivo ZIP com todos os dados CSV
- Inclui timestamp automático no nome do arquivo
- Download instantâneo do backup criado

### Restaurar Backup
- Upload de arquivo de backup ZIP
- Validação de integridade dos dados
- Backup automático dos dados atuais antes da restauração
- Confirmação obrigatória para segurança

### Gerenciar Backups
- Lista todos os backups disponíveis
- Informações de data, hora e tamanho
- Download de backups anteriores
- Exclusão de backups antigos

### Boas Práticas
- Crie backups regularmente (diário, semanal ou mensal)
- Mantenha cópias em locais seguros
- Teste a restauração periodicamente
- Os backups são salvos na pasta `backups/`
- **Importante**: Backups não incluem fotos dos alunos. Faça backup separado da pasta `data/fotos/` se necessário.

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para interface web
- **Pandas**: Manipulação de dados CSV
- **ReportLab**: Geração de PDFs
- **Plotly**: Gráficos interativos
- **OpenCV**: Processamento de imagens e captura de webcam
- **face_recognition**: Reconhecimento facial baseado em dlib
- **TensorFlow/Keras**: Modelo CNN para detecção de liveness
- **imgaug**: Data augmentation para treinamento
- **scikit-learn**: Ferramentas de machine learning
- **Python**: Linguagem principal

## 📝 Como Usar

### Fluxo Básico
1. **Cadastrar Alunos**: Acesse "Cadastro Geral" e preencha os dados
   - **Novo!** 📸 Faça upload da foto 3x4 do aluno no primeiro campo
2. **Completar Informações**: Preencha PEI, Socioeconômico, Questionário SAEB e Saúde para cada aluno
3. **Cadastrar Face**: Use "Registro de Presença" para capturar fotos faciais
4. **Marcar Presença**: Use "Frequência de Aula" para reconhecimento automático
5. **Visualizar Estatísticas**: Acesse o Dashboard
6. **Buscar Alunos**: Use a busca inteligente
7. **Gerar Documentos**: Crie PDFs individuais ou exportação em lote
   - PDFs agora incluem a foto do aluno automaticamente
8. **Exportar Dados**: Use a aba "Lista de Alunos" para exportar em JSON ou gerar PDFs em lote

### 📸 Upload de Fotos

**Formato Recomendado**: 
- Fotos 3x4 (proporção padrão)
- Formatos aceitos: JPG, JPEG, PNG
- As imagens são automaticamente redimensionadas para 300x400 pixels
- Qualidade otimizada para tamanho de arquivo reduzido

**Como fazer upload**:
1. Acesse "Cadastro Geral" > "Novo Cadastro"
2. No campo "Foto do Aluno (3x4)", clique em "Browse files"
3. Selecione a foto do aluno
4. A foto será processada e salva automaticamente ao finalizar o cadastro

### 🆕 Sistema de Reconhecimento Facial

O sistema agora inclui reconhecimento facial completo com anti-spoofing para controle de presença.

#### 📸 Registro de Presença (Cadastro Facial)

**Como cadastrar um aluno para reconhecimento facial:**

1. Acesse "Registro de Presença" no menu
2. Selecione o aluno já cadastrado no sistema
3. Clique em "Iniciar Captura de Fotos"
4. O sistema irá capturar 30 fotos em 10 segundos automaticamente
5. Durante a captura, varie levemente a posição da cabeça
6. O sistema aplica data augmentation (flip, rotação, escala, brilho, blur)
7. Aguarde o treinamento automático do modelo
8. Pronto! O aluno já pode marcar presença via reconhecimento facial

**Dicas para melhor captura:**
- Mantenha boa iluminação (evite contra-luz)
- Posicione o rosto centralizado na câmera
- Mantenha distância de 50-80cm da câmera
- Varie levemente a posição (não exagere nos movimentos)
- Evite usar óculos escuros ou chapéus

**Re-treinamento:**
- Use a aba "Re-treinar Modelo" para retreinar todos os alunos
- Útil após cadastrar vários alunos novos
- Melhora a precisão geral do sistema

#### ✅ Frequência de Aula (Marcação de Presença)

**Como marcar presença:**

1. Acesse "Frequência de Aula" no menu
2. Clique em "Iniciar Reconhecimento Facial"
3. Posicione seu rosto na frente da câmera
4. O sistema reconhecerá automaticamente em segundos
5. A presença será registrada com:
   - Data e hora
   - Nível de confiança (mínimo 60%)
   - Status de verificação

**Segurança Anti-Spoofing:**
- O sistema detecta fotos e rejeita automaticamente
- Usa modelo CNN treinado para liveness detection
- Impede fraudes com fotos impressas ou em telas
- Mensagem "FOTO DETECTADA!" aparece se tentar usar foto

**Visualização de Registros:**
- Aba "Registros de Hoje": veja presenças do dia atual
- Aba "Histórico Completo": acesse registros anteriores
- Filtros por data e aluno
- Exportação em CSV para relatórios
- Gráficos de presença por data e por aluno

#### 🔐 Características Técnicas

**Reconhecimento Facial:**
- Biblioteca: face_recognition (baseada em dlib)
- Algoritmo: 128-dimensional face encoding
- Tolerância: 0.5 (balanço entre precisão e recall)
- Confiança mínima: 60%

**Data Augmentation:**
- Flip horizontal: 50% das imagens
- Rotação: -10° a +10°
- Escala: 90% a 110%
- Brilho: 80% a 120%
- Blur gaussiano leve

**Anti-Spoofing:**
- Modelo: CNN (Convolutional Neural Network)
- Arquitetura: 3 camadas Conv2D + Dense
- Early stopping com patience=3
- Input: 64x64 pixels RGB
- Output: probabilidade de ser real (0-1)

**Persistência:**
- Face embeddings salvos em pickle
- Modelo de liveness em formato H5 (Keras)
- Registros de presença em CSV
- Fotos originais mantidas para re-treinamento

### 📋 Questionário SAEB/SPAECE

O Questionário SAEB/SPAECE inclui 13 seções completas:

1. **Identificação**: Informações básicas do aluno
2. **Informações Pessoais**: Sexo, idade, língua falada, cor/raça
3. **Informações de Inclusão**: Deficiência, TEA, altas habilidades
4. **Composição Familiar**: Quem mora com o aluno e escolaridade dos responsáveis
5. **Rotina Familiar**: Apoio dos responsáveis
6. **Condições do Bairro**: Infraestrutura do bairro
7. **Condições da Casa**: Bens e recursos disponíveis
8. **Trajeto à Escola**: Tempo e meio de transporte
9. **Histórico Escolar**: Trajetória educacional
10. **Uso do Tempo**: Como o aluno distribui seu tempo
11. **Práticas Pedagógicas**: Percepção sobre os professores
12. **Percepção da Escola**: Avaliação do ambiente escolar
13. **Expectativas Futuras**: Planos após conclusão do ano

## 🔒 Segurança

- Dados armazenados localmente
- Sem conexão com serviços externos
- Validação de dados obrigatórios
- Confirmação para operações de exclusão

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📞 Suporte

Para dúvidas ou suporte, abra uma issue no GitHub.