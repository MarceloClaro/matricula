"""
Sistema de Matrícula Escolar 2026
Aplicação principal em Streamlit
"""
import streamlit as st
from data_manager import DataManager
from modulos import cadastro_geral, pei, socioeconomico, saude, questionario_saeb, anamnese_pei, dashboard, crud, busca, pdf_generator, export_zip, backup, registro_presenca, frequencia_aula, registro_lote

# Configuração da página
st.set_page_config(
    page_title="Matrícula Escolar 2026",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .stButton>button {
        width: 100%;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

data_manager = get_data_manager()

# Sidebar - Menu de navegação
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/school.png", width=80)
    st.title("Matrícula Escolar 2026")
    st.markdown("---")
    
    menu_opcao = st.radio(
        "Menu Principal",
        [
            "🏠 Início",
            "📝 Cadastro Geral",
            "♿ PEI",
            "🧠 Anamnese Pedagógica (PEI)",
            "💰 Socioeconômico",
            "📋 Questionário SAEB",
            "🏥 Saúde",
            "📸 Registro de Presença",
            "✅ Frequência de Aula",
            "📸👥 Registro em Lote (Foto da Turma)",
            "📊 Dashboard",
            "⚙️ Gerenciamento (CRUD)",
            "🔍 Busca Inteligente",
            "📄 Gerar PDF Individual",
            "📦 Exportar em Lote (ZIP)",
            "💾 Backup e Restauração"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Estatísticas rápidas
    st.subheader("📈 Estatísticas")
    df_cadastro = data_manager.get_data('cadastro')
    
    if len(df_cadastro) > 0:
        st.metric("Total de Alunos", len(df_cadastro))
        
        ativos = len(df_cadastro[df_cadastro['status'] == 'Ativo'])
        st.metric("Alunos Ativos", ativos)
        
        df_pei = data_manager.get_data('pei')
        com_pei = len(df_pei[df_pei['necessidade_especial'] == 'Sim'])
        st.metric("Com PEI", com_pei)
    else:
        st.info("Nenhum aluno cadastrado")
    
    st.markdown("---")
    st.caption("Sistema de Matrícula Escolar v1.0")

# Conteúdo principal
if menu_opcao == "🏠 Início":
    st.title("🎓 Sistema de Matrícula Escolar 2026")
    st.markdown("---")
    
    st.markdown("""
    ## Bem-vindo ao Sistema de Matrícula Escolar!
    
    Este sistema foi desenvolvido para facilitar o gerenciamento completo das matrículas escolares,
    incluindo cadastro de alunos e todas as informações complementares necessárias.
    
    ### 📋 Funcionalidades Disponíveis:
    
    #### Cadastros
    - **Cadastro Geral**: Dados pessoais, endereço e informações escolares
    - **PEI**: Plano Educacional Individualizado para alunos com necessidades especiais
    - **Socioeconômico**: Questionário socioeconômico para análise do perfil dos alunos
    - **Questionário SAEB**: Questionário completo SAEB/SPAECE do aluno
    - **Saúde**: Ficha de saúde com informações médicas e contato de emergência
    
    #### 🆕 Reconhecimento Facial e Presença
    - **Registro de Presença**: Cadastro facial de alunos com captura de 30 fotos em 10 segundos
    - **Frequência de Aula**: Marcação automática de presença com reconhecimento facial
    - **🆕 Registro em Lote**: Upload de foto da turma para identificação automática e registro de presença em lote
    - **Anti-Spoofing**: Sistema de detecção de fotos para evitar fraudes
    - **Treinamento Automático**: Re-treina modelo a cada novo aluno cadastrado
    
    #### Gestão e Análise
    - **Dashboard**: Visualização de estatísticas e gráficos
    - **Gerenciamento (CRUD)**: Editar, visualizar e deletar registros
    - **Busca Inteligente**: Busca rápida e avançada com múltiplos filtros
    
    #### Documentos
    - **PDF Individual**: Gerar ficha completa de matrícula em PDF
    - **Exportação em Lote**: Exportar múltiplos PDFs e dados em formato ZIP
    
    #### Segurança
    - **Backup e Restauração**: Sistema completo de backup e recuperação de dados
    
    ### 🚀 Como Começar:
    
    1. **Cadastre os alunos** através do menu "Cadastro Geral"
    2. **Complete os dados** nos módulos PEI, Socioeconômico, Questionário SAEB e Saúde
    3. **Cadastre faces** no "Registro de Presença" para reconhecimento facial
    4. **Marque presenças** usando "Frequência de Aula" com reconhecimento automático
    5. **🆕 Ou use "Registro em Lote"** para registrar presença de vários alunos de uma só vez com uma foto da turma
    6. **Visualize estatísticas** no Dashboard
    7. **Gere documentos** em PDF conforme necessário
    
    ### 💡 Dicas:
    
    - Use a busca inteligente para encontrar alunos rapidamente
    - O Dashboard mostra alunos com cadastro incompleto
    - Você pode exportar todos os dados em CSV e PDF
    - Os dados são salvos automaticamente em arquivos CSV na pasta 'data'
    - **Novo!** Sistema de reconhecimento facial com anti-spoofing
    - **Novo!** Registro em lote: tire uma foto da turma e registre presença de todos de uma vez
    - **Novo!** Crie backups regulares dos seus dados para maior segurança
    
    ---
    
    **Selecione uma opção no menu lateral para começar!** 👈
    """)
    
    # Cards informativos
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.info("📝\n\n**Cadastro Geral**\n\nDados pessoais e escolares completos")
    
    with col2:
        st.info("♿\n\n**PEI**\n\nPlano Educacional Individualizado")
    
    with col3:
        st.info("💰\n\n**Socioeconômico**\n\nPerfil socioeconômico familiar")
    
    with col4:
        st.info("📋\n\n**Quest. SAEB**\n\nQuestionário SAEB/SPAECE")
    
    with col5:
        st.info("🏥\n\n**Saúde**\n\nDados de saúde e emergência")
    
    with col6:
        st.info("💾\n\n**Backup**\n\nBackup e restauração de dados")

elif menu_opcao == "📝 Cadastro Geral":
    tab1, tab2 = st.tabs(["Novo Cadastro", "Lista de Alunos"])
    
    with tab1:
        cadastro_geral.render_cadastro_geral(data_manager)
    
    with tab2:
        cadastro_geral.render_lista_alunos(data_manager)

elif menu_opcao == "♿ PEI":
    pei.render_pei(data_manager)

elif menu_opcao == "🧠 Anamnese Pedagógica (PEI)":
    anamnese_pei.render_anamnese_pei(data_manager)

elif menu_opcao == "💰 Socioeconômico":
    socioeconomico.render_socioeconomico(data_manager)

elif menu_opcao == "📋 Questionário SAEB":
    questionario_saeb.render_questionario_saeb(data_manager)

elif menu_opcao == "🏥 Saúde":
    saude.render_saude(data_manager)

elif menu_opcao == "📸 Registro de Presença":
    registro_presenca.render_registro_presenca(data_manager)

elif menu_opcao == "✅ Frequência de Aula":
    frequencia_aula.render_frequencia_aula(data_manager)

elif menu_opcao == "📸👥 Registro em Lote (Foto da Turma)":
    registro_lote.render_registro_lote(data_manager)

elif menu_opcao == "📊 Dashboard":
    dashboard.render_dashboard(data_manager)

elif menu_opcao == "⚙️ Gerenciamento (CRUD)":
    crud.render_crud(data_manager)

elif menu_opcao == "🔍 Busca Inteligente":
    busca.render_busca(data_manager)

elif menu_opcao == "📄 Gerar PDF Individual":
    pdf_generator.render_pdf_generator(data_manager)

elif menu_opcao == "📦 Exportar em Lote (ZIP)":
    export_zip.render_export_zip(data_manager)

elif menu_opcao == "💾 Backup e Restauração":
    backup.render_backup(data_manager)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Sistema de Matrícula Escolar 2026 - Desenvolvido com ❤️ usando Streamlit</p>
        <p style='font-size: 12px;'>Todos os dados são armazenados localmente em formato CSV</p>
    </div>
    """,
    unsafe_allow_html=True
)
