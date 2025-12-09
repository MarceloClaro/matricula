"""
Módulo Questionário SAEB/SPAECE do Aluno
"""
import streamlit as st
import pandas as pd

def render_questionario_saeb(data_manager):
    """Renderiza questionário SAEB/SPAECE do aluno"""
    st.header("📋 Questionário SAEB/SPAECE do Aluno")
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
        st.info("Selecione um aluno para preencher o questionário SAEB/SPAECE")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    
    # Verificar se já existe cadastro para este aluno
    df_saeb = data_manager.get_data('questionario_saeb')
    saeb_existente = df_saeb[df_saeb['aluno_id'] == aluno_id]
    
    if len(saeb_existente) > 0:
        st.info("ℹ️ Este aluno já possui questionário SAEB cadastrado. Você pode editá-lo abaixo.")
        saeb_atual = saeb_existente.iloc[0].to_dict()
    else:
        saeb_atual = {}
    
    with st.form("form_questionario_saeb"):
        # Seção 2: Informações Pessoais
        st.subheader("2. Informações Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sexo = st.selectbox(
                "2.1 Sexo *",
                ["", "Masculino", "Feminino", "Não quero declarar"],
                index=0 if not saeb_atual.get('sexo') else 
                ["", "Masculino", "Feminino", "Não quero declarar"].index(saeb_atual.get('sexo', ''))
            )
            
            lingua_familia = st.selectbox(
                "2.3 Língua falada pela família *",
                ["", "Português", "Espanhol", "Libras / Línguas de sinais", "Outra língua"],
                index=0 if not saeb_atual.get('lingua_familia') else 
                ["", "Português", "Espanhol", "Libras / Línguas de sinais", "Outra língua"].index(saeb_atual.get('lingua_familia', ''))
            )
        
        with col2:
            idade = st.selectbox(
                "2.2 Idade *",
                ["", "13 anos ou menos", "14 anos", "15 anos", "16 anos", "17 anos", "18 anos ou mais"],
                index=0 if not saeb_atual.get('idade') else 
                ["", "13 anos ou menos", "14 anos", "15 anos", "16 anos", "17 anos", "18 anos ou mais"].index(saeb_atual.get('idade', ''))
            )
            
            cor_raca = st.selectbox(
                "2.4 Cor ou raça *",
                ["", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Não quero declarar"],
                index=0 if not saeb_atual.get('cor_raca') else 
                ["", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Não quero declarar"].index(saeb_atual.get('cor_raca', ''))
            )
        
        # Seção 3: Informações de Inclusão
        st.subheader("3. Informações de Inclusão")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            deficiencia = st.radio(
                "Possui deficiência? *",
                ["Não", "Sim"],
                index=0 if not saeb_atual else (1 if saeb_atual.get('deficiencia') == 'Sim' else 0)
            )
        
        with col2:
            tea = st.radio(
                "Transtorno do espectro autista (TEA)? *",
                ["Não", "Sim"],
                index=0 if not saeb_atual else (1 if saeb_atual.get('tea') == 'Sim' else 0)
            )
        
        with col3:
            altas_habilidades = st.radio(
                "Altas habilidades / superdotação? *",
                ["Não", "Sim"],
                index=0 if not saeb_atual else (1 if saeb_atual.get('altas_habilidades') == 'Sim' else 0)
            )
        
        # Seção 4: Composição Familiar
        st.subheader("4. Composição Familiar e Escolaridade dos Responsáveis")
        
        st.markdown("**4.1 Quem mora com o aluno**")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            mora_mae = st.checkbox("Mãe(s) ou madrasta(s)", 
                                   value=saeb_atual.get('mora_mae') == 'Sim' if saeb_atual else False)
        
        with col2:
            mora_pai = st.checkbox("Pai(s) ou padrasto(s)", 
                                   value=saeb_atual.get('mora_pai') == 'Sim' if saeb_atual else False)
        
        with col3:
            mora_avo = st.checkbox("Avó(s)", 
                                   value=saeb_atual.get('mora_avo') == 'Sim' if saeb_atual else False)
        
        with col4:
            mora_avoh = st.checkbox("Avô(s)", 
                                    value=saeb_atual.get('mora_avoh') == 'Sim' if saeb_atual else False)
        
        with col5:
            mora_outros = st.checkbox("Outros familiares", 
                                      value=saeb_atual.get('mora_outros') == 'Sim' if saeb_atual else False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            escolaridade_mae = st.selectbox(
                "4.2 Escolaridade da mãe / responsável mulher *",
                ["", "Não completou 4ª/5º ano", "Fundamental incompleto", "Fundamental completo",
                 "Médio completo", "Superior completo", "Não sei"],
                index=0 if not saeb_atual.get('escolaridade_mae') else 
                ["", "Não completou 4ª/5º ano", "Fundamental incompleto", "Fundamental completo",
                 "Médio completo", "Superior completo", "Não sei"].index(saeb_atual.get('escolaridade_mae', ''))
            )
        
        with col2:
            escolaridade_pai = st.selectbox(
                "4.3 Escolaridade do pai / responsável homem *",
                ["", "Não completou 4ª/5º ano", "Fundamental incompleto", "Fundamental completo",
                 "Médio completo", "Superior completo", "Não sei"],
                index=0 if not saeb_atual.get('escolaridade_pai') else 
                ["", "Não completou 4ª/5º ano", "Fundamental incompleto", "Fundamental completo",
                 "Médio completo", "Superior completo", "Não sei"].index(saeb_atual.get('escolaridade_pai', ''))
            )
        
        # Seção 5: Rotina Familiar
        st.subheader("5. Rotina Familiar e Apoio dos Responsáveis")
        st.markdown("**Frequência com que os responsáveis:**")
        
        freq_opcoes = ["Nunca / quase nunca", "De vez em quando", "Sempre / quase sempre"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            responsavel_le = st.selectbox(
                "Leem com o aluno",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_le', freq_opcoes[0])) if saeb_atual.get('responsavel_le') in freq_opcoes else 0
            )
            
            responsavel_conversa = st.selectbox(
                "Conversam sobre a escola",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_conversa', freq_opcoes[0])) if saeb_atual.get('responsavel_conversa') in freq_opcoes else 0
            )
            
            responsavel_incentiva_estudar = st.selectbox(
                "Incentivam a estudar",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_incentiva_estudar', freq_opcoes[0])) if saeb_atual.get('responsavel_incentiva_estudar') in freq_opcoes else 0
            )
        
        with col2:
            responsavel_incentiva_tarefas = st.selectbox(
                "Incentivam tarefas de casa",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_incentiva_tarefas', freq_opcoes[0])) if saeb_atual.get('responsavel_incentiva_tarefas') in freq_opcoes else 0
            )
            
            responsavel_incentiva_aulas = st.selectbox(
                "Incentivam a assistir aulas",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_incentiva_aulas', freq_opcoes[0])) if saeb_atual.get('responsavel_incentiva_aulas') in freq_opcoes else 0
            )
            
            responsavel_participa_reunioes = st.selectbox(
                "Participam de reuniões",
                freq_opcoes,
                index=freq_opcoes.index(saeb_atual.get('responsavel_participa_reunioes', freq_opcoes[0])) if saeb_atual.get('responsavel_participa_reunioes') in freq_opcoes else 0
            )
        
        # Seção 6: Condições do Bairro
        st.subheader("6. Condições do bairro onde mora")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bairro_asfalto = st.checkbox("Asfalto / calçamento", 
                                         value=saeb_atual.get('bairro_asfalto') == 'Sim' if saeb_atual else False)
        
        with col2:
            bairro_agua_tratada = st.checkbox("Água tratada", 
                                              value=saeb_atual.get('bairro_agua_tratada') == 'Sim' if saeb_atual else False)
        
        with col3:
            bairro_iluminacao = st.checkbox("Iluminação pública", 
                                            value=saeb_atual.get('bairro_iluminacao') == 'Sim' if saeb_atual else False)
        
        # Seção 7: Condições da Casa
        st.subheader("7. Condições da casa e bens")
        st.markdown("**Quantos existem em sua casa:**")
        
        qtd_opcoes = ["Nenhum", "1", "2", "3 ou mais"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            qtd_geladeira = st.selectbox(
                "Geladeira",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_geladeira', qtd_opcoes[0])) if saeb_atual.get('qtd_geladeira') in qtd_opcoes else 0
            )
            
            qtd_computador = st.selectbox(
                "Computador / notebook",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_computador', qtd_opcoes[0])) if saeb_atual.get('qtd_computador') in qtd_opcoes else 0
            )
        
        with col2:
            qtd_quartos = st.selectbox(
                "Quartos para dormir",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_quartos', qtd_opcoes[0])) if saeb_atual.get('qtd_quartos') in qtd_opcoes else 0
            )
            
            qtd_televisao = st.selectbox(
                "Televisão",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_televisao', qtd_opcoes[0])) if saeb_atual.get('qtd_televisao') in qtd_opcoes else 0
            )
        
        with col3:
            qtd_banheiro = st.selectbox(
                "Banheiro",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_banheiro', qtd_opcoes[0])) if saeb_atual.get('qtd_banheiro') in qtd_opcoes else 0
            )
            
            qtd_carro = st.selectbox(
                "Carro",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_carro', qtd_opcoes[0])) if saeb_atual.get('qtd_carro') in qtd_opcoes else 0
            )
        
        with col4:
            qtd_celular_internet = st.selectbox(
                "Celular com internet",
                qtd_opcoes,
                index=qtd_opcoes.index(saeb_atual.get('qtd_celular_internet', qtd_opcoes[0])) if saeb_atual.get('qtd_celular_internet') in qtd_opcoes else 0
            )
        
        st.markdown("**Itens presentes na casa:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            casa_tv_internet = st.checkbox("TV por internet", 
                                           value=saeb_atual.get('casa_tv_internet') == 'Sim' if saeb_atual else False)
            casa_wifi = st.checkbox("Rede Wi-Fi", 
                                    value=saeb_atual.get('casa_wifi') == 'Sim' if saeb_atual else False)
        
        with col2:
            casa_mesa_estudar = st.checkbox("Mesa para estudar", 
                                            value=saeb_atual.get('casa_mesa_estudar') == 'Sim' if saeb_atual else False)
            casa_microondas = st.checkbox("Micro-ondas", 
                                          value=saeb_atual.get('casa_microondas') == 'Sim' if saeb_atual else False)
        
        with col3:
            casa_aspirador = st.checkbox("Aspirador de pó", 
                                         value=saeb_atual.get('casa_aspirador') == 'Sim' if saeb_atual else False)
            casa_maquina_lavar = st.checkbox("Máquina de lavar", 
                                             value=saeb_atual.get('casa_maquina_lavar') == 'Sim' if saeb_atual else False)
        
        with col4:
            casa_freezer = st.checkbox("Freezer", 
                                       value=saeb_atual.get('casa_freezer') == 'Sim' if saeb_atual else False)
            casa_garagem = st.checkbox("Garagem", 
                                       value=saeb_atual.get('casa_garagem') == 'Sim' if saeb_atual else False)
        
        # Seção 8: Trajeto até a escola
        st.subheader("8. Trajeto até a escola")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tempo_escola = st.selectbox(
                "8.1 Tempo para chegar à escola *",
                ["", "Menos de 30 minutos", "Entre 30 min e 1 hora", "Mais de 1 hora"],
                index=0 if not saeb_atual.get('tempo_escola') else 
                ["", "Menos de 30 minutos", "Entre 30 min e 1 hora", "Mais de 1 hora"].index(saeb_atual.get('tempo_escola', ''))
            )
        
        with col2:
            meio_transporte_principal = st.selectbox(
                "8.3 Meio principal para chegar à escola *",
                ["", "A pé", "Bicicleta", "Van / Kombi", "Ônibus", "Metrô / trem", 
                 "Carro", "Barco", "Motocicleta", "Outro"],
                index=0 if not saeb_atual.get('meio_transporte_principal') else 
                ["", "A pé", "Bicicleta", "Van / Kombi", "Ônibus", "Metrô / trem", 
                 "Carro", "Barco", "Motocicleta", "Outro"].index(saeb_atual.get('meio_transporte_principal', ''))
            )
        
        st.markdown("**8.2 Meio de transporte utilizado:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            transporte_gratuito = st.checkbox("Transporte escolar gratuito", 
                                              value=saeb_atual.get('transporte_gratuito') == 'Sim' if saeb_atual else False)
        
        with col2:
            passe_escolar = st.checkbox("Passe escolar", 
                                        value=saeb_atual.get('passe_escolar') == 'Sim' if saeb_atual else False)
        
        # Seção 9: Histórico Escolar
        st.subheader("9. Histórico escolar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            idade_entrada_escola = st.selectbox(
                "Idade de entrada na escola *",
                ["", "3 anos ou menos", "4–5 anos", "6–7 anos", "8 anos ou mais"],
                index=0 if not saeb_atual.get('idade_entrada_escola') else 
                ["", "3 anos ou menos", "4–5 anos", "6–7 anos", "8 anos ou mais"].index(saeb_atual.get('idade_entrada_escola', ''))
            )
            
            reprovacao = st.selectbox(
                "Reprovação *",
                ["", "Nunca", "Uma vez", "Duas ou mais vezes"],
                index=0 if not saeb_atual.get('reprovacao') else 
                ["", "Nunca", "Uma vez", "Duas ou mais vezes"].index(saeb_atual.get('reprovacao', ''))
            )
        
        with col2:
            trajetoria_educacao = st.selectbox(
                "Trajetória na educação *",
                ["", "Sempre escola pública", "Sempre escola particular", "Ambas"],
                index=0 if not saeb_atual.get('trajetoria_educacao') else 
                ["", "Sempre escola pública", "Sempre escola particular", "Ambas"].index(saeb_atual.get('trajetoria_educacao', ''))
            )
            
            abandono = st.selectbox(
                "Abandono *",
                ["", "Nunca", "Uma vez", "Duas ou mais vezes"],
                index=0 if not saeb_atual.get('abandono') else 
                ["", "Nunca", "Uma vez", "Duas ou mais vezes"].index(saeb_atual.get('abandono', ''))
            )
        
        # Seção 10: Uso do Tempo
        st.subheader("10. Uso do tempo fora da escola")
        
        tempo_opcoes = ["Não uso meu tempo para isso", "Menos de 1h", "Entre 1–2h", "Mais de 2h"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            tempo_estudar = st.selectbox(
                "Estudar",
                tempo_opcoes,
                index=tempo_opcoes.index(saeb_atual.get('tempo_estudar', tempo_opcoes[0])) if saeb_atual.get('tempo_estudar') in tempo_opcoes else 0
            )
            
            tempo_extracurriculares = st.selectbox(
                "Atividades extracurriculares",
                tempo_opcoes,
                index=tempo_opcoes.index(saeb_atual.get('tempo_extracurriculares', tempo_opcoes[0])) if saeb_atual.get('tempo_extracurriculares') in tempo_opcoes else 0
            )
            
            tempo_trabalho_domestico = st.selectbox(
                "Trabalho doméstico",
                tempo_opcoes,
                index=tempo_opcoes.index(saeb_atual.get('tempo_trabalho_domestico', tempo_opcoes[0])) if saeb_atual.get('tempo_trabalho_domestico') in tempo_opcoes else 0
            )
        
        with col2:
            tempo_trabalho_remunerado = st.selectbox(
                "Trabalho remunerado",
                tempo_opcoes,
                index=tempo_opcoes.index(saeb_atual.get('tempo_trabalho_remunerado', tempo_opcoes[0])) if saeb_atual.get('tempo_trabalho_remunerado') in tempo_opcoes else 0
            )
            
            tempo_lazer = st.selectbox(
                "Lazer",
                tempo_opcoes,
                index=tempo_opcoes.index(saeb_atual.get('tempo_lazer', tempo_opcoes[0])) if saeb_atual.get('tempo_lazer') in tempo_opcoes else 0
            )
        
        # Seção 11: Práticas Pedagógicas
        st.subheader("11. Percepção sobre práticas pedagógicas")
        st.markdown("**Proporção de professores que fazem:**")
        
        prop_opcoes = ["Nenhum", "Poucos", "A maioria", "Todos"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            prof_explica = st.selectbox(
                "Explicam o que será ensinado",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_explica', prop_opcoes[0])) if saeb_atual.get('prof_explica') in prop_opcoes else 0
            )
            
            prof_pergunta = st.selectbox(
                "Perguntam o que o aluno já sabe",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_pergunta', prop_opcoes[0])) if saeb_atual.get('prof_pergunta') in prop_opcoes else 0
            )
            
            prof_debate = st.selectbox(
                "Trazem temas para debate",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_debate', prop_opcoes[0])) if saeb_atual.get('prof_debate') in prop_opcoes else 0
            )
            
            prof_grupos = st.selectbox(
                "Trabalham em grupos",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_grupos', prop_opcoes[0])) if saeb_atual.get('prof_grupos') in prop_opcoes else 0
            )
        
        with col2:
            prof_bullying = st.selectbox(
                "Abordam bullying",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_bullying', prop_opcoes[0])) if saeb_atual.get('prof_bullying') in prop_opcoes else 0
            )
            
            prof_racismo = st.selectbox(
                "Abordam racismo",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_racismo', prop_opcoes[0])) if saeb_atual.get('prof_racismo') in prop_opcoes else 0
            )
            
            prof_genero = st.selectbox(
                "Abordam desigualdade de gênero",
                prop_opcoes,
                index=prop_opcoes.index(saeb_atual.get('prof_genero', prop_opcoes[0])) if saeb_atual.get('prof_genero') in prop_opcoes else 0
            )
        
        # Seção 12: Percepção da Escola
        st.subheader("12. Percepção da escola")
        
        percepcao_opcoes = ["Discordo totalmente", "Discordo", "Concordo", "Concordo totalmente"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            escola_interesse = st.selectbox(
                "Interesse nos conteúdos",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_interesse', percepcao_opcoes[0])) if saeb_atual.get('escola_interesse') in percepcao_opcoes else 0
            )
            
            escola_motivacao = st.selectbox(
                "Motivação para estudar",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_motivacao', percepcao_opcoes[0])) if saeb_atual.get('escola_motivacao') in percepcao_opcoes else 0
            )
            
            escola_opinioes = st.selectbox(
                "Opiniões respeitadas",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_opinioes', percepcao_opcoes[0])) if saeb_atual.get('escola_opinioes') in percepcao_opcoes else 0
            )
            
            escola_seguranca = st.selectbox(
                "Sentir-se seguro",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_seguranca', percepcao_opcoes[0])) if saeb_atual.get('escola_seguranca') in percepcao_opcoes else 0
            )
            
            escola_vontade_prof = st.selectbox(
                "Sentir-se à vontade com professores",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_vontade_prof', percepcao_opcoes[0])) if saeb_atual.get('escola_vontade_prof') in percepcao_opcoes else 0
            )
        
        with col2:
            escola_dificuldade = st.selectbox(
                "Dificuldade dos conteúdos",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_dificuldade', percepcao_opcoes[0])) if saeb_atual.get('escola_dificuldade') in percepcao_opcoes else 0
            )
            
            escola_avaliacoes = st.selectbox(
                "Avaliações refletem aprendizado",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_avaliacoes', percepcao_opcoes[0])) if saeb_atual.get('escola_avaliacoes') in percepcao_opcoes else 0
            )
            
            escola_prof_acreditam = st.selectbox(
                "Professores acreditam no aluno",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_prof_acreditam', percepcao_opcoes[0])) if saeb_atual.get('escola_prof_acreditam') in percepcao_opcoes else 0
            )
            
            escola_motivacao_continuar = st.selectbox(
                "Motivação para continuar estudos",
                percepcao_opcoes,
                index=percepcao_opcoes.index(saeb_atual.get('escola_motivacao_continuar', percepcao_opcoes[0])) if saeb_atual.get('escola_motivacao_continuar') in percepcao_opcoes else 0
            )
        
        # Seção 13: Expectativas Futuras
        st.subheader("13. Expectativas futuras")
        
        expectativa_futura = st.selectbox(
            "O que pretende fazer após concluir este ano? *",
            ["", "Continuar estudando", "Só trabalhar", "Trabalhar e estudar", "Não sabe"],
            index=0 if not saeb_atual.get('expectativa_futura') else 
            ["", "Continuar estudando", "Só trabalhar", "Trabalhar e estudar", "Não sabe"].index(saeb_atual.get('expectativa_futura', ''))
        )
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Questionário", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not sexo:
                erros.append("Sexo é obrigatório")
            if not idade:
                erros.append("Idade é obrigatória")
            if not lingua_familia:
                erros.append("Língua falada pela família é obrigatória")
            if not cor_raca:
                erros.append("Cor ou raça é obrigatória")
            if not escolaridade_mae:
                erros.append("Escolaridade da mãe é obrigatória")
            if not escolaridade_pai:
                erros.append("Escolaridade do pai é obrigatória")
            if not tempo_escola:
                erros.append("Tempo para chegar à escola é obrigatório")
            if not meio_transporte_principal:
                erros.append("Meio principal de transporte é obrigatório")
            if not idade_entrada_escola:
                erros.append("Idade de entrada na escola é obrigatória")
            if not trajetoria_educacao:
                erros.append("Trajetória na educação é obrigatória")
            if not reprovacao:
                erros.append("Informação sobre reprovação é obrigatória")
            if not abandono:
                erros.append("Informação sobre abandono é obrigatória")
            if not expectativa_futura:
                erros.append("Expectativa futura é obrigatória")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                dados = {
                    'aluno_id': aluno_id,
                    'sexo': sexo,
                    'idade': idade,
                    'lingua_familia': lingua_familia,
                    'cor_raca': cor_raca,
                    'deficiencia': deficiencia,
                    'tea': tea,
                    'altas_habilidades': altas_habilidades,
                    'mora_mae': 'Sim' if mora_mae else 'Não',
                    'mora_pai': 'Sim' if mora_pai else 'Não',
                    'mora_avo': 'Sim' if mora_avo else 'Não',
                    'mora_avoh': 'Sim' if mora_avoh else 'Não',
                    'mora_outros': 'Sim' if mora_outros else 'Não',
                    'escolaridade_mae': escolaridade_mae,
                    'escolaridade_pai': escolaridade_pai,
                    'responsavel_le': responsavel_le,
                    'responsavel_conversa': responsavel_conversa,
                    'responsavel_incentiva_estudar': responsavel_incentiva_estudar,
                    'responsavel_incentiva_tarefas': responsavel_incentiva_tarefas,
                    'responsavel_incentiva_aulas': responsavel_incentiva_aulas,
                    'responsavel_participa_reunioes': responsavel_participa_reunioes,
                    'bairro_asfalto': 'Sim' if bairro_asfalto else 'Não',
                    'bairro_agua_tratada': 'Sim' if bairro_agua_tratada else 'Não',
                    'bairro_iluminacao': 'Sim' if bairro_iluminacao else 'Não',
                    'qtd_geladeira': qtd_geladeira,
                    'qtd_computador': qtd_computador,
                    'qtd_quartos': qtd_quartos,
                    'qtd_televisao': qtd_televisao,
                    'qtd_banheiro': qtd_banheiro,
                    'qtd_carro': qtd_carro,
                    'qtd_celular_internet': qtd_celular_internet,
                    'casa_tv_internet': 'Sim' if casa_tv_internet else 'Não',
                    'casa_wifi': 'Sim' if casa_wifi else 'Não',
                    'casa_mesa_estudar': 'Sim' if casa_mesa_estudar else 'Não',
                    'casa_microondas': 'Sim' if casa_microondas else 'Não',
                    'casa_aspirador': 'Sim' if casa_aspirador else 'Não',
                    'casa_maquina_lavar': 'Sim' if casa_maquina_lavar else 'Não',
                    'casa_freezer': 'Sim' if casa_freezer else 'Não',
                    'casa_garagem': 'Sim' if casa_garagem else 'Não',
                    'tempo_escola': tempo_escola,
                    'transporte_gratuito': 'Sim' if transporte_gratuito else 'Não',
                    'passe_escolar': 'Sim' if passe_escolar else 'Não',
                    'meio_transporte_principal': meio_transporte_principal,
                    'idade_entrada_escola': idade_entrada_escola,
                    'trajetoria_educacao': trajetoria_educacao,
                    'reprovacao': reprovacao,
                    'abandono': abandono,
                    'tempo_estudar': tempo_estudar,
                    'tempo_extracurriculares': tempo_extracurriculares,
                    'tempo_trabalho_domestico': tempo_trabalho_domestico,
                    'tempo_trabalho_remunerado': tempo_trabalho_remunerado,
                    'tempo_lazer': tempo_lazer,
                    'prof_explica': prof_explica,
                    'prof_pergunta': prof_pergunta,
                    'prof_debate': prof_debate,
                    'prof_grupos': prof_grupos,
                    'prof_bullying': prof_bullying,
                    'prof_racismo': prof_racismo,
                    'prof_genero': prof_genero,
                    'escola_interesse': escola_interesse,
                    'escola_motivacao': escola_motivacao,
                    'escola_opinioes': escola_opinioes,
                    'escola_seguranca': escola_seguranca,
                    'escola_vontade_prof': escola_vontade_prof,
                    'escola_dificuldade': escola_dificuldade,
                    'escola_avaliacoes': escola_avaliacoes,
                    'escola_prof_acreditam': escola_prof_acreditam,
                    'escola_motivacao_continuar': escola_motivacao_continuar,
                    'expectativa_futura': expectativa_futura
                }
                
                try:
                    if len(saeb_existente) > 0:
                        # Atualizar existente
                        data_manager.update_record('questionario_saeb', saeb_existente.iloc[0]['id'], dados)
                        st.success("✅ Questionário SAEB atualizado com sucesso!")
                    else:
                        # Criar novo
                        data_manager.add_record('questionario_saeb', dados)
                        st.success("✅ Questionário SAEB cadastrado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar questionário: {str(e)}")
