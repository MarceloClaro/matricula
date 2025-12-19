"""
Módulo de Registro de Presença em Lote
Permite upload de foto da turma para identificação facial e registro automático de presença
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import numpy as np
import io
from .reconhecimento_facial import FaceRecognitionSystem

def render_registro_lote(data_manager):
    """
    Renderiza a interface de registro de presença em lote
    
    Args:
        data_manager: Instância do DataManager
    """
    st.header("📸👥 Registro de Presença em Lote - Foto da Turma")
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
    1. **Tire uma foto da turma** ou faça upload de uma imagem existente
    2. O sistema irá **detectar todas as faces** na imagem
    3. Cada face será **identificada automaticamente** comparando com os alunos cadastrados
    4. A presença será **registrada automaticamente** para todos os alunos identificados
    5. Você verá um **relatório detalhado** com quem foi identificado e o nível de confiança
    
    **💡 Dicas para melhor resultado:**
    - Use boa iluminação
    - Certifique-se de que todas as faces estão visíveis e não muito pequenas
    - Evite rostos muito distantes da câmera
    - Prefira fotos frontais (evite perfis)
    
    **🔒 Segurança:** Apenas alunos previamente cadastrados serão identificados.
    """)
    
    # Verificar se há alunos cadastrados
    if face_system.get_student_count() == 0:
        st.warning("""
        ⚠️ **Nenhum aluno cadastrado para reconhecimento facial.**
        
        Por favor, cadastre alunos primeiro no módulo **"Registro de Presença"**.
        """)
        return
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Alunos Cadastrados", face_system.get_student_count())
    
    with col2:
        df_attendance = data_manager.get_data('attendance')
        hoje = datetime.now().strftime('%Y-%m-%d')
        presencas_hoje = len(df_attendance[df_attendance['data'] == hoje]) if len(df_attendance) > 0 else 0
        st.metric("✅ Presenças Hoje", presencas_hoje)
    
    with col3:
        df_alunos = data_manager.get_data('cadastro')
        total_alunos = len(df_alunos[df_alunos['status'] == 'Ativo']) if len(df_alunos) > 0 else 0
        st.metric("📊 Total Alunos Ativos", total_alunos)
    
    st.markdown("---")
    
    # Upload de imagem
    st.subheader("📤 Upload da Foto da Turma")
    
    uploaded_file = st.file_uploader(
        "Escolha uma imagem da turma (JPG, JPEG, PNG)",
        type=['jpg', 'jpeg', 'png'],
        help="Faça upload de uma foto onde aparecem os alunos que você deseja registrar presença"
    )
    
    if uploaded_file is not None:
        # Processar imagem
        process_group_photo(data_manager, face_system, uploaded_file)
    else:
        st.info("👆 Faça upload de uma foto da turma para começar")

def process_group_photo(data_manager, face_system, uploaded_file):
    """
    Processa foto da turma e registra presença automaticamente
    
    Args:
        data_manager: Instância do DataManager
        face_system: Sistema de reconhecimento facial
        uploaded_file: Arquivo de imagem uploaded
    """
    try:
        # Carregar imagem
        image = Image.open(uploaded_file)
        
        # Converter para RGB se necessário
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Converter para numpy array (formato do OpenCV)
        img_array = np.array(image)
        
        # Exibir imagem original
        st.subheader("📷 Imagem Carregada")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(image, caption="Foto da Turma", use_container_width=True)
        
        with col2:
            st.info(f"""
            **Informações da Imagem:**
            - Dimensões: {image.size[0]} x {image.size[1]} pixels
            - Formato: {image.format if image.format else 'N/A'}
            - Modo: {image.mode}
            """)
        
        # Botão para processar
        if st.button("🔍 Processar e Registrar Presenças", type="primary", use_container_width=True):
            with st.spinner("🔎 Detectando e identificando faces..."):
                # Processar imagem
                results = detect_and_identify_faces(face_system, img_array, data_manager)
                
                if results is None:
                    st.error("❌ Erro ao processar a imagem. Tente novamente com outra foto.")
                    return
                
                # Exibir resultados
                display_results(data_manager, results, img_array)
                
    except Exception as e:
        st.error(f"❌ Erro ao processar imagem: {str(e)}")
        st.info("💡 Tente com outra imagem ou verifique se o arquivo está corrompido.")

