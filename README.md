# 🎓 Sistema de Matrícula Escolar 2026

Sistema completo de gerenciamento de matrículas escolares desenvolvido em Streamlit com persistência em CSV.

## 📋 Funcionalidades

### Módulos de Cadastro
- **Cadastro Geral**: Dados pessoais, endereço e informações escolares
- **PEI**: Plano Educacional Individualizado para alunos com necessidades especiais
- **Socioeconômico**: Questionário completo sobre situação socioeconômica familiar
- **Questionário SAEB/SPAECE**: Questionário completo do aluno baseado no SAEB/SPAECE com 13 seções
- **Saúde**: Ficha de saúde com dados médicos e contato de emergência

### Gestão e Análise
- **Dashboard**: Visualização de estatísticas e gráficos interativos
- **CRUD Completo**: Criar, ler, atualizar e deletar registros
- **Busca Inteligente**: Busca rápida e avançada com múltiplos filtros

### Documentos
- **PDF Individual**: Geração de ficha completa de matrícula em PDF
- **Exportação em Lote**: Exportação de múltiplos PDFs e dados CSV em arquivo ZIP

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip

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
│   ├── dashboard.py           # Dashboard com gráficos
│   ├── crud.py                # Gerenciamento CRUD
│   ├── busca.py               # Busca inteligente
│   ├── pdf_generator.py       # Gerador de PDF
│   └── export_zip.py          # Exportação em lote
└── data/                       # Dados CSV (criado automaticamente)
    ├── cadastro_geral.csv
    ├── pei.csv
    ├── socioeconomico.csv
    ├── questionario_saeb.csv
    └── saude.csv
```

## 💾 Persistência de Dados

Os dados são armazenados em arquivos CSV na pasta `data/`:
- **cadastro_geral.csv**: Dados pessoais e escolares dos alunos
- **pei.csv**: Informações do Plano Educacional Individualizado
- **socioeconomico.csv**: Dados socioeconômicos
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

PDFs individuais incluem:
- Dados pessoais e de contato
- Endereço completo
- Informações escolares
- PEI (se aplicável)
- Dados socioeconômicos
- Ficha de saúde

Layout similar à ficha municipal com formatação profissional.

## 📦 Exportação em Lote

Permite exportar:
- PDFs de múltiplos alunos
- Dados CSV filtrados
- Relatório resumido com estatísticas
- Tudo compactado em arquivo ZIP

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para interface web
- **Pandas**: Manipulação de dados CSV
- **ReportLab**: Geração de PDFs
- **Plotly**: Gráficos interativos
- **Python**: Linguagem principal

## 📝 Como Usar

1. **Cadastrar Alunos**: Acesse "Cadastro Geral" e preencha os dados
2. **Completar Informações**: Preencha PEI, Socioeconômico, Questionário SAEB e Saúde para cada aluno
3. **Visualizar Estatísticas**: Acesse o Dashboard
4. **Buscar Alunos**: Use a busca inteligente
5. **Gerar Documentos**: Crie PDFs individuais ou exportação em lote

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