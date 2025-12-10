"""
Módulo de Registro de Presença
Permite registrar alunos com captura de fotos via webcam para reconhecimento facial
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from .reconhecimento_facial import FaceRecognitionSystem

def render_registro_presenca(data_manager):
    """
    Renderiza a interface de registro de presença
    
    Args:
        data_manager: Instância do DataManager
    """
    st.header("📸 Registro de Presença - Cadastro Facial")
    st.markdown("---")
    
    st.info("""
    ### 📋 Como funciona:
    1. Selecione um aluno já cadastrado no sistema
    2. Clique em 'Iniciar Captura' para tirar 30 fotos em 10 segundos
    3. O sistema irá processar as fotos e treinar o reconhecimento facial
    4. O aluno poderá marcar presença usando o reconhecimento facial
    
    **💡 Dica:** Mantenha o rosto centralizado e bem iluminado durante a captura.
    """)
    
    # Inicializar sistema de reconhecimento facial
    face_system = FaceRecognitionSystem(data_dir=data_manager.data_dir)
    
    # Abas
    tab1, tab2, tab3 = st.tabs([
        "📷 Novo Cadastro Facial", 
        "📋 Alunos Registrados",
        "🔄 Re-treinar Modelo"
    ])
    
    with tab1:
        render_novo_cadastro_facial(data_manager, face_system)
    
    with tab2:
        render_lista_registrados(data_manager, face_system)
    
    with tab3:
        render_retreinar_modelo(data_manager, face_system)

def render_novo_cadastro_facial(data_manager, face_system):
    """Renderiza formulário de novo cadastro facial"""
    st.subheader("📷 Novo Cadastro Facial")
    
    # Buscar alunos cadastrados
    df_alunos = data_manager.get_data('cadastro')
    
    if len(df_alunos) == 0:
        st.warning("⚠️ Nenhum aluno cadastrado. Cadastre alunos primeiro no módulo 'Cadastro Geral'.")
        return
    
    # Filtrar apenas alunos ativos
    df_alunos_ativos = df_alunos[df_alunos['status'] == 'Ativo']
    
    if len(df_alunos_ativos) == 0:
        st.warning("⚠️ Nenhum aluno ativo cadastrado.")
        return
    
    # Criar lista de opções
    opcoes_alunos = [
        f"{row['id']} - {row['nome_completo']} ({row['ano_escolar']} - {row['turno']})"
        for _, row in df_alunos_ativos.iterrows()
    ]
    
    # Selecionar aluno
    st.markdown("### Selecione o Aluno")
    aluno_selecionado = st.selectbox(
        "Aluno",
        options=opcoes_alunos,
        help="Selecione o aluno para cadastrar reconhecimento facial"
    )
    
    if aluno_selecionado:
        # Extrair ID do aluno
        aluno_id = int(aluno_selecionado.split(' - ')[0])
        aluno = data_manager.get_record('cadastro', aluno_id)
        
        # Mostrar dados do aluno
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nome", aluno['nome_completo'])
        with col2:
            st.metric("Ano Escolar", aluno['ano_escolar'])
        with col3:
            st.metric("Turno", aluno['turno'])
        
        st.markdown("---")
        
        # Verificar se aluno já tem cadastro facial
        df_embeddings = data_manager.get_data('face_embeddings')
        aluno_ja_cadastrado = False
        
        if len(df_embeddings) > 0:
            embeddings_aluno = df_embeddings[df_embeddings['aluno_id'] == str(aluno_id)]
            if len(embeddings_aluno) > 0:
                aluno_ja_cadastrado = True
                st.warning(f"⚠️ Este aluno já possui cadastro facial registrado em {embeddings_aluno.iloc[0]['data_cadastro']}")
                
                if st.checkbox("Desejo atualizar o cadastro facial"):
                    aluno_ja_cadastrado = False
        
        if not aluno_ja_cadastrado:
            st.markdown("### 📸 Captura de Fotos")
            st.info("""
            **Instruções:**
            - Posicione-se em frente à webcam
            - Mantenha boa iluminação
            - O sistema capturará 30 fotos em 10 segundos
            - Varie levemente a posição da cabeça durante a captura
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                num_photos = st.number_input("Número de fotos", min_value=20, max_value=50, value=30)
            with col2:
                duration = st.number_input("Duração (segundos)", min_value=5, max_value=30, value=10)
            
            if st.button("🎥 Iniciar Captura de Fotos", type="primary", use_container_width=True):
                with st.spinner("Preparando webcam..."):
                    # Capturar sequência de fotos
                    photo_paths = face_system.capture_photo_sequence(
                        aluno_id=aluno_id,
                        num_photos=num_photos,
                        duration=duration
                    )
                    
                    if len(photo_paths) > 0:
                        st.success(f"✅ {len(photo_paths)} fotos capturadas!")
                        
                        # Treinar reconhecimento facial
                        with st.spinner("Treinando modelo de reconhecimento facial..."):
                            success = face_system.train_face_recognition(aluno_id, photo_paths)
                            
                            if success:
                                # Salvar registro no banco
                                embedding_data = {
                                    'aluno_id': aluno_id,
                                    'embedding': 'trained',  # Placeholder
                                    'photo_path': photo_paths[0],  # Primeira foto
                                    'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                                data_manager.add_record('face_embeddings', embedding_data)
                                
                                st.success(f"""
                                ✅ **Cadastro facial concluído com sucesso!**
                                
                                - Aluno: {aluno['nome_completo']}
                                - Fotos capturadas: {len(photo_paths)}
                                - Modelo treinado: Sim
                                
                                O aluno já pode marcar presença usando reconhecimento facial!
                                """)
                                
                                st.balloons()
                            else:
                                st.error("❌ Erro ao treinar modelo. Tente novamente.")
                    else:
                        st.error("❌ Nenhuma foto foi capturada. Verifique a webcam.")

def render_lista_registrados(data_manager, face_system):
    """Renderiza lista de alunos com cadastro facial"""
    st.subheader("📋 Alunos com Cadastro Facial")
    
    df_embeddings = data_manager.get_data('face_embeddings')
    
    if len(df_embeddings) == 0:
        st.info("📝 Nenhum aluno com cadastro facial ainda.")
        return
    
    # Buscar dados dos alunos
    df_alunos = data_manager.get_data('cadastro')
    
    # Criar lista de alunos registrados
    alunos_registrados = []
    for _, embedding in df_embeddings.iterrows():
        aluno_id = int(embedding['aluno_id'])
        aluno = data_manager.get_record('cadastro', aluno_id)
        
        if aluno:
            alunos_registrados.append({
                'ID': aluno_id,
                'Nome': aluno['nome_completo'],
                'Ano Escolar': aluno['ano_escolar'],
                'Turno': aluno['turno'],
                'Data Cadastro': embedding['data_cadastro']
            })
    
    if len(alunos_registrados) > 0:
        df_registrados = pd.DataFrame(alunos_registrados)
        
        st.metric("Total de Alunos Registrados", len(df_registrados))
        st.dataframe(df_registrados, use_container_width=True)
        
        # Estatísticas
        st.markdown("### 📊 Estatísticas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_alunos = len(data_manager.get_data('cadastro'))
            porcentagem = (len(df_registrados) / total_alunos * 100) if total_alunos > 0 else 0
            st.metric("% de Cobertura", f"{porcentagem:.1f}%")
        
        with col2:
            model_count = face_system.get_student_count()
            st.metric("Modelos Treinados", model_count)
        
        with col3:
            st.metric("Total Cadastros", len(df_alunos))
    else:
        st.info("📝 Nenhum aluno encontrado.")

def render_retreinar_modelo(data_manager, face_system):
    """Renderiza interface de re-treinamento do modelo"""
    st.subheader("🔄 Re-treinar Modelo")
    
    st.warning("""
    ### ⚠️ Re-treinamento do Modelo
    
    Esta opção irá re-treinar o modelo de reconhecimento facial com todos os alunos cadastrados.
    
    **Quando usar:**
    - Após cadastrar vários alunos novos
    - Se o reconhecimento não estiver funcionando bem
    - Para melhorar a precisão do sistema
    
    **Nota:** Este processo pode demorar alguns minutos dependendo do número de alunos.
    """)
    
    df_embeddings = data_manager.get_data('face_embeddings')
    
    if len(df_embeddings) == 0:
        st.info("📝 Nenhum aluno cadastrado para re-treinar.")
        return
    
    st.metric("Alunos a processar", len(df_embeddings))
    
    if st.button("🔄 Iniciar Re-treinamento", type="primary", use_container_width=True):
        with st.spinner("Re-treinando modelo..."):
            # Limpar encodings atuais
            face_system.known_face_encodings = []
            face_system.known_face_ids = []
            
            progress_bar = st.progress(0)
            success_count = 0
            
            for idx, embedding in df_embeddings.iterrows():
                aluno_id = int(embedding['aluno_id'])
                
                # Buscar fotos do aluno
                import os
                aluno_dir = os.path.join(face_system.faces_dir, f'aluno_{aluno_id}')
                
                if os.path.exists(aluno_dir):
                    photo_paths = [
                        os.path.join(aluno_dir, f) 
                        for f in os.listdir(aluno_dir) 
                        if f.endswith('.jpg')
                    ]
                    
                    if len(photo_paths) > 0:
                        # Re-treinar para este aluno
                        encodings = face_system.extract_face_encodings(photo_paths, aluno_id)
                        
                        if len(encodings) > 0:
                            face_system.known_face_encodings.extend(encodings)
                            face_system.known_face_ids.extend([aluno_id] * len(encodings))
                            success_count += 1
                
                progress_bar.progress((idx + 1) / len(df_embeddings))
            
            # Salvar embeddings atualizados
            face_system.save_embeddings()
            
            progress_bar.empty()
            st.success(f"""
            ✅ **Re-treinamento concluído!**
            
            - Alunos processados: {success_count}/{len(df_embeddings)}
            - Total de encodings: {len(face_system.known_face_encodings)}
            """)
            st.balloons()