def detect_and_identify_faces(face_system, img_array, data_manager):
    """
    Detecta e identifica todas as faces na imagem
    
    Args:
        face_system: Sistema de reconhecimento facial
        img_array: Imagem como numpy array
        data_manager: Instância do DataManager
    
    Returns:
        dict: Resultados da identificação
    """
    try:
        import cv2
        import face_recognition
        
        # Converter BGR para RGB se necessário
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            rgb_frame = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        else:
            rgb_frame = img_array
        
        # Detectar faces na imagem
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        
        if len(face_locations) == 0:
            st.warning("⚠️ Nenhuma face detectada na imagem. Tente com outra foto onde as faces estejam mais visíveis.")
            return None
        
        st.success(f"✅ {len(face_locations)} face(s) detectada(s) na imagem!")
        
        # Extrair encodings de todas as faces
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Identificar cada face
        identifications = []
        for idx, (face_encoding, face_location) in enumerate(zip(face_encodings, face_locations)):
            # Calcular distâncias para todas as faces conhecidas
            if len(face_system.known_face_encodings) == 0:
                identifications.append({
                    'face_number': idx + 1,
                    'face_location': face_location,
                    'identified': False,
                    'aluno_id': None,
                    'aluno_nome': None,
                    'confidence': 0,
                    'reason': 'Nenhum aluno cadastrado'
                })
                continue
            
            face_distances = face_recognition.face_distance(face_system.known_face_encodings, face_encoding)
            
            # Agrupar por aluno_id e calcular distância média
            aluno_distances = {}
            for aluno_id, distance in zip(face_system.known_face_ids, face_distances):
                if aluno_id not in aluno_distances:
                    aluno_distances[aluno_id] = []
                aluno_distances[aluno_id].append(distance)
            
            # Calcular média de distâncias por aluno
            aluno_avg_distances = {
                aluno_id: sum(distances) / len(distances)
                for aluno_id, distances in aluno_distances.items()
            }
            
            # Encontrar melhor match
            if aluno_avg_distances:
                best_aluno_id = min(aluno_avg_distances, key=aluno_avg_distances.get)
                best_distance = aluno_avg_distances[best_aluno_id]
                confidence = 1 - best_distance
                
                # Threshold para aceitar identificação
                threshold = 0.50
                
                if best_distance < threshold:
                    # Buscar nome do aluno
                    df_alunos = data_manager.get_data('cadastro')
                    aluno = df_alunos[df_alunos['id'] == best_aluno_id]
                    aluno_nome = aluno['nome_completo'].values[0] if len(aluno) > 0 else f"Aluno {best_aluno_id}"
                    
                    identifications.append({
                        'face_number': idx + 1,
                        'face_location': face_location,
                        'identified': True,
                        'aluno_id': best_aluno_id,
                        'aluno_nome': aluno_nome,
                        'confidence': confidence,
                        'distance': best_distance
                    })
                else:
                    identifications.append({
                        'face_number': idx + 1,
                        'face_location': face_location,
                        'identified': False,
                        'aluno_id': None,
                        'aluno_nome': None,
                        'confidence': confidence,
                        'reason': f'Confiança muito baixa ({confidence*100:.1f}%)'
                    })
            else:
                identifications.append({
                    'face_number': idx + 1,
                    'face_location': face_location,
                    'identified': False,
                    'aluno_id': None,
                    'aluno_nome': None,
                    'confidence': 0,
                    'reason': 'Sem match encontrado'
                })
        
        return {
            'total_faces': len(face_locations),
            'identifications': identifications,
            'image_shape': img_array.shape
        }
        
    except Exception as e:
        st.error(f"Erro na detecção: {str(e)}")
        return None

def display_results(data_manager, results, img_array):
    """
    Exibe resultados da identificação e registra presenças
    
    Args:
        data_manager: Instância do DataManager
        results: Resultados da identificação
        img_array: Imagem original
    """
    st.markdown("---")
    st.subheader("📊 Resultados da Identificação")
    
    # Contar identificados
    identified = [r for r in results['identifications'] if r['identified']]
    not_identified = [r for r in results['identifications'] if not r['identified']]
    
    # Métricas de resultado
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Faces Detectadas", results['total_faces'])
    
    with col2:
        st.metric("✅ Identificadas", len(identified), 
                 delta=f"{len(identified)/results['total_faces']*100:.0f}%" if results['total_faces'] > 0 else "0%")
    
    with col3:
        st.metric("❓ Não Identificadas", len(not_identified))
    
    # Imagem com anotações
    st.subheader("🖼️ Imagem com Detecções")
    annotated_image = draw_annotations(img_array.copy(), results['identifications'])
    st.image(annotated_image, caption="Faces Detectadas e Identificadas", use_container_width=True)
    
    # Lista de identificados
    if identified:
        st.subheader("✅ Alunos Identificados")
        
        # Criar DataFrame para exibição
        df_identified = pd.DataFrame([
            {
                'Face #': r['face_number'],
                'Nome': r['aluno_nome'],
                'ID': r['aluno_id'],
                'Confiança': f"{r['confidence']*100:.1f}%"
            }
            for r in identified
        ])
        
        st.dataframe(df_identified, use_container_width=True, hide_index=True)
        
        # Botão para registrar presenças
        if st.button("💾 Registrar Presenças", type="primary", use_container_width=True):
            register_batch_attendance(data_manager, identified)
    
    # Lista de não identificados
    if not_identified:
        with st.expander(f"❓ Faces Não Identificadas ({len(not_identified)})"):
            for r in not_identified:
                st.warning(f"**Face #{r['face_number']}**: {r.get('reason', 'Não identificada')}")

