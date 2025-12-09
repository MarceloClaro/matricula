"""
Módulo Socioeconômico
"""
import streamlit as st
import pandas as pd

def render_socioeconomico(data_manager):
    """Renderiza formulário socioeconômico"""
    st.header("💰 Questionário Socioeconômico")
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
        st.info("Selecione um aluno para preencher o questionário socioeconômico")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    
    # Verificar se já existe cadastro para este aluno
    df_socio = data_manager.get_data('socioeconomico')
    socio_existente = df_socio[df_socio['aluno_id'] == aluno_id]
    
    if len(socio_existente) > 0:
        st.info("ℹ️ Este aluno já possui questionário socioeconômico cadastrado. Você pode editá-lo abaixo.")
        socio_atual = socio_existente.iloc[0].to_dict()
    else:
        socio_atual = {}
    
    with st.form("form_socioeconomico"):
        st.subheader("Renda Familiar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            renda_familiar = st.selectbox(
                "Renda Familiar Mensal *",
                ["", "Até 1 salário mínimo", "De 1 a 2 salários mínimos", 
                 "De 2 a 3 salários mínimos", "De 3 a 5 salários mínimos",
                 "De 5 a 10 salários mínimos", "Acima de 10 salários mínimos"],
                index=0 if not socio_atual.get('renda_familiar') else 
                ["", "Até 1 salário mínimo", "De 1 a 2 salários mínimos", 
                 "De 2 a 3 salários mínimos", "De 3 a 5 salários mínimos",
                 "De 5 a 10 salários mínimos", "Acima de 10 salários mínimos"].index(socio_atual.get('renda_familiar', ''))
            )
        
        with col2:
            qtd_pessoas_casa = st.number_input(
                "Quantidade de pessoas na residência *",
                min_value=1,
                max_value=20,
                value=socio_atual.get('qtd_pessoas_casa', 1) if socio_atual.get('qtd_pessoas_casa') else 1
            )
        
        st.subheader("Moradia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_moradia = st.selectbox(
                "Tipo de Moradia *",
                ["", "Própria", "Alugada", "Cedida", "Financiada", "Outros"],
                index=0 if not socio_atual.get('tipo_moradia') else 
                ["", "Própria", "Alugada", "Cedida", "Financiada", "Outros"].index(socio_atual.get('tipo_moradia', ''))
            )
        
        with col2:
            pass
        
        st.subheader("Recursos Tecnológicos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            possui_internet = st.radio(
                "Possui Internet? *",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('possui_internet') == 'Sim' else 0)
            )
        
        with col2:
            possui_computador = st.radio(
                "Possui Computador? *",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('possui_computador') == 'Sim' else 0)
            )
        
        with col3:
            possui_smartphone = st.radio(
                "Possui Smartphone? *",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('possui_smartphone') == 'Sim' else 0)
            )
        
        st.subheader("Benefícios Sociais")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bolsa_familia = st.radio(
                "Bolsa Família?",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('bolsa_familia') == 'Sim' else 0)
            )
        
        with col2:
            auxilio_brasil = st.radio(
                "Auxílio Brasil?",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('auxilio_brasil') == 'Sim' else 0)
            )
        
        with col3:
            beneficio_social = st.radio(
                "Outro Benefício?",
                ["Não", "Sim"],
                index=0 if not socio_atual else (1 if socio_atual.get('beneficio_social') == 'Sim' else 0)
            )
        
        st.subheader("Dados do Responsável")
        
        col1, col2 = st.columns(2)
        
        with col1:
            situacao_trabalho = st.selectbox(
                "Situação de Trabalho do Responsável *",
                ["", "Empregado com carteira assinada", "Empregado sem carteira assinada",
                 "Funcionário público", "Autônomo", "Empresário", 
                 "Desempregado", "Aposentado", "Do lar", "Outros"],
                index=0 if not socio_atual.get('situacao_trabalho_responsavel') else
                ["", "Empregado com carteira assinada", "Empregado sem carteira assinada",
                 "Funcionário público", "Autônomo", "Empresário", 
                 "Desempregado", "Aposentado", "Do lar", "Outros"].index(socio_atual.get('situacao_trabalho_responsavel', ''))
            )
        
        with col2:
            profissao = st.text_input(
                "Profissão do Responsável",
                max_chars=100,
                value=socio_atual.get('profissao_responsavel', '')
            )
        
        st.subheader("Escolaridade dos Pais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            escolaridade_mae = st.selectbox(
                "Escolaridade da Mãe",
                ["", "Não alfabetizado", "Fundamental Incompleto", "Fundamental Completo",
                 "Médio Incompleto", "Médio Completo", "Superior Incompleto", 
                 "Superior Completo", "Pós-graduação"],
                index=0 if not socio_atual.get('escolaridade_mae') else
                ["", "Não alfabetizado", "Fundamental Incompleto", "Fundamental Completo",
                 "Médio Incompleto", "Médio Completo", "Superior Incompleto", 
                 "Superior Completo", "Pós-graduação"].index(socio_atual.get('escolaridade_mae', ''))
            )
        
        with col2:
            escolaridade_pai = st.selectbox(
                "Escolaridade do Pai",
                ["", "Não alfabetizado", "Fundamental Incompleto", "Fundamental Completo",
                 "Médio Incompleto", "Médio Completo", "Superior Incompleto", 
                 "Superior Completo", "Pós-graduação"],
                index=0 if not socio_atual.get('escolaridade_pai') else
                ["", "Não alfabetizado", "Fundamental Incompleto", "Fundamental Completo",
                 "Médio Incompleto", "Médio Completo", "Superior Incompleto", 
                 "Superior Completo", "Pós-graduação"].index(socio_atual.get('escolaridade_pai', ''))
            )
        
        st.subheader("Transporte Escolar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            transporte_escolar = st.selectbox(
                "Utiliza Transporte Escolar? *",
                ["", "Não", "Sim - Municipal", "Sim - Particular", "Sim - Público"],
                index=0 if not socio_atual.get('transporte_escolar') else
                ["", "Não", "Sim - Municipal", "Sim - Particular", "Sim - Público"].index(socio_atual.get('transporte_escolar', ''))
            )
        
        with col2:
            tempo_deslocamento = st.selectbox(
                "Tempo de Deslocamento até a Escola",
                ["", "Até 15 minutos", "De 15 a 30 minutos", "De 30 a 60 minutos",
                 "De 1 a 2 horas", "Acima de 2 horas"],
                index=0 if not socio_atual.get('tempo_deslocamento') else
                ["", "Até 15 minutos", "De 15 a 30 minutos", "De 30 a 60 minutos",
                 "De 1 a 2 horas", "Acima de 2 horas"].index(socio_atual.get('tempo_deslocamento', ''))
            )
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Questionário", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not renda_familiar:
                erros.append("Renda familiar é obrigatória")
            if not tipo_moradia:
                erros.append("Tipo de moradia é obrigatório")
            if not situacao_trabalho:
                erros.append("Situação de trabalho é obrigatória")
            if not transporte_escolar:
                erros.append("Informação sobre transporte escolar é obrigatória")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                dados = {
                    'aluno_id': aluno_id,
                    'renda_familiar': renda_familiar,
                    'qtd_pessoas_casa': qtd_pessoas_casa,
                    'tipo_moradia': tipo_moradia,
                    'possui_internet': possui_internet,
                    'possui_computador': possui_computador,
                    'possui_smartphone': possui_smartphone,
                    'bolsa_familia': bolsa_familia,
                    'auxilio_brasil': auxilio_brasil,
                    'beneficio_social': beneficio_social,
                    'situacao_trabalho_responsavel': situacao_trabalho,
                    'profissao_responsavel': profissao,
                    'escolaridade_mae': escolaridade_mae,
                    'escolaridade_pai': escolaridade_pai,
                    'transporte_escolar': transporte_escolar,
                    'tempo_deslocamento': tempo_deslocamento
                }
                
                try:
                    if len(socio_existente) > 0:
                        # Atualizar existente
                        data_manager.update_record('socioeconomico', socio_existente.iloc[0]['id'], dados)
                        st.success("✅ Questionário socioeconômico atualizado com sucesso!")
                    else:
                        # Criar novo
                        data_manager.add_record('socioeconomico', dados)
                        st.success("✅ Questionário socioeconômico cadastrado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar questionário: {str(e)}")
