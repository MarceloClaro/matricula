"""
Módulo de Saúde
"""
import streamlit as st
import pandas as pd

def render_saude(data_manager):
    """Renderiza formulário de saúde"""
    st.header("🏥 Ficha de Saúde")
    st.markdown("---")
    
    # Selecionar aluno
    df_alunos = data_manager.get_data('cadastro')
    
    if len(df_alunos) == 0:
        st.warning("⚠️ Não há alunos cadastrados. Cadastre um aluno primeiro.")
        return
    
    # Criar lista de alunos
    alunos_opcoes = ["Selecione um aluno"] + [
        f"{row['id']} - {row['nome_completo']}" 
        for _, row in df_alunos.iterrows()
    ]
    
    aluno_selecionado = st.selectbox("Aluno *", alunos_opcoes)
    
    if aluno_selecionado == "Selecione um aluno":
        st.info("Selecione um aluno para preencher a ficha de saúde")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    
    # Verificar se já existe ficha para este aluno
    df_saude = data_manager.get_data('saude')
    saude_existente = df_saude[df_saude['aluno_id'] == aluno_id]
    
    if len(saude_existente) > 0:
        st.info("ℹ️ Este aluno já possui ficha de saúde cadastrada. Você pode editá-la abaixo.")
        saude_atual = saude_existente.iloc[0].to_dict()
    else:
        saude_atual = {}
    
    with st.form("form_saude"):
        st.subheader("Tipo Sanguíneo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_sanguineo = st.selectbox(
                "Tipo Sanguíneo *",
                ["", "A", "B", "AB", "O", "Não informado"],
                index=0 if not saude_atual.get('tipo_sanguineo') else
                ["", "A", "B", "AB", "O", "Não informado"].index(saude_atual.get('tipo_sanguineo', ''))
            )
        
        with col2:
            fator_rh = st.selectbox(
                "Fator RH *",
                ["", "Positivo", "Negativo", "Não informado"],
                index=0 if not saude_atual.get('fator_rh') else
                ["", "Positivo", "Negativo", "Não informado"].index(saude_atual.get('fator_rh', ''))
            )
        
        st.subheader("Condições de Saúde")
        
        alergias = st.text_area(
            "Alergias",
            height=100,
            value=saude_atual.get('alergias', ''),
            help="Descreva alergias alimentares, medicamentosas, etc."
        )
        
        doencas_cronicas = st.text_area(
            "Doenças Crônicas",
            height=100,
            value=saude_atual.get('doencas_cronicas', ''),
            help="Diabetes, asma, epilepsia, etc."
        )
        
        medicamentos_uso_continuo = st.text_area(
            "Medicamentos de Uso Contínuo",
            height=100,
            value=saude_atual.get('medicamentos_uso_continuo', ''),
            help="Liste medicamentos, dosagens e horários"
        )
        
        historico_doencas = st.text_area(
            "Histórico de Doenças",
            height=100,
            value=saude_atual.get('historico_doencas', ''),
            help="Doenças anteriores relevantes, cirurgias, internações"
        )
        
        st.subheader("Vacinação")
        
        vacinacao_em_dia = st.radio(
            "Vacinação em dia? *",
            ["Sim", "Não", "Não informado"],
            index=0 if not saude_atual else 
            ["Sim", "Não", "Não informado"].index(saude_atual.get('vacinacao_em_dia', 'Sim'))
        )
        
        st.subheader("Plano de Saúde")
        
        col1, col2 = st.columns(2)
        
        with col1:
            plano_saude = st.radio(
                "Possui Plano de Saúde?",
                ["Não", "Sim"],
                index=0 if not saude_atual else (1 if saude_atual.get('plano_saude') == 'Sim' else 0)
            )
        
        with col2:
            if plano_saude == "Sim":
                nome_plano_saude = st.text_input(
                    "Nome do Plano",
                    max_chars=100,
                    value=saude_atual.get('nome_plano_saude', '')
                )
            else:
                nome_plano_saude = ""
        
        if plano_saude == "Sim":
            numero_plano = st.text_input(
                "Número da Carteirinha",
                max_chars=50,
                value=saude_atual.get('numero_plano', '')
            )
        else:
            numero_plano = ""
        
        st.subheader("Contato de Emergência")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            contato_emergencia = st.text_input(
                "Nome do Contato *",
                max_chars=100,
                value=saude_atual.get('contato_emergencia', '')
            )
        
        with col2:
            telefone_emergencia = st.text_input(
                "Telefone *",
                max_chars=20,
                value=saude_atual.get('telefone_emergencia', ''),
                placeholder="(00) 00000-0000"
            )
        
        with col3:
            parentesco_emergencia = st.selectbox(
                "Parentesco *",
                ["", "Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Irmão/Irmã", "Outros"],
                index=0 if not saude_atual.get('parentesco_emergencia') else
                ["", "Pai", "Mãe", "Avô/Avó", "Tio/Tia", "Irmão/Irmã", "Outros"].index(saude_atual.get('parentesco_emergencia', ''))
            )
        
        st.subheader("Observações Adicionais")
        
        observacoes_saude = st.text_area(
            "Informações Complementares",
            height=150,
            value=saude_atual.get('observacoes_saude', ''),
            help="Qualquer informação adicional relevante sobre a saúde do aluno"
        )
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Ficha de Saúde", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not tipo_sanguineo:
                erros.append("Tipo sanguíneo é obrigatório")
            if not fator_rh:
                erros.append("Fator RH é obrigatório")
            if not contato_emergencia:
                erros.append("Nome do contato de emergência é obrigatório")
            if not telefone_emergencia:
                erros.append("Telefone de emergência é obrigatório")
            if not parentesco_emergencia:
                erros.append("Parentesco do contato de emergência é obrigatório")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                dados = {
                    'aluno_id': aluno_id,
                    'tipo_sanguineo': tipo_sanguineo,
                    'fator_rh': fator_rh,
                    'alergias': alergias,
                    'doencas_cronicas': doencas_cronicas,
                    'medicamentos_uso_continuo': medicamentos_uso_continuo,
                    'historico_doencas': historico_doencas,
                    'vacinacao_em_dia': vacinacao_em_dia,
                    'plano_saude': plano_saude,
                    'nome_plano_saude': nome_plano_saude,
                    'numero_plano': numero_plano,
                    'contato_emergencia': contato_emergencia,
                    'telefone_emergencia': telefone_emergencia,
                    'parentesco_emergencia': parentesco_emergencia,
                    'observacoes_saude': observacoes_saude
                }
                
                try:
                    if len(saude_existente) > 0:
                        # Atualizar existente
                        data_manager.update_record('saude', saude_existente.iloc[0]['id'], dados)
                        st.success("✅ Ficha de saúde atualizada com sucesso!")
                    else:
                        # Criar novo
                        data_manager.add_record('saude', dados)
                        st.success("✅ Ficha de saúde cadastrada com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar ficha de saúde: {str(e)}")
