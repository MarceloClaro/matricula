"""
Módulo de Frequência de Aula
Permite marcar presença usando reconhecimento facial
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from .reconhecimento_facial import FaceRecognitionSystem

def render_frequencia_aula(data_manager):
    """
    Renderiza a interface de frequência de aula
    
    Args:
        data_manager: Instância do DataManager
    """
    st.header("✅ Frequência de Aula - Reconhecimento Facial")
    st.markdown("---")
    
    # Inicializar sistema de reconhecimento facial
    face_system = FaceRecognitionSystem(data_dir=data_manager.data_dir)
    
    # Verificar se reconhecimento facial está disponível
    if not face_system.available:
        st.error("""
        ❌ **Reconhecimento Facial não está disponível**
        
        As bibliotecas necessárias (opencv-python, face_recognition e dlib) não foram instaladas corretamente.
        
        **Para habilitar esta funcionalidade:**
        - Instale as dependências do sistema: `build-essential`, `cmake`, `libopenblas-dev`
        - Execute: `pip install opencv-python-headless dlib face-recognition`
        
        No Streamlit Cloud, certifique-se de que o arquivo `packages.txt` contém as dependências necessárias.
        """)
        return
    
    st.info("""
    ### 📋 Como funciona:
    1. Clique em 'Marcar Presença' 
    2. Posicione seu rosto na frente da câmera
    3. O sistema irá reconhecer automaticamente e marcar sua presença
    4. A presença será registrada com data, hora e nível de confiança
    
    **🔒 Segurança:** O sistema possui anti-spoofing para evitar fraudes com fotos.
    """)
    
    # Verificar se há alunos cadastrados
    if face_system.get_student_count() == 0:
        st.warning("""
        ⚠️ **Nenhum aluno cadastrado para reconhecimento facial.**
        
        Por favor, cadastre alunos primeiro no módulo **"Registro de Presença"**.
        """)
        return
    
    # Abas
    tab1, tab2, tab3 = st.tabs([
        "📸 Marcar Presença",
        "📋 Registros de Hoje",
        "📊 Histórico Completo"
    ])
    
    with tab1:
        render_marcar_presenca(data_manager, face_system)
    
    with tab2:
        render_registros_hoje(data_manager)
    
    with tab3:
        render_historico_completo(data_manager)

def render_marcar_presenca(data_manager, face_system):
    """Renderiza interface de marcar presença"""
    st.subheader("📸 Marcar Presença")
    
    st.markdown("""
    ### 📝 Instruções:
    1. Clique no botão abaixo para iniciar
    2. Posicione seu rosto centralizado na câmera
    3. Aguarde o reconhecimento automático
    4. Sua presença será registrada instantaneamente
    """)
    
    # Métricas do sistema
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Alunos Cadastrados", face_system.get_student_count())
    
    with col2:
        df_attendance = data_manager.get_data('attendance')
        hoje = datetime.now().strftime('%Y-%m-%d')
        presencas_hoje = len(df_attendance[df_attendance['data'] == hoje]) if len(df_attendance) > 0 else 0
        st.metric("Presenças Hoje", presencas_hoje)
    
    with col3:
        df_alunos = data_manager.get_data('cadastro')
        total_alunos = len(df_alunos[df_alunos['status'] == 'Ativo']) if len(df_alunos) > 0 else 0
        st.metric("Total Alunos Ativos", total_alunos)
    
    st.markdown("---")
    
    # Botão para marcar presença
    if st.button("🎥 Iniciar Reconhecimento Facial", type="primary", use_container_width=True):
        with st.spinner("Acessando câmera..."):
            attendance_data = face_system.mark_attendance_with_webcam(data_manager, timeout=30)
            
            if attendance_data:
                # Mostrar dados registrados
                st.success("✅ Presença registrada com sucesso!")
                
                aluno = data_manager.get_record('cadastro', attendance_data['aluno_id'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"""
                    **👤 Aluno:** {aluno['nome_completo']}
                    
                    **📅 Data:** {attendance_data['data']}
                    
                    **🕐 Hora:** {attendance_data['hora']}
                    """)
                
                with col2:
                    st.info(f"""
                    **✅ Status:** {attendance_data['verificado']}
                    
                    **📊 Confiança:** {attendance_data['confianca']}
                    
                    **🔒 Observações:** {attendance_data['observacoes']}
                    """)
                
                st.balloons()
            else:
                st.warning("⚠️ Nenhuma face reconhecida. Tente novamente.")

def render_registros_hoje(data_manager):
    """Renderiza registros de presença de hoje"""
    st.subheader("📋 Registros de Hoje")
    
    df_attendance = data_manager.get_data('attendance')
    
    if len(df_attendance) == 0:
        st.info("📝 Nenhum registro de presença ainda.")
        return
    
    # Filtrar registros de hoje
    hoje = datetime.now().strftime('%Y-%m-%d')
    df_hoje = df_attendance[df_attendance['data'] == hoje]
    
    if len(df_hoje) == 0:
        st.info("📝 Nenhum registro de presença hoje.")
        return
    
    # Buscar dados dos alunos
    df_alunos = data_manager.get_data('cadastro')
    
    # Criar lista de registros
    registros = []
    for _, registro in df_hoje.iterrows():
        aluno_id = int(registro['aluno_id'])
        aluno = data_manager.get_record('cadastro', aluno_id)
        
        if aluno:
            registros.append({
                'ID': aluno_id,
                'Nome': aluno['nome_completo'],
                'Ano Escolar': aluno['ano_escolar'],
                'Turno': aluno['turno'],
                'Hora': registro['hora'],
                'Tipo': registro['tipo'],
                'Verificado': registro['verificado'],
                'Confiança': registro['confianca']
            })
    
    if len(registros) > 0:
        df_registros = pd.DataFrame(registros)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Presenças Hoje", len(df_registros))
        with col2:
            df_alunos_ativos = df_alunos[df_alunos['status'] == 'Ativo']
            total_ativos = len(df_alunos_ativos) if len(df_alunos_ativos) > 0 else 1
            taxa_presenca = (len(df_registros) / total_ativos * 100)
            st.metric("Taxa de Presença", f"{taxa_presenca:.1f}%")
        with col3:
            st.metric("Alunos Faltantes", max(0, total_ativos - len(df_registros)))
        
        st.markdown("---")
        
        # Tabela de registros
        st.dataframe(df_registros, use_container_width=True)
        
        # Gráfico por turno
        if 'Turno' in df_registros.columns:
            st.markdown("### 📊 Distribuição por Turno")
            turno_counts = df_registros['Turno'].value_counts()
            st.bar_chart(turno_counts)
        
        # Opção de exportar
        st.markdown("---")
        if st.button("📥 Exportar Registros de Hoje (CSV)"):
            csv = df_registros.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"presencas_{hoje}.csv",
                mime="text/csv"
            )
    else:
        st.info("📝 Nenhum registro encontrado.")

def render_historico_completo(data_manager):
    """Renderiza histórico completo de presenças"""
    st.subheader("📊 Histórico Completo")
    
    df_attendance = data_manager.get_data('attendance')
    
    if len(df_attendance) == 0:
        st.info("📝 Nenhum registro de presença ainda.")
        return
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro de data
        data_inicio = st.date_input(
            "Data Início",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )
    
    with col2:
        data_fim = st.date_input(
            "Data Fim",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    with col3:
        # Filtro de aluno
        df_alunos = data_manager.get_data('cadastro')
        opcoes_alunos = ["Todos"] + [
            f"{row['id']} - {row['nome_completo']}"
            for _, row in df_alunos.iterrows()
        ]
        aluno_filtro = st.selectbox("Aluno", opcoes_alunos)
    
    # Aplicar filtros
    df_filtrado = df_attendance.copy()
    
    # Converter datas
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')
    
    df_filtrado = df_filtrado[
        (df_filtrado['data'] >= data_inicio_str) &
        (df_filtrado['data'] <= data_fim_str)
    ]
    
    # Filtro de aluno
    if aluno_filtro != "Todos":
        aluno_id = int(aluno_filtro.split(' - ')[0])
        df_filtrado = df_filtrado[df_filtrado['aluno_id'] == str(aluno_id)]
    
    if len(df_filtrado) == 0:
        st.info("📝 Nenhum registro encontrado para os filtros selecionados.")
        return
    
    # Buscar dados dos alunos
    registros = []
    for _, registro in df_filtrado.iterrows():
        aluno_id = int(registro['aluno_id'])
        aluno = data_manager.get_record('cadastro', aluno_id)
        
        if aluno:
            registros.append({
                'ID': aluno_id,
                'Nome': aluno['nome_completo'],
                'Ano Escolar': aluno['ano_escolar'],
                'Turno': aluno['turno'],
                'Data': registro['data'],
                'Hora': registro['hora'],
                'Tipo': registro['tipo'],
                'Verificado': registro['verificado'],
                'Confiança': registro['confianca']
            })
    
    if len(registros) > 0:
        df_registros = pd.DataFrame(registros)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Registros", len(df_registros))
        with col2:
            alunos_unicos = df_registros['Nome'].nunique()
            st.metric("Alunos Únicos", alunos_unicos)
        with col3:
            dias_unicos = df_registros['Data'].nunique()
            st.metric("Dias Letivos", dias_unicos)
        with col4:
            media_diaria = len(df_registros) / dias_unicos if dias_unicos > 0 else 0
            st.metric("Média Diária", f"{media_diaria:.1f}")
        
        st.markdown("---")
        
        # Tabela de registros
        st.dataframe(df_registros, use_container_width=True)
        
        # Gráficos
        st.markdown("### 📊 Análises")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Presenças por Data")
            presencas_por_data = df_registros.groupby('Data').size()
            st.line_chart(presencas_por_data)
        
        with col2:
            st.markdown("#### Presenças por Aluno (Top 10)")
            presencas_por_aluno = df_registros['Nome'].value_counts().head(10)
            st.bar_chart(presencas_por_aluno)
        
        # Opção de exportar
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exportar Filtrado (CSV)", use_container_width=True):
                csv = df_registros.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"historico_presencas_{data_inicio_str}_a_{data_fim_str}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📥 Exportar Completo (CSV)", use_container_width=True):
                # Exportar todos os registros
                todos_registros = []
                for _, registro in df_attendance.iterrows():
                    aluno_id = int(registro['aluno_id'])
                    aluno = data_manager.get_record('cadastro', aluno_id)
                    
                    if aluno:
                        todos_registros.append({
                            'ID': aluno_id,
                            'Nome': aluno['nome_completo'],
                            'Data': registro['data'],
                            'Hora': registro['hora'],
                            'Tipo': registro['tipo'],
                            'Verificado': registro['verificado'],
                            'Confiança': registro['confianca']
                        })
                
                df_todos = pd.DataFrame(todos_registros)
                csv = df_todos.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV Completo",
                    data=csv,
                    file_name=f"historico_presencas_completo.csv",
                    mime="text/csv"
                )
    else:
        st.info("📝 Nenhum registro encontrado.")
