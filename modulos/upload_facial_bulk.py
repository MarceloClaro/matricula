"""
Módulo de Upload em Lote de Imagens Faciais
Permite upload de ZIP com subpastas nomeadas por aluno para treinamento em massa
"""
import streamlit as st
import pandas as pd
import os
import zipfile
import shutil
import tempfile
from datetime import datetime
from .reconhecimento_facial import FaceRecognitionSystem
import pickle

def render_upload_facial_bulk(data_manager):
    """
    Renderiza a interface de upload em lote de imagens faciais
    
    Args:
        data_manager: Instância do DataManager
    """
    st.header("📦 Upload em Lote de Imagens Faciais")
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
        """)
        return
    
    st.info("""
    ### 📋 Como funciona:
    1. **Prepare um arquivo ZIP** com a seguinte estrutura:
       ```
       faces.zip
       ├── Nome_Completo_Aluno1/
       │   ├── foto1.jpg
       │   ├── foto2.jpg
       │   └── ...
       ├── Nome_Completo_Aluno2/
       │   ├── foto1.jpg
       │   └── ...
       └── ...
       ```
    2. **Importante:** O nome de cada pasta deve corresponder **exatamente** ao nome completo do aluno cadastrado no sistema
    3. Faça upload do arquivo ZIP
    4. O sistema irá processar todas as imagens e treinar o modelo automaticamente
    5. Você poderá baixar o modelo treinado para reutilização futura
    
    **💡 Dicas:**
    - Inclua pelo menos 10-30 fotos por aluno para melhor precisão
    - Use fotos com boa iluminação e diferentes ângulos
    - Formatos suportados: JPG, JPEG, PNG
    """)
    
    # Abas
    tab1, tab2, tab3 = st.tabs([
        "📤 Upload de Imagens", 
        "💾 Gerenciar Modelo",
        "📊 Status do Sistema"
    ])
    
    with tab1:
        render_upload_tab(data_manager, face_system)
    
    with tab2:
        render_model_management_tab(data_manager, face_system)
    
    with tab3:
        render_status_tab(data_manager, face_system)

def render_upload_tab(data_manager, face_system):
    """Renderiza aba de upload de imagens"""
    st.subheader("📤 Upload de Imagens Faciais")
    
    # Buscar alunos cadastrados
    df_alunos = data_manager.get_data('cadastro')
    
    if len(df_alunos) == 0:
        st.warning("⚠️ Nenhum aluno cadastrado. Cadastre alunos primeiro no módulo 'Cadastro Geral'.")
        return
    
    # Criar mapa de nomes para IDs
    nome_to_id = {}
    for _, row in df_alunos.iterrows():
        nome_completo = str(row['nome_completo']).strip()
        nome_to_id[nome_completo] = int(row['id'])
    
    st.markdown("### Alunos Cadastrados no Sistema")
    st.info(f"Total de alunos: {len(df_alunos)}")
    
    with st.expander("Ver lista de nomes de alunos"):
        for nome in sorted(nome_to_id.keys()):
            st.text(f"• {nome}")
    
    st.markdown("---")
    st.markdown("### Upload do Arquivo ZIP")
    
    uploaded_file = st.file_uploader(
        "Selecione o arquivo ZIP com as imagens",
        type=['zip'],
        help="O arquivo deve conter pastas nomeadas com o nome completo de cada aluno"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Arquivo carregado: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
        
        if st.button("🚀 Processar e Treinar Modelo", type="primary"):
            process_bulk_upload(uploaded_file, nome_to_id, face_system, data_manager)

def process_bulk_upload(uploaded_file, nome_to_id, face_system, data_manager):
    """
    Processa o upload em lote e treina o modelo
    
    Args:
        uploaded_file: Arquivo ZIP enviado
        nome_to_id: Dicionário mapeando nomes para IDs
        face_system: Sistema de reconhecimento facial
        data_manager: DataManager
    """
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        st.info("📦 Extraindo arquivo ZIP...")
        
        # Salvar arquivo temporariamente
        zip_path = os.path.join(temp_dir, 'upload.zip')
        with open(zip_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Extrair ZIP
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Validar membros do ZIP para prevenir directory traversal (Zip Slip)
                for member in zip_ref.namelist():
                    # Normalizar caminho e verificar se está dentro do temp_dir
                    member_path = os.path.normpath(os.path.join(temp_dir, member))
                    if not member_path.startswith(os.path.normpath(temp_dir)):
                        st.error(f"❌ Arquivo ZIP contém caminho suspeito: {member}")
                        return
                
                # Extração segura
                zip_ref.extractall(temp_dir)
        except Exception as e:
            st.error(f"❌ Erro ao extrair ZIP: {str(e)}")
            return
        
        st.success("✅ Arquivo extraído com sucesso!")
        
        # Encontrar pastas de alunos
        st.info("🔍 Identificando alunos...")
        
        alunos_encontrados = {}
        alunos_nao_encontrados = []
        
        # Percorrer diretórios
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path) and item != '__MACOSX':
                # Tentar encontrar aluno pelo nome
                nome_pasta = item.strip()
                
                if nome_pasta in nome_to_id:
                    aluno_id = nome_to_id[nome_pasta]
                    # Contar imagens - formatos suportados
                    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
                    imagens = [f for f in os.listdir(item_path) 
                              if f.lower().endswith(SUPPORTED_FORMATS)]
                    
                    if len(imagens) > 0:
                        alunos_encontrados[aluno_id] = {
                            'nome': nome_pasta,
                            'pasta': item_path,
                            'num_imagens': len(imagens),
                            'imagens': [os.path.join(item_path, img) for img in imagens]
                        }
                else:
                    alunos_nao_encontrados.append(nome_pasta)
        
        # Mostrar resumo
        st.markdown("### 📊 Resumo da Análise")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Alunos Encontrados", len(alunos_encontrados))
        with col2:
            st.metric("❌ Pastas Não Reconhecidas", len(alunos_nao_encontrados))
        
        if len(alunos_encontrados) > 0:
            st.markdown("#### Alunos que serão processados:")
            for aluno_id, info in alunos_encontrados.items():
                st.success(f"• **{info['nome']}** (ID: {aluno_id}) - {info['num_imagens']} imagens")
        
        if len(alunos_nao_encontrados) > 0:
            with st.expander("⚠️ Pastas não reconhecidas (serão ignoradas)"):
                for nome in alunos_nao_encontrados:
                    st.warning(f"• {nome}")
                st.info("**Dica:** Certifique-se de que o nome da pasta corresponde exatamente ao nome completo cadastrado.")
        
        if len(alunos_encontrados) == 0:
            st.error("❌ Nenhum aluno foi reconhecido. Verifique os nomes das pastas.")
            return
        
        # Confirmar antes de treinar
        st.markdown("---")
        if st.button("✅ Confirmar e Iniciar Treinamento", type="primary"):
            treinar_modelo_bulk(alunos_encontrados, face_system, data_manager)

def treinar_modelo_bulk(alunos_encontrados, face_system, data_manager):
    """
    Treina o modelo com as imagens de múltiplos alunos
    
    Args:
        alunos_encontrados: Dicionário com informações dos alunos
        face_system: Sistema de reconhecimento facial
        data_manager: DataManager
    """
    st.markdown("---")
    st.header("🎓 Iniciando Treinamento")
    
    # Adicionar informação sobre tempo estimado
    total_alunos = len(alunos_encontrados)
    total_imagens = sum(info['num_imagens'] for info in alunos_encontrados.values())
    st.info(f"""
    📊 **Estimativa de processamento:**
    - Total de alunos: {total_alunos}
    - Total de imagens: {total_imagens}
    - Tempo estimado: {total_imagens * 2 // 60} - {total_imagens * 3 // 60} minutos
    
    ⏳ Por favor, aguarde. O treinamento será executado sequencialmente.
    """)
    
    progresso_geral = st.progress(0)
    status_geral = st.empty()
    
    resultados = {
        'sucesso': [],
        'falha': []
    }
    
    for idx, (aluno_id, info) in enumerate(alunos_encontrados.items()):
        status_geral.info(f"🔄 Processando {idx + 1}/{total_alunos}: {info['nome']}")
        
        st.markdown(f"### Aluno: {info['nome']}")
        
        # Treinar com as imagens deste aluno
        sucesso = face_system.train_face_recognition(aluno_id, info['imagens'])
        
        if sucesso:
            resultados['sucesso'].append(info['nome'])
            st.success(f"✅ {info['nome']} treinado com sucesso!")
        else:
            resultados['falha'].append(info['nome'])
            st.error(f"❌ Falha ao treinar {info['nome']}")
        
        # Atualizar progresso
        progresso_geral.progress((idx + 1) / total_alunos)
    
    # Resumo final
    progresso_geral.empty()
    status_geral.empty()
    
    st.markdown("---")
    st.header("🎉 Treinamento Concluído!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Sucessos", len(resultados['sucesso']))
    with col2:
        st.metric("❌ Falhas", len(resultados['falha']))
    
    if len(resultados['sucesso']) > 0:
        with st.expander("✅ Alunos treinados com sucesso"):
            for nome in resultados['sucesso']:
                st.success(f"• {nome}")
    
    if len(resultados['falha']) > 0:
        with st.expander("❌ Alunos com falha no treinamento"):
            for nome in resultados['falha']:
                st.error(f"• {nome}")
    
    st.success("🎓 Modelo atualizado e pronto para uso!")
    st.info("💡 Você pode baixar o modelo treinado na aba 'Gerenciar Modelo'")

def render_model_management_tab(data_manager, face_system):
    """Renderiza aba de gerenciamento do modelo"""
    st.subheader("💾 Gerenciar Modelo")
    
    st.markdown("### 📥 Exportar Modelo Treinado")
    st.info("Exporte o modelo atual para reutilização futura ou backup.")
    
    # Verificar se há modelo treinado
    if len(face_system.known_face_encodings) == 0:
        st.warning("⚠️ Nenhum modelo treinado disponível para exportar.")
    else:
        st.success(f"✅ Modelo atual contém {len(set(face_system.known_face_ids))} alunos treinados")
        st.info(f"Total de encodings: {len(face_system.known_face_encodings)}")
        
        if st.button("📥 Baixar Modelo Treinado"):
            export_model(face_system)
    
    st.markdown("---")
    st.markdown("### 📤 Importar Modelo Treinado")
    st.info("Importe um modelo previamente exportado para evitar retreinamento.")
    
    uploaded_model = st.file_uploader(
        "Selecione o arquivo do modelo (.pkl)",
        type=['pkl'],
        help="Arquivo de modelo exportado anteriormente"
    )
    
    if uploaded_model is not None:
        st.success(f"✅ Arquivo carregado: {uploaded_model.name}")
        
        if st.button("📤 Importar e Substituir Modelo Atual", type="primary"):
            import_model(uploaded_model, face_system)

def export_model(face_system):
    """
    Exporta o modelo treinado
    
    Args:
        face_system: Sistema de reconhecimento facial
    """
    try:
        # Criar arquivo pickle em memória
        data = {
            'encodings': face_system.known_face_encodings,
            'ids': face_system.known_face_ids,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0'
        }
        
        # Serializar
        model_bytes = pickle.dumps(data)
        
        # Nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'modelo_facial_{timestamp}.pkl'
        
        # Botão de download
        st.download_button(
            label="💾 Download do Modelo",
            data=model_bytes,
            file_name=filename,
            mime='application/octet-stream'
        )
        
        st.success(f"""
        ✅ **Modelo pronto para download!**
        
        📊 **Informações do modelo:**
        - Alunos: {len(set(face_system.known_face_ids))}
        - Encodings: {len(face_system.known_face_encodings)}
        - Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        💡 Guarde este arquivo em local seguro para backup
        """)
        
    except Exception as e:
        st.error(f"❌ Erro ao exportar modelo: {str(e)}")

def import_model(uploaded_model, face_system):
    """
    Importa um modelo treinado
    
    Args:
        uploaded_model: Arquivo do modelo
        face_system: Sistema de reconhecimento facial
    """
    try:
        # Carregar dados - NOTA: pickle pode ser inseguro com fontes não confiáveis
        # Considere usar apenas modelos de fontes confiáveis
        model_bytes = uploaded_model.read()
        
        # Validação básica de tamanho
        if len(model_bytes) > 100 * 1024 * 1024:  # 100MB limite
            st.error("❌ Arquivo muito grande. Tamanho máximo: 100MB")
            return
        
        # Tentar carregar com validação
        try:
            data = pickle.loads(model_bytes)
        except (pickle.UnpicklingError, EOFError) as e:
            st.error(f"❌ Arquivo de modelo inválido ou corrompido: {str(e)}")
            return
        
        # Validar estrutura e tipos
        if not isinstance(data, dict):
            st.error("❌ Estrutura de modelo inválida!")
            return
            
        if 'encodings' not in data or 'ids' not in data:
            st.error("❌ Arquivo de modelo inválido - campos obrigatórios faltando!")
            return
        
        # Validar tipos
        if not isinstance(data['encodings'], list) or not isinstance(data['ids'], list):
            st.error("❌ Tipos de dados inválidos no modelo!")
            return
        
        if len(data['encodings']) != len(data['ids']):
            st.error("❌ Inconsistência nos dados do modelo!")
            return
        
        # Mostrar informações
        num_alunos = len(set(data['ids']))
        num_encodings = len(data['encodings'])
        timestamp = data.get('timestamp', 'Desconhecido')
        
        st.info(f"""
        📊 **Informações do modelo importado:**
        - Alunos: {num_alunos}
        - Encodings: {num_encodings}
        - Data de criação: {timestamp}
        """)
        
        # Confirmar substituição
        if st.button("⚠️ CONFIRMAR: Substituir modelo atual", type="secondary"):
            # Fazer backup do modelo atual
            if len(face_system.known_face_encodings) > 0:
                try:
                    # Salvar modelo atual primeiro
                    face_system.save_embeddings()
                    
                    # Criar backup se o arquivo existe
                    if os.path.exists(face_system.embeddings_path):
                        backup_path = face_system.embeddings_path + '.backup'
                        shutil.copy2(face_system.embeddings_path, backup_path)
                        st.info(f"💾 Backup do modelo atual salvo em: {backup_path}")
                except Exception as e:
                    st.warning(f"⚠️ Não foi possível criar backup: {str(e)}")
            
            # Substituir modelo
            face_system.known_face_encodings = data['encodings']
            face_system.known_face_ids = data['ids']
            face_system.save_embeddings()
            
            st.success("""
            ✅ **Modelo importado com sucesso!**
            
            O sistema agora está usando o modelo importado.
            Você pode verificar o status na aba 'Status do Sistema'.
            """)
            
            st.balloons()
            
    except Exception as e:
        st.error(f"❌ Erro ao importar modelo: {str(e)}")

def render_status_tab(data_manager, face_system):
    """Renderiza aba de status do sistema"""
    st.subheader("📊 Status do Sistema")
    
    # Estatísticas do modelo
    st.markdown("### 🎓 Modelo de Reconhecimento Facial")
    
    if len(face_system.known_face_encodings) == 0:
        st.warning("⚠️ Nenhum modelo treinado")
    else:
        alunos_treinados = set(face_system.known_face_ids)
        num_alunos = len(alunos_treinados)
        num_encodings = len(face_system.known_face_encodings)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Alunos Treinados", num_alunos)
        with col2:
            st.metric("🧠 Total de Encodings", num_encodings)
        with col3:
            avg_encodings = num_encodings / num_alunos if num_alunos > 0 else 0
            st.metric("📊 Média por Aluno", f"{avg_encodings:.1f}")
        
        # Detalhes por aluno
        st.markdown("---")
        st.markdown("### 📋 Detalhes por Aluno")
        
        # Contar encodings por aluno
        aluno_counts = {}
        for aluno_id in face_system.known_face_ids:
            aluno_counts[aluno_id] = aluno_counts.get(aluno_id, 0) + 1
        
        # Buscar nomes dos alunos
        df_alunos = data_manager.get_data('cadastro')
        
        status_data = []
        for aluno_id, count in sorted(aluno_counts.items()):
            aluno = df_alunos[df_alunos['id'] == aluno_id]
            if len(aluno) > 0:
                nome = aluno.iloc[0]['nome_completo']
            else:
                nome = f"Aluno ID {aluno_id} (não encontrado)"
            
            status_data.append({
                'ID': aluno_id,
                'Nome': nome,
                'Encodings': count,
                'Status': '✅ Bom' if count >= 20 else '⚠️ Melhorar' if count >= 10 else '❌ Insuficiente'
            })
        
        df_status = pd.DataFrame(status_data)
        st.dataframe(df_status, use_container_width=True, hide_index=True)
        
        # Recomendações
        st.markdown("---")
        st.markdown("### 💡 Recomendações")
        
        alunos_insuficientes = [s for s in status_data if s['Encodings'] < 10]
        if len(alunos_insuficientes) > 0:
            st.warning(f"""
            ⚠️ **{len(alunos_insuficientes)} aluno(s) com encodings insuficientes**
            
            Para melhor precisão, recomendamos pelo menos 10-30 encodings por aluno.
            Considere recapturar fotos destes alunos.
            """)
        else:
            st.success("✅ Todos os alunos têm quantidade adequada de encodings!")
    
    # Informações do sistema
    st.markdown("---")
    st.markdown("### ⚙️ Informações do Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **Diretórios:**
        - Dados: `{face_system.data_dir}`
        - Faces: `{face_system.faces_dir}`
        - Modelos: `{face_system.models_dir}`
        """)
    
    with col2:
        st.info(f"""
        **Status das bibliotecas:**
        - Face Recognition: {'✅ Disponível' if face_system.available else '❌ Não disponível'}
        - OpenCV: {'✅ Disponível' if face_system.available else '❌ Não disponível'}
        """)
