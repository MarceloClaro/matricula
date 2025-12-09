"""
Módulo CRUD - Gerenciamento de Registros
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def render_crud(data_manager):
    """Renderiza interface CRUD"""
    st.header("⚙️ Gerenciamento de Registros (CRUD)")
    st.markdown("---")
    
    # Selecionar tipo de registro
    tipo_registro = st.selectbox(
        "Selecione o tipo de registro",
        ["Cadastro Geral", "PEI", "Socioeconômico", "Saúde"]
    )
    
    tipo_map = {
        "Cadastro Geral": "cadastro",
        "PEI": "pei",
        "Socioeconômico": "socioeconomico",
        "Saúde": "saude"
    }
    
    tipo = tipo_map[tipo_registro]
    
    st.markdown("---")
    
    # Tabs para operações CRUD
    tab_listar, tab_editar, tab_deletar = st.tabs(["📋 Listar", "✏️ Editar", "🗑️ Deletar"])
    
    with tab_listar:
        render_listar(data_manager, tipo, tipo_registro)
    
    with tab_editar:
        render_editar(data_manager, tipo, tipo_registro)
    
    with tab_deletar:
        render_deletar(data_manager, tipo, tipo_registro)

def render_listar(data_manager, tipo, tipo_registro):
    """Lista todos os registros"""
    st.subheader(f"Lista de {tipo_registro}")
    
    df = data_manager.get_data(tipo)
    
    if len(df) == 0:
        st.info(f"Nenhum registro de {tipo_registro} encontrado.")
        return
    
    # Opção de filtro
    if tipo == 'cadastro':
        col1, col2 = st.columns(2)
        with col1:
            filtro_status = st.selectbox("Filtrar por Status", 
                                        ["Todos"] + list(df['status'].unique()))
        with col2:
            filtro_ano = st.selectbox("Filtrar por Ano", 
                                     ["Todos"] + list(df['ano_escolar'].unique()))
        
        if filtro_status != "Todos":
            df = df[df['status'] == filtro_status]
        if filtro_ano != "Todos":
            df = df[df['ano_escolar'] == filtro_ano]
    
    # Mostrar quantidade
    st.markdown(f"**Total de registros:** {len(df)}")
    
    # Mostrar dados
    st.dataframe(df, use_container_width=True, height=400)
    
    # Opção de exportar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar para CSV",
        data=csv,
        file_name=f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

def render_editar(data_manager, tipo, tipo_registro):
    """Edita um registro existente"""
    st.subheader(f"Editar {tipo_registro}")
    
    df = data_manager.get_data(tipo)
    
    if len(df) == 0:
        st.info(f"Nenhum registro de {tipo_registro} encontrado.")
        return
    
    # Selecionar registro
    if tipo == 'cadastro':
        opcoes = [f"{row['id']} - {row['nome_completo']}" for _, row in df.iterrows()]
    else:
        # Para outros tipos, buscar nome do aluno
        df_alunos = data_manager.get_data('cadastro')
        opcoes = []
        for _, row in df.iterrows():
            if tipo in ['pei', 'socioeconomico', 'saude'] and 'aluno_id' in row:
                aluno = df_alunos[df_alunos['id'] == row['aluno_id']]
                if len(aluno) > 0:
                    nome_aluno = aluno.iloc[0]['nome_completo']
                    opcoes.append(f"{row['id']} - {nome_aluno}")
                else:
                    opcoes.append(f"{row['id']} - Aluno não encontrado")
            else:
                opcoes.append(f"ID: {row['id']}")
    
    registro_selecionado = st.selectbox("Selecione o registro", ["Selecione..."] + opcoes)
    
    if registro_selecionado == "Selecione...":
        st.info("Selecione um registro para editar")
        return
    
    registro_id = int(registro_selecionado.split(" - ")[0])
    registro = data_manager.get_record(tipo, registro_id)
    
    if not registro:
        st.error("Registro não encontrado")
        return
    
    st.markdown("---")
    
    # Formulário de edição simplificado
    with st.form("form_editar"):
        st.write("**Campos principais para edição:**")
        
        campos_editados = {}
        
        if tipo == 'cadastro':
            campos_editados['nome_completo'] = st.text_input(
                "Nome Completo", value=registro.get('nome_completo', '')
            )
            campos_editados['telefone'] = st.text_input(
                "Telefone", value=registro.get('telefone', '')
            )
            campos_editados['email'] = st.text_input(
                "E-mail", value=registro.get('email', '')
            )
            campos_editados['ano_escolar'] = st.selectbox(
                "Ano Escolar",
                ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                 "6º Ano", "7º Ano", "8º Ano", "9º Ano"],
                index=["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                       "6º Ano", "7º Ano", "8º Ano", "9º Ano"].index(registro.get('ano_escolar', '1º Ano'))
            )
            campos_editados['turno'] = st.selectbox(
                "Turno",
                ["Matutino", "Vespertino", "Integral"],
                index=["Matutino", "Vespertino", "Integral"].index(registro.get('turno', 'Matutino'))
            )
            campos_editados['status'] = st.selectbox(
                "Status",
                ["Ativo", "Aguardando Documentação", "Cancelado"],
                index=["Ativo", "Aguardando Documentação", "Cancelado"].index(registro.get('status', 'Ativo'))
            )
        
        elif tipo == 'pei':
            campos_editados['necessidade_especial'] = st.radio(
                "Possui necessidade especial?",
                ["Não", "Sim"],
                index=1 if registro.get('necessidade_especial') == 'Sim' else 0
            )
            campos_editados['observacoes'] = st.text_area(
                "Observações",
                value=registro.get('observacoes', ''),
                height=150
            )
        
        elif tipo == 'socioeconomico':
            campos_editados['renda_familiar'] = st.selectbox(
                "Renda Familiar",
                ["Até 1 salário mínimo", "De 1 a 2 salários mínimos", 
                 "De 2 a 3 salários mínimos", "De 3 a 5 salários mínimos",
                 "De 5 a 10 salários mínimos", "Acima de 10 salários mínimos"],
                index=["Até 1 salário mínimo", "De 1 a 2 salários mínimos", 
                       "De 2 a 3 salários mínimos", "De 3 a 5 salários mínimos",
                       "De 5 a 10 salários mínimos", "Acima de 10 salários mínimos"].index(
                           registro.get('renda_familiar', 'Até 1 salário mínimo'))
            )
            campos_editados['possui_internet'] = st.radio(
                "Possui Internet?",
                ["Não", "Sim"],
                index=1 if registro.get('possui_internet') == 'Sim' else 0
            )
        
        elif tipo == 'saude':
            campos_editados['tipo_sanguineo'] = st.selectbox(
                "Tipo Sanguíneo",
                ["A", "B", "AB", "O", "Não informado"],
                index=["A", "B", "AB", "O", "Não informado"].index(
                    registro.get('tipo_sanguineo', 'Não informado'))
            )
            campos_editados['contato_emergencia'] = st.text_input(
                "Contato de Emergência",
                value=registro.get('contato_emergencia', '')
            )
            campos_editados['telefone_emergencia'] = st.text_input(
                "Telefone de Emergência",
                value=registro.get('telefone_emergencia', '')
            )
        
        submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
        
        if submitted:
            try:
                data_manager.update_record(tipo, registro_id, campos_editados)
                st.success("✅ Registro atualizado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Erro ao atualizar registro: {str(e)}")

def render_deletar(data_manager, tipo, tipo_registro):
    """Deleta um registro"""
    st.subheader(f"Deletar {tipo_registro}")
    
    st.warning("⚠️ **Atenção:** Esta operação não pode ser desfeita!")
    
    df = data_manager.get_data(tipo)
    
    if len(df) == 0:
        st.info(f"Nenhum registro de {tipo_registro} encontrado.")
        return
    
    # Selecionar registro
    if tipo == 'cadastro':
        opcoes = [f"{row['id']} - {row['nome_completo']}" for _, row in df.iterrows()]
    else:
        # Para outros tipos, buscar nome do aluno
        df_alunos = data_manager.get_data('cadastro')
        opcoes = []
        for _, row in df.iterrows():
            if tipo in ['pei', 'socioeconomico', 'saude'] and 'aluno_id' in row:
                aluno = df_alunos[df_alunos['id'] == row['aluno_id']]
                if len(aluno) > 0:
                    nome_aluno = aluno.iloc[0]['nome_completo']
                    opcoes.append(f"{row['id']} - {nome_aluno}")
                else:
                    opcoes.append(f"{row['id']} - Aluno não encontrado")
            else:
                opcoes.append(f"ID: {row['id']}")
    
    registro_selecionado = st.selectbox("Selecione o registro", ["Selecione..."] + opcoes)
    
    if registro_selecionado == "Selecione...":
        st.info("Selecione um registro para deletar")
        return
    
    registro_id = int(registro_selecionado.split(" - ")[0])
    
    # Confirmação
    st.markdown("---")
    confirmar = st.checkbox("Confirmo que desejo deletar este registro")
    
    if st.button("🗑️ Deletar Registro", use_container_width=True, disabled=not confirmar):
        try:
            data_manager.delete_record(tipo, registro_id)
            st.success("✅ Registro deletado com sucesso!")
            # Add small delay for user to see success message
            import time
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erro ao deletar registro: {str(e)}")
