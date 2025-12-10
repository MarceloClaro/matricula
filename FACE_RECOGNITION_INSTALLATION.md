# Guia de Instalação do Reconhecimento Facial

## Visão Geral

Este documento explica como configurar o sistema de reconhecimento facial no Sistema de Matrícula Escolar. O reconhecimento facial utiliza as bibliotecas `dlib` e `face-recognition`, que requerem dependências do sistema para compilação.

## Solução Implementada

### 1. Dependências do Sistema (`packages.txt`)

O arquivo `packages.txt` foi configurado com todas as dependências necessárias para compilar o `dlib` no Streamlit Cloud:

```
build-essential      # Ferramentas de compilação C++
cmake               # Sistema de build necessário para dlib
libopenblas-dev     # Biblioteca de álgebra linear
liblapack-dev       # Rotinas de álgebra linear
libx11-dev          # Arquivos de desenvolvimento X11
libgtk-3-dev        # Arquivos de desenvolvimento GTK
libatlas-base-dev   # Biblioteca ATLAS para operações matemáticas
gfortran            # Compilador Fortran (necessário para algumas bibliotecas)
```

### 2. Dependências Python (`requirements.txt`)

As bibliotecas de reconhecimento facial foram integradas ao `requirements.txt` principal:

```python
# Face Recognition Dependencies
dlib==19.24.0              # Biblioteca base para detecção e reconhecimento facial
face-recognition==1.3.0    # API de alto nível para reconhecimento facial

# Anti-spoofing (liveness detection)
tensorflow==2.15.0         # Para detectar fotos falsas (anti-spoofing)

# Data augmentation
imgaug==0.4.0             # Aumentação de dados para melhor treinamento
```

**Nota:** Foi utilizado `opencv-python-headless` em vez de `opencv-python` para compatibilidade com ambientes sem GUI (como Streamlit Cloud).

## Instalação

### Para Streamlit Cloud

1. Faça commit dos arquivos `packages.txt` e `requirements.txt` no repositório
2. Faça deploy no Streamlit Cloud
3. O Streamlit Cloud instalará automaticamente:
   - As dependências do sistema do `packages.txt`
   - As dependências Python do `requirements.txt`
4. O reconhecimento facial estará disponível se a instalação for bem-sucedida

### Para Desenvolvimento Local

#### Ubuntu/Debian

```bash
# 1. Instalar dependências do sistema
sudo apt-get update
sudo apt-get install -y build-essential cmake libopenblas-dev liblapack-dev \
                        libx11-dev libgtk-3-dev libatlas-base-dev gfortran

# 2. Clonar o repositório
git clone https://github.com/MarceloClaro/matricula.git
cd matricula

# 3. Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependências Python
pip install -r requirements.txt

# 5. Executar a aplicação
streamlit run app.py
```

#### macOS

```bash
# 1. Instalar Homebrew (se ainda não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependências do sistema
brew install cmake

# 3. Clonar o repositório
git clone https://github.com/MarceloClaro/matricula.git
cd matricula

# 4. Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 5. Instalar dependências Python
pip install -r requirements.txt

# 6. Executar a aplicação
streamlit run app.py
```

#### Windows (usando Anaconda/Miniconda)

```bash
# 1. Instalar Anaconda/Miniconda se ainda não tiver
# Download: https://www.anaconda.com/products/distribution

# 2. Criar ambiente conda
conda create -n matricula python=3.10
conda activate matricula

# 3. Clonar o repositório
git clone https://github.com/MarceloClaro/matricula.git
cd matricula

# 4. Instalar dlib via conda-forge (recomendado para Windows)
conda install -c conda-forge dlib

# 5. Instalar outras dependências
pip install streamlit pandas reportlab pillow plotly opencv-python-headless \
            scikit-learn numpy face-recognition tensorflow imgaug

# 6. Executar a aplicação
streamlit run app.py
```

## Troubleshooting