def draw_annotations(img_array, identifications):
    """
    Desenha retângulos e nomes nas faces identificadas
    
    Args:
        img_array: Imagem como numpy array
        identifications: Lista de identificações
    
    Returns:
        numpy array: Imagem anotada
    """
    try:
        import cv2
        
        for ident in identifications:
            top, right, bottom, left = ident['face_location']
            
            # Cor: Verde se identificado, Vermelho se não
            color = (0, 255, 0) if ident['identified'] else (255, 0, 0)
            
            # Desenhar retângulo
            cv2.rectangle(img_array, (left, top), (right, bottom), color, 3)
            
            # Preparar texto
            if ident['identified']:
                text = f"{ident['aluno_nome']}"
                confidence_text = f"{ident['confidence']*100:.0f}%"
            else:
                text = f"Face #{ident['face_number']}"
                confidence_text = "?"
            
            # Fundo para o texto
            cv2.rectangle(img_array, (left, bottom), (right, bottom + 60), color, -1)
            
            # Texto do nome
            cv2.putText(img_array, text, (left + 6, bottom + 25), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Texto da confiança
            cv2.putText(img_array, confidence_text, (left + 6, bottom + 50), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        
        return img_array
    except Exception as e:
        st.warning(f"Não foi possível anotar a imagem: {str(e)}")
        return img_array

def register_batch_attendance(data_manager, identified):
    """
    Registra presença em lote para todos os alunos identificados
    
    Args:
        data_manager: Instância do DataManager
        identified: Lista de alunos identificados
    """
    try:
        df_attendance = data_manager.get_data('attendance')
        
        hoje = datetime.now().strftime('%Y-%m-%d')
        agora = datetime.now().strftime('%H:%M:%S')
        
        registros_novos = 0
        registros_duplicados = 0
        
        for ident in identified:
            aluno_id = ident['aluno_id']
            
            # Verificar se já existe registro de presença hoje
            if len(df_attendance) > 0:
                ja_registrado = df_attendance[
                    (df_attendance['aluno_id'] == aluno_id) & 
                    (df_attendance['data'] == hoje)
                ]
                if len(ja_registrado) > 0:
                    registros_duplicados += 1
                    continue
            
            # Buscar dados do aluno
            df_alunos = data_manager.get_data('cadastro')
            aluno = df_alunos[df_alunos['id'] == aluno_id]
            
            if len(aluno) == 0:
                continue
            
            # Criar novo registro
            novo_id = df_attendance['id'].max() + 1 if len(df_attendance) > 0 else 1
            
            novo_registro = {
                'id': novo_id,
                'aluno_id': aluno_id,
                'nome_aluno': ident['aluno_nome'],
                'data': hoje,
                'hora': agora,
                'confianca': ident['confidence'],
                'liveness_score': 0,  # N/A para foto estática
                'confirmations': 1,
                'method': 'batch_upload'
            }
            
            # Adicionar ao DataFrame
            df_attendance = pd.concat([df_attendance, pd.DataFrame([novo_registro])], ignore_index=True)
            registros_novos += 1
        
        # Salvar dados
        data_manager.save_data('attendance', df_attendance)
        
        # Mensagem de sucesso
        st.success(f"""
        ✅ **Presenças Registradas com Sucesso!**
        
        - **{registros_novos}** nova(s) presença(s) registrada(s)
        - **{registros_duplicados}** aluno(s) já tinha(m) presença registrada hoje
        
        Data: {hoje} às {agora}
        """)
        
        # Mostrar detalhes
        if registros_novos > 0:
            st.balloons()
            
            with st.expander("📋 Ver Detalhes dos Registros"):
                for ident in identified:
                    if ident['aluno_id']:
                        st.write(f"✅ **{ident['aluno_nome']}** - Confiança: {ident['confidence']*100:.1f}%")
        
        if registros_duplicados > 0:
            st.info(f"ℹ️ {registros_duplicados} aluno(s) já tinha(m) presença registrada hoje e não foram duplicados.")
        
    except Exception as e:
        st.error(f"❌ Erro ao registrar presenças: {str(e)}")
        st.info("💡 Verifique os dados e tente novamente.")
