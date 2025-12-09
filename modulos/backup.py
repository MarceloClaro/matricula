"""
Módulo de Backup e Restauração de Dados
"""
import streamlit as st
import os
import tempfile
from datetime import datetime

def render_backup(data_manager):
    """Renderiza interface de backup e restauração"""
    st.title("💾 Backup e Restauração de Dados")
    st.markdown("---")
    
    st.markdown("""
    ### 📦 Sistema de Backup e Restauração
    
    Use esta funcionalidade para:
    - **Criar backups** de todos os dados do sistema
    - **Restaurar dados** a partir de backups anteriores
    - **Gerenciar backups** existentes
    
    ⚠️ **Importante**: Sempre crie um backup antes de fazer alterações importantes!
    """)
    
    st.markdown("---")
    
    # Três abas principais
    tab1, tab2, tab3 = st.tabs(["📥 Criar Backup", "📤 Restaurar Backup", "📋 Gerenciar Backups"])
    
    # ABA 1: Criar Backup
    with tab1:
        st.subheader("📥 Criar Novo Backup")
        
        st.info("""
        O backup incluirá todos os arquivos CSV com os dados:
        - Cadastro Geral
        - PEI (Plano Educacional Individualizado)
        - Socioeconômico
        - Questionário SAEB/SPAECE
        - Saúde
        - Anamnese Pedagógica
        """)
        
        # Estatísticas dos dados atuais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            df_cadastro = data_manager.get_data('cadastro')
            st.metric("Total de Alunos", len(df_cadastro))
        
        with col2:
            df_pei = data_manager.get_data('pei')
            st.metric("Registros PEI", len(df_pei))
        
        with col3:
            df_saude = data_manager.get_data('saude')
            st.metric("Registros Saúde", len(df_saude))
        
        st.markdown("---")
        
        # Botão para criar backup
        if st.button("🔽 Criar Backup Agora", type="primary", use_container_width=True):
            with st.spinner("Criando backup..."):
                try:
                    backup_path = data_manager.create_backup()
                    
                    # Verifica se o arquivo foi criado
                    if os.path.exists(backup_path):
                        file_size = os.path.getsize(backup_path) / 1024  # KB
                        
                        st.success(f"✅ Backup criado com sucesso!")
                        st.info(f"""
                        **Arquivo:** `{os.path.basename(backup_path)}`  
                        **Tamanho:** {file_size:.2f} KB  
                        **Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                        """)
                        
                        # Botão para download
                        with open(backup_path, 'rb') as f:
                            backup_data = f.read()
                            st.download_button(
                                label="⬇️ Baixar Backup",
                                data=backup_data,
                                file_name=os.path.basename(backup_path),
                                mime="application/zip",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Erro: Arquivo de backup não foi criado.")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao criar backup: {str(e)}")
    
    # ABA 2: Restaurar Backup
    with tab2:
        st.subheader("📤 Restaurar Dados de Backup")
        
        st.warning("""
        ⚠️ **ATENÇÃO**: A restauração substituirá TODOS os dados atuais!
        
        Antes de restaurar:
        1. Certifique-se de ter um backup dos dados atuais
        2. Verifique que o arquivo de backup está correto
        3. Confirme a operação
        """)
        
        st.markdown("---")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Selecione o arquivo de backup (ZIP)",
            type=['zip'],
            help="Faça upload de um arquivo de backup criado anteriormente. Limite recomendado: 200MB"
        )
        
        if uploaded_file is not None:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            st.success(f"📁 Arquivo selecionado: **{uploaded_file.name}**")
            st.info(f"Tamanho: {file_size_mb:.2f} MB")
            
            # Aviso para arquivos grandes
            if file_size_mb > 100:
                st.warning("⚠️ Arquivo grande detectado. A restauração pode demorar alguns minutos.")
            
            st.markdown("---")
            
            # Checkbox de confirmação
            confirmar = st.checkbox(
                "⚠️ Confirmo que desejo restaurar este backup e substituir os dados atuais",
                value=False
            )
            
            if confirmar:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("🔄 Restaurar Backup", type="primary", use_container_width=True):
                        with st.spinner("Restaurando backup... Aguarde..."):
                            temp_path = None
                            try:
                                # Salva arquivo temporariamente de forma segura
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                                    tmp_file.write(uploaded_file.getbuffer())
                                    temp_path = tmp_file.name
                                
                                # Restaura o backup
                                sucesso, mensagem = data_manager.restore_backup(temp_path)
                                
                                if sucesso:
                                    st.success(f"✅ {mensagem}")
                                    st.balloons()
                                    st.info("🔄 Recarregue a página (F5) para ver os dados restaurados.")
                                else:
                                    st.error(f"❌ {mensagem}")
                                    
                            except Exception as e:
                                st.error(f"❌ Erro ao restaurar backup: {str(e)}")
                            finally:
                                # Remove arquivo temporário sempre, mesmo se houver erro
                                if temp_path and os.path.exists(temp_path):
                                    try:
                                        os.remove(temp_path)
                                    except:
                                        pass  # Ignora erros ao remover arquivo temporário
                
                with col2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.rerun()
    
    # ABA 3: Gerenciar Backups
    with tab3:
        st.subheader("📋 Backups Disponíveis")
        
        # Lista backups existentes
        backups = data_manager.list_backups()
        
        if len(backups) == 0:
            st.info("📭 Nenhum backup encontrado. Crie seu primeiro backup na aba 'Criar Backup'.")
        else:
            st.success(f"📦 {len(backups)} backup(s) encontrado(s)")
            st.markdown("---")
            
            for idx, backup in enumerate(backups):
                with st.expander(f"📁 {backup['filename']}", expanded=(idx == 0)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **Data de Criação:** {backup['date']}  
                        **Tamanho:** {backup['size'] / 1024:.2f} KB  
                        **Arquivo:** `{backup['filename']}`
                        """)
                    
                    with col2:
                        # Botão de download
                        try:
                            with open(backup['filepath'], 'rb') as f:
                                backup_data = f.read()
                                st.download_button(
                                    label="⬇️ Baixar",
                                    data=backup_data,
                                    file_name=backup['filename'],
                                    mime="application/zip",
                                    key=f"download_{idx}",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                        
                        # Botão de exclusão
                        if st.button("🗑️ Excluir", key=f"delete_{idx}", use_container_width=True):
                            try:
                                os.remove(backup['filepath'])
                                st.success("Backup excluído!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir: {str(e)}")
    
    st.markdown("---")
    
    # Dicas
    with st.expander("💡 Dicas de Backup"):
        st.markdown("""
        ### Boas Práticas de Backup
        
        1. **Frequência**: Crie backups regularmente (diário, semanal ou mensal)
        2. **Armazenamento**: Mantenha cópias em locais seguros (nuvem, HD externo)
        3. **Verificação**: Teste a restauração de backups periodicamente
        4. **Nomenclatura**: Os backups incluem data e hora para fácil identificação
        5. **Limpeza**: Remova backups antigos para economizar espaço
        
        ### O que está incluído no backup?
        
        - ✅ Todos os dados de cadastro dos alunos
        - ✅ Informações do PEI
        - ✅ Dados socioeconômicos
        - ✅ Questionários SAEB/SPAECE
        - ✅ Fichas de saúde
        - ✅ Anamneses pedagógicas
        
        ### Quando criar um backup?
        
        - Antes de fazer grandes alterações nos dados
        - Após adicionar muitos registros novos
        - Antes de atualizar o sistema
        - Periodicamente como rotina de segurança
        """)