### Erro: "Failed building wheel for dlib"

**Causa:** Dependências do sistema não instaladas ou CMake incompatível.

**Solução:**
1. Verifique se todas as dependências do sistema estão instaladas
2. Para Ubuntu/Debian:
   ```bash
   sudo apt-get install -y build-essential cmake libopenblas-dev liblapack-dev \
                           libx11-dev libgtk-3-dev libatlas-base-dev gfortran
   ```
3. Para Windows, use conda-forge:
   ```bash
   conda install -c conda-forge dlib
   ```

### Erro: "CMake Error: Compatibility with CMake < 3.5 has been removed"

**Causa:** Versão do CMake muito recente (3.31+) incompatível com dlib 19.24.2.

**Solução:** 
- Foi utilizado dlib 19.24.0 em vez de 19.24.2 para melhor compatibilidade
- Se o problema persistir, use conda-forge

### Sistema funciona mas reconhecimento facial não está disponível

**Causa:** A instalação do dlib/face-recognition falhou, mas o sistema continua funcionando.

**Comportamento esperado:** O sistema foi projetado para funcionar mesmo sem reconhecimento facial.

**Verificação:**
```python
python test_imports.py
```

**Para habilitar o reconhecimento facial:**
1. Instale as dependências do sistema
2. Reinstale o dlib:
   ```bash
   pip install --force-reinstall dlib face-recognition
   ```

## Arquitetura da Solução

### Graceful Degradation

O sistema foi projetado para funcionar mesmo se o reconhecimento facial não estiver disponível:

```python
# modulos/reconhecimento_facial.py
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

class FaceRecognitionSystem:
    def __init__(self):
        self.available = FACE_RECOGNITION_AVAILABLE
    
    def capture_photo_sequence(self, ...):
        if not self.available:
            st.error("❌ Reconhecimento Facial não está disponível")
            return []
        # ... implementação
```

### Funcionalidades Disponíveis

#### ✅ Sem Reconhecimento Facial
- Cadastro Geral de Alunos
- PEI (Plano Educacional Individualizado)
- Dados Socioeconômicos
- Questionário SAEB/SPAECE
- Informações de Saúde
- Dashboard com estatísticas
- Busca de alunos
- Geração de PDFs
- Exportação de dados
- Backup e restauração

#### 🔐 Com Reconhecimento Facial
- Todas as funcionalidades acima +
- Registro de Presença (cadastro facial)
- Frequência de Aula (marcação automática de presença)
- Anti-spoofing (detecção de fotos falsas)

## Referências

Esta solução foi baseada em:
- [coneypo/Dlib_face_recognition_from_camera](https://github.com/coneypo/Dlib_face_recognition_from_camera)
- [MarceloClaro/Attendance-with-Face-Recognition](https://github.com/MarceloClaro/Attendance-with-Face-Recognition)

## Suporte

### Verificar Status da Instalação

Execute o script de teste:
```bash
python test_imports.py
```

Este script mostrará:
- ✓ Módulos básicos instalados
- ✓/⚠ Status do reconhecimento facial
- ✓ Status dos módulos do sistema

### Logs de Debug

Para ver logs detalhados durante a instalação:
```bash
pip install -v -r requirements.txt
```

### Problemas Conhecidos

1. **Python 3.12+**: Algumas versões do dlib podem ter problemas com Python 3.12. Recomenda-se Python 3.10 ou 3.11.
2. **Windows**: A compilação do dlib é complexa no Windows. Use conda-forge.
3. **Streamlit Cloud**: A compilação pode levar vários minutos na primeira vez.

## Conclusão

A solução implementada garante que:
- ✅ O sistema funciona em todos os ambientes (com ou sem reconhecimento facial)
- ✅ O Streamlit Cloud pode compilar o dlib com as dependências corretas
- ✅ Instalação local é possível com instruções claras
- ✅ Graceful degradation mantém o sistema funcional mesmo sem reconhecimento facial
