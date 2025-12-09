"""
Módulo PEI - Plano Educacional Individualizado
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def render_pei(data_manager):
    """Renderiza formulário PEI"""
    st.header("♿ PEI - Plano Educacional Individualizado")
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
        st.info("Selecione um aluno para preencher o PEI")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    
    # Verificar se já existe PEI para este aluno
    df_pei = data_manager.get_data('pei')
    pei_existente = df_pei[df_pei['aluno_id'] == aluno_id]
    
    if len(pei_existente) > 0:
        st.info("ℹ️ Este aluno já possui um PEI cadastrado. Você pode editá-lo abaixo.")
        pei_atual = pei_existente.iloc[0].to_dict()
    else:
        pei_atual = {}
    
    with st.form("form_pei"):
        st.subheader("Necessidades Especiais")
        
        necessidade_especial = st.radio(
            "Possui necessidade especial? *",
            ["Não", "Sim"],
            index=0 if not pei_atual else (1 if pei_atual.get('necessidade_especial') == 'Sim' else 0)
        )
        
        if necessidade_especial == "Sim":
            tipo_deficiencia = st.multiselect(
                "Tipo de Deficiência *",
                ["Deficiência Física", "Deficiência Visual", "Deficiência Auditiva", 
                 "Deficiência Intelectual", "Transtorno do Espectro Autista (TEA)", 
                 "Deficiência Múltipla", "Altas Habilidades/Superdotação", "Outros"],
                default=pei_atual.get('tipo_deficiencia', '').split(', ') if pei_atual.get('tipo_deficiencia') else []
            )
            
            st.subheader("Laudo Médico")
            col1, col2 = st.columns(2)
            
            with col1:
                laudo_medico = st.radio(
                    "Possui Laudo Médico? *",
                    ["Não", "Sim"],
                    index=0 if not pei_atual else (1 if pei_atual.get('laudo_medico') == 'Sim' else 0)
                )
            
            with col2:
                if laudo_medico == "Sim":
                    data_laudo = st.date_input(
                        "Data do Laudo",
                        value=datetime.strptime(pei_atual.get('data_laudo', ''), '%Y-%m-%d') 
                        if pei_atual.get('data_laudo') else datetime.now()
                    )
                else:
                    data_laudo = None
            
            cid = st.text_input("CID (se aplicável)", 
                               max_chars=50,
                               value=pei_atual.get('cid', ''))
            
            st.subheader("Informações Clínicas")
            
            medicacao = st.text_area(
                "Medicação em uso",
                height=100,
                value=pei_atual.get('medicacao', ''),
                help="Descreva medicações e dosagens"
            )
            
            restricoes = st.text_area(
                "Restrições e Contraindicações",
                height=100,
                value=pei_atual.get('restricoes', ''),
                help="Atividades ou situações que devem ser evitadas"
            )
            
            st.subheader("Apoio Pedagógico")
            
            apoio_necessario = st.multiselect(
                "Tipo de Apoio Necessário",
                ["Sala de Recursos Multifuncionais", "Professor de Apoio", 
                 "Intérprete de Libras", "Cuidador", "Tutor", 
                 "Tecnologias Assistivas", "Outros"],
                default=pei_atual.get('apoio_necessario', '').split(', ') if pei_atual.get('apoio_necessario') else []
            )
            
            adaptacao_curricular = st.text_area(
                "Adaptações Curriculares Necessárias",
                height=150,
                value=pei_atual.get('adaptacao_curricular', ''),
                help="Descreva as adaptações necessárias no currículo"
            )
            
            acompanhamento_especializado = st.text_area(
                "Acompanhamento Especializado",
                height=100,
                value=pei_atual.get('acompanhamento_especializado', ''),
                help="Ex: Fonoaudiologia, Psicologia, Terapia Ocupacional"
            )
            
            recursos_necessarios = st.text_area(
                "Recursos e Materiais Necessários",
                height=100,
                value=pei_atual.get('recursos_necessarios', ''),
                help="Equipamentos, materiais adaptados, etc."
            )
            
            observacoes = st.text_area(
                "Observações Adicionais",
                height=150,
                value=pei_atual.get('observacoes', '')
            )
        else:
            tipo_deficiencia = []
            laudo_medico = "Não"
            data_laudo = None
            cid = ""
            medicacao = ""
            restricoes = ""
            apoio_necessario = []
            adaptacao_curricular = ""
            acompanhamento_especializado = ""
            recursos_necessarios = ""
            observacoes = ""
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar PEI", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if necessidade_especial == "Sim":
                if not tipo_deficiencia:
                    erros.append("Tipo de deficiência é obrigatório")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                dados = {
                    'aluno_id': aluno_id,
                    'necessidade_especial': necessidade_especial,
                    'tipo_deficiencia': ', '.join(tipo_deficiencia) if tipo_deficiencia else '',
                    'laudo_medico': laudo_medico,
                    'data_laudo': data_laudo.strftime('%Y-%m-%d') if data_laudo else '',
                    'cid': cid,
                    'medicacao': medicacao,
                    'restricoes': restricoes,
                    'apoio_necessario': ', '.join(apoio_necessario) if apoio_necessario else '',
                    'adaptacao_curricular': adaptacao_curricular,
                    'acompanhamento_especializado': acompanhamento_especializado,
                    'recursos_necessarios': recursos_necessarios,
                    'observacoes': observacoes
                }
                
                try:
                    if len(pei_existente) > 0:
                        # Atualizar existente
                        data_manager.update_record('pei', pei_existente.iloc[0]['id'], dados)
                        st.success("✅ PEI atualizado com sucesso!")
                    else:
                        # Criar novo
                        data_manager.add_record('pei', dados)
                        st.success("✅ PEI cadastrado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar PEI: {str(e)}")
