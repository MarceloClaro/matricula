"""
Módulo Anamnese Pedagógica para PEI
Questionário neuropsicopedagógico rigoroso (Qualis A1) para elaboração do PEI
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def render_anamnese_pei(data_manager):
    """Renderiza questionário de anamnese pedagógica completo"""
    st.header("📋 Anamnese Pedagógica e Neuropsicopedagógica - PEI")
    st.markdown("---")
    
    st.info("""
    **Fundamentação Legal e Conceitual**
    
    Este relatório foi elaborado com base em princípios neuropsicopedagógicos e nas normativas legais vigentes, 
    objetivando registrar de forma detalhada os comportamentos observados, os impactos no ambiente educacional 
    e as medidas de intervenção realizadas e indicadas.
    
    **Referências Legais:**
    - Estatuto da Criança e do Adolescente (ECA) – Lei nº 8.069/1990 (Art. 98 a 102)
    - Lei de Diretrizes e Bases da Educação Nacional (LDB) – Lei nº 9.394/1996
    - Lei nº 13.185/2015 – Política Nacional de Combate ao Bullying
    - Lei nº 7.716/1989 – Prevenção ao Racismo
    """)
    
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
    
    aluno_selecionado = st.selectbox("Aluno(a) *", alunos_opcoes)
    
    if aluno_selecionado == "Selecione um aluno":
        st.info("Selecione um aluno para preencher a anamnese pedagógica")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    aluno_info = df_alunos[df_alunos['id'] == aluno_id].iloc[0]
    
    # Verificar se já existe anamnese para este aluno
    df_anamnese = data_manager.get_data('anamnese_pei')
    anamnese_existente = df_anamnese[df_anamnese['aluno_id'] == aluno_id]
    
    if len(anamnese_existente) > 0:
        st.info("ℹ️ Este aluno já possui anamnese pedagógica cadastrada. Você pode editá-la abaixo.")
        anamnese_atual = anamnese_existente.iloc[0].to_dict()
    else:
        # Auto-preencher com dados do cadastro geral se não houver anamnese
        anamnese_atual = {}
        
        # Auto-preencher filiação
        filiacao_parts = []
        if pd.notna(aluno_info.get('nome_mae')) and aluno_info.get('nome_mae'):
            filiacao_parts.append(f"Mãe: {aluno_info['nome_mae']}")
        if pd.notna(aluno_info.get('nome_pai')) and aluno_info.get('nome_pai'):
            filiacao_parts.append(f"Pai: {aluno_info['nome_pai']}")
        if filiacao_parts:
            anamnese_atual['filiacao'] = '\n'.join(filiacao_parts)
        
        # Auto-preencher ano/turma do cadastro
        if pd.notna(aluno_info.get('ano_escolar')) and aluno_info.get('ano_escolar'):
            anamnese_atual['turma_serie'] = aluno_info['ano_escolar']
        
        # Exibir aviso de auto-preenchimento
        if anamnese_atual:
            st.success("✨ Alguns campos foram automaticamente preenchidos com informações do cadastro geral. Você pode editá-los se necessário.")
    
    with st.form("form_anamnese_pei"):
        # Seção 1: Identificação
        st.subheader("1. Identificação do Aluno")
        
        col1, col2 = st.columns(2)
        with col1:
            data_preenchimento = st.date_input(
                "Data do Preenchimento *",
                value=datetime.strptime(anamnese_atual.get('data_preenchimento', ''), '%Y-%m-%d') 
                if anamnese_atual.get('data_preenchimento') else datetime.now()
            )
            
            filiacao = st.text_area(
                "Filiação *",
                value=anamnese_atual.get('filiacao', ''),
                height=80
            )
        
        with col2:
            turma_serie = st.selectbox(
                "Ano/Turma *",
                ["", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                 "6º Ano-A", "6º Ano-B", "7º Ano-A", "7º Ano-B", 
                 "8º Ano-A", "8º Ano-B", "9º Ano-A", "9º Ano-B"],
                index=0 if not anamnese_atual.get('turma_serie') else
                ["", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                 "6º Ano-A", "6º Ano-B", "7º Ano-A", "7º Ano-B", 
                 "8º Ano-A", "8º Ano-B", "9º Ano-A", "9º Ano-B"].index(anamnese_atual.get('turma_serie', ''))
            )
        
        # Seção 2: Desenvolvimento Neuropsicomotor
        st.subheader("2. Desenvolvimento Neuropsicomotor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            desenvolvimento_motor = st.selectbox(
                "2.1 Desenvolvimento Motor Geral",
                ["Típico", "Atraso leve", "Atraso moderado", "Atraso severo", "Não avaliado"],
                index=["Típico", "Atraso leve", "Atraso moderado", "Atraso severo", "Não avaliado"].index(
                    anamnese_atual.get('desenvolvimento_motor', 'Típico'))
            )
            
            coordenacao_motora_fina = st.selectbox(
                "2.2 Coordenação Motora Fina",
                ["Adequada", "Parcialmente adequada", "Inadequada", "Não avaliada"],
                index=["Adequada", "Parcialmente adequada", "Inadequada", "Não avaliada"].index(
                    anamnese_atual.get('coordenacao_motora_fina', 'Adequada'))
            )
            
            coordenacao_motora_grossa = st.selectbox(
                "2.3 Coordenação Motora Grossa",
                ["Adequada", "Parcialmente adequada", "Inadequada", "Não avaliada"],
                index=["Adequada", "Parcialmente adequada", "Inadequada", "Não avaliada"].index(
                    anamnese_atual.get('coordenacao_motora_grossa', 'Adequada'))
            )
        
        with col2:
            lateralidade = st.selectbox(
                "2.4 Lateralidade",
                ["Destro", "Canhoto", "Ambidestro", "Não definida"],
                index=["Destro", "Canhoto", "Ambidestro", "Não definida"].index(
                    anamnese_atual.get('lateralidade', 'Destro'))
            )
            
            equilibrio = st.selectbox(
                "2.5 Equilíbrio",
                ["Adequado", "Dificuldades leves", "Dificuldades significativas"],
                index=["Adequado", "Dificuldades leves", "Dificuldades significativas"].index(
                    anamnese_atual.get('equilibrio', 'Adequado'))
            )
        
        observacoes_neuro = st.text_area(
            "Observações sobre Desenvolvimento Neuropsicomotor",
            value=anamnese_atual.get('observacoes_neuro', ''),
            height=100
        )
        
        # Seção 3: Desenvolvimento Cognitivo
        st.subheader("3. Desenvolvimento Cognitivo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            atencao_concentracao = st.selectbox(
                "3.1 Atenção e Concentração",
                ["Mantém atenção adequadamente", "Atenção dispersa ocasionalmente", 
                 "Dificuldade significativa de atenção", "Hiperatenção (foco excessivo)"],
                index=["Mantém atenção adequadamente", "Atenção dispersa ocasionalmente", 
                 "Dificuldade significativa de atenção", "Hiperatenção (foco excessivo)"].index(
                    anamnese_atual.get('atencao_concentracao', 'Mantém atenção adequadamente'))
            )
            
            memoria = st.selectbox(
                "3.2 Memória",
                ["Memória adequada", "Dificuldade em memória de curto prazo", 
                 "Dificuldade em memória de longo prazo", "Dificuldade em ambas"],
                index=["Memória adequada", "Dificuldade em memória de curto prazo", 
                 "Dificuldade em memória de longo prazo", "Dificuldade em ambas"].index(
                    anamnese_atual.get('memoria', 'Memória adequada'))
            )
            
            raciocinio_logico = st.selectbox(
                "3.3 Raciocínio Lógico-Matemático",
                ["Adequado à idade", "Abaixo do esperado", "Acima do esperado"],
                index=["Adequado à idade", "Abaixo do esperado", "Acima do esperado"].index(
                    anamnese_atual.get('raciocinio_logico', 'Adequado à idade'))
            )
        
        with col2:
            resolucao_problemas = st.selectbox(
                "3.4 Resolução de Problemas",
                ["Resolve autonomamente", "Necessita auxílio ocasional", 
                 "Necessita auxílio constante", "Não consegue resolver"],
                index=["Resolve autonomamente", "Necessita auxílio ocasional", 
                 "Necessita auxílio constante", "Não consegue resolver"].index(
                    anamnese_atual.get('resolucao_problemas', 'Resolve autonomamente'))
            )
            
            pensamento_abstrato = st.selectbox(
                "3.5 Pensamento Abstrato",
                ["Desenvolvido", "Em desenvolvimento", "Concreto predominante"],
                index=["Desenvolvido", "Em desenvolvimento", "Concreto predominante"].index(
                    anamnese_atual.get('pensamento_abstrato', 'Em desenvolvimento'))
            )
            
            funcoes_executivas = st.selectbox(
                "3.6 Funções Executivas (planejamento, organização)",
                ["Adequadas", "Parcialmente adequadas", "Inadequadas"],
                index=["Adequadas", "Parcialmente adequadas", "Inadequadas"].index(
                    anamnese_atual.get('funcoes_executivas', 'Adequadas'))
            )
        
        observacoes_cognitivas = st.text_area(
            "Observações sobre Desenvolvimento Cognitivo",
            value=anamnese_atual.get('observacoes_cognitivas', ''),
            height=100
        )
        
        # Seção 4: Linguagem e Comunicação
        st.subheader("4. Linguagem e Comunicação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            linguagem_oral = st.selectbox(
                "4.1 Linguagem Oral",
                ["Adequada", "Atraso leve", "Atraso moderado", "Atraso severo", "Não verbal"],
                index=["Adequada", "Atraso leve", "Atraso moderado", "Atraso severo", "Não verbal"].index(
                    anamnese_atual.get('linguagem_oral', 'Adequada'))
            )
            
            articulacao = st.selectbox(
                "4.2 Articulação de Fonemas",
                ["Clara e adequada", "Algumas trocas fonêmicas", "Múltiplas trocas", "Ininteligível"],
                index=["Clara e adequada", "Algumas trocas fonêmicas", "Múltiplas trocas", "Ininteligível"].index(
                    anamnese_atual.get('articulacao', 'Clara e adequada'))
            )
            
            vocabulario = st.selectbox(
                "4.3 Vocabulário",
                ["Amplo e diversificado", "Adequado à idade", "Restrito", "Muito limitado"],
                index=["Amplo e diversificado", "Adequado à idade", "Restrito", "Muito limitado"].index(
                    anamnese_atual.get('vocabulario', 'Adequado à idade'))
            )
        
        with col2:
            compreensao_verbal = st.selectbox(
                "4.4 Compreensão Verbal",
                ["Adequada", "Dificuldade parcial", "Dificuldade significativa"],
                index=["Adequada", "Dificuldade parcial", "Dificuldade significativa"].index(
                    anamnese_atual.get('compreensao_verbal', 'Adequada'))
            )
            
            expressao_verbal = st.selectbox(
                "4.5 Expressão Verbal",
                ["Fluente e adequada", "Dificuldade de expressão", "Comunicação limitada"],
                index=["Fluente e adequada", "Dificuldade de expressão", "Comunicação limitada"].index(
                    anamnese_atual.get('expressao_verbal', 'Fluente e adequada'))
            )
            
            linguagem_escrita = st.selectbox(
                "4.6 Linguagem Escrita",
                ["Adequada", "Em desenvolvimento", "Dificuldades", "Não alfabetizado"],
                index=["Adequada", "Em desenvolvimento", "Dificuldades", "Não alfabetizado"].index(
                    anamnese_atual.get('linguagem_escrita', 'Em desenvolvimento'))
            )
        
        observacoes_linguagem = st.text_area(
            "Observações sobre Linguagem e Comunicação",
            value=anamnese_atual.get('observacoes_linguagem', ''),
            height=100
        )
        
        # Seção 5: Aspectos Socioemocionais
        st.subheader("5. Aspectos Socioemocionais e Comportamentais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            interacao_social = st.selectbox(
                "5.1 Interação Social",
                ["Interage adequadamente", "Tímido/retraído", "Dificuldade de interação", "Isolamento social"],
                index=["Interage adequadamente", "Tímido/retraído", "Dificuldade de interação", "Isolamento social"].index(
                    anamnese_atual.get('interacao_social', 'Interage adequadamente'))
            )
            
            relacionamento_pares = st.selectbox(
                "5.2 Relacionamento com Pares",
                ["Bom relacionamento", "Relacionamento seletivo", "Conflitos ocasionais", "Conflitos frequentes"],
                index=["Bom relacionamento", "Relacionamento seletivo", "Conflitos ocasionais", "Conflitos frequentes"].index(
                    anamnese_atual.get('relacionamento_pares', 'Bom relacionamento'))
            )
            
            relacionamento_professores = st.selectbox(
                "5.3 Relacionamento com Professores",
                ["Respeitoso e colaborativo", "Ocasionalmente desafiador", "Frequentemente desafiador", "Conflituoso"],
                index=["Respeitoso e colaborativo", "Ocasionalmente desafiador", "Frequentemente desafiador", "Conflituoso"].index(
                    anamnese_atual.get('relacionamento_professores', 'Respeitoso e colaborativo'))
            )
            
            regulacao_emocional = st.selectbox(
                "5.4 Regulação Emocional",
                ["Adequada", "Dificuldade leve", "Dificuldade moderada", "Desregulação frequente"],
                index=["Adequada", "Dificuldade leve", "Dificuldade moderada", "Desregulação frequente"].index(
                    anamnese_atual.get('regulacao_emocional', 'Adequada'))
            )
        
        with col2:
            autoestima = st.selectbox(
                "5.5 Autoestima",
                ["Adequada", "Baixa", "Oscilante", "Superestimada"],
                index=["Adequada", "Baixa", "Oscilante", "Superestimada"].index(
                    anamnese_atual.get('autoestima', 'Adequada'))
            )
            
            ansiedade = st.selectbox(
                "5.6 Níveis de Ansiedade",
                ["Não apresenta", "Ansiedade leve", "Ansiedade moderada", "Ansiedade severa"],
                index=["Não apresenta", "Ansiedade leve", "Ansiedade moderada", "Ansiedade severa"].index(
                    anamnese_atual.get('ansiedade', 'Não apresenta'))
            )
            
            impulsividade = st.selectbox(
                "5.7 Impulsividade",
                ["Controle adequado", "Ocasionalmente impulsivo", "Frequentemente impulsivo"],
                index=["Controle adequado", "Ocasionalmente impulsivo", "Frequentemente impulsivo"].index(
                    anamnese_atual.get('impulsividade', 'Controle adequado'))
            )
            
            agressividade = st.selectbox(
                "5.8 Comportamento Agressivo",
                ["Não apresenta", "Agressividade verbal ocasional", "Agressividade física ocasional", "Agressividade frequente"],
                index=["Não apresenta", "Agressividade verbal ocasional", "Agressividade física ocasional", "Agressividade frequente"].index(
                    anamnese_atual.get('agressividade', 'Não apresenta'))
            )
        
        # Comportamentos específicos
        st.markdown("**5.9 Comportamentos Observados**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bullying_vitima = st.checkbox("Vítima de bullying", 
                value=anamnese_atual.get('bullying_vitima') == 'Sim' if anamnese_atual else False)
            bullying_agressor = st.checkbox("Agressor em situações de bullying", 
                value=anamnese_atual.get('bullying_agressor') == 'Sim' if anamnese_atual else False)
        
        with col2:
            comportamento_opositor = st.checkbox("Comportamento opositor desafiador", 
                value=anamnese_atual.get('comportamento_opositor') == 'Sim' if anamnese_atual else False)
            autolesao = st.checkbox("Comportamento autolesivo", 
                value=anamnese_atual.get('autolesao') == 'Sim' if anamnese_atual else False)
        
        with col3:
            fuga_escola = st.checkbox("Tentativas de fuga da escola", 
                value=anamnese_atual.get('fuga_escola') == 'Sim' if anamnese_atual else False)
            isolamento_voluntario = st.checkbox("Isolamento voluntário", 
                value=anamnese_atual.get('isolamento_voluntario') == 'Sim' if anamnese_atual else False)
        
        observacoes_socioemocionais = st.text_area(
            "Observações sobre Aspectos Socioemocionais",
            value=anamnese_atual.get('observacoes_socioemocionais', ''),
            height=120
        )
        
        # Seção 6: Desempenho Acadêmico
        st.subheader("6. Desempenho Acadêmico por Área")
        
        st.markdown("**Avaliação por Disciplina**")
        col1, col2, col3 = st.columns(3)
        
        desempenho_opcoes = ["Excelente", "Bom", "Regular", "Insuficiente", "Não avaliado"]
        
        with col1:
            desempenho_portugues = st.selectbox(
                "Língua Portuguesa",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_portugues', 'Não avaliado'))
            )
            
            desempenho_matematica = st.selectbox(
                "Matemática",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_matematica', 'Não avaliado'))
            )
            
            desempenho_ciencias = st.selectbox(
                "Ciências",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_ciencias', 'Não avaliado'))
            )
        
        with col2:
            desempenho_historia = st.selectbox(
                "História",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_historia', 'Não avaliado'))
            )
            
            desempenho_geografia = st.selectbox(
                "Geografia",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_geografia', 'Não avaliado'))
            )
            
            desempenho_ingles = st.selectbox(
                "Língua Inglesa",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_ingles', 'Não avaliado'))
            )
        
        with col3:
            desempenho_ed_fisica = st.selectbox(
                "Educação Física",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_ed_fisica', 'Não avaliado'))
            )
            
            desempenho_artes = st.selectbox(
                "Artes",
                desempenho_opcoes,
                index=desempenho_opcoes.index(anamnese_atual.get('desempenho_artes', 'Não avaliado'))
            )
        
        # Habilidades de Leitura e Escrita
        st.markdown("**6.1 Habilidades de Leitura e Escrita**")
        col1, col2 = st.columns(2)
        
        with col1:
            leitura = st.selectbox(
                "Nível de Leitura",
                ["Pré-silábico", "Silábico", "Silábico-alfabético", "Alfabético", "Fluente"],
                index=["Pré-silábico", "Silábico", "Silábico-alfabético", "Alfabético", "Fluente"].index(
                    anamnese_atual.get('leitura', 'Alfabético'))
            )
            
            escrita = st.selectbox(
                "Nível de Escrita",
                ["Pré-silábica", "Silábica", "Silábico-alfabética", "Alfabética", "Ortográfica"],
                index=["Pré-silábica", "Silábica", "Silábico-alfabética", "Alfabética", "Ortográfica"].index(
                    anamnese_atual.get('escrita', 'Alfabética'))
            )
        
        with col2:
            compreensao_leitora = st.selectbox(
                "Compreensão Leitora",
                ["Adequada", "Dificuldade leve", "Dificuldade significativa", "Não compreende"],
                index=["Adequada", "Dificuldade leve", "Dificuldade significativa", "Não compreende"].index(
                    anamnese_atual.get('compreensao_leitora', 'Adequada'))
            )
            
            producao_textual = st.selectbox(
                "Produção Textual",
                ["Adequada", "Textos curtos e simples", "Dificuldade significativa", "Não produz"],
                index=["Adequada", "Textos curtos e simples", "Dificuldade significativa", "Não produz"].index(
                    anamnese_atual.get('producao_textual', 'Textos curtos e simples'))
            )
        
        observacoes_academicas = st.text_area(
            "Observações sobre Desempenho Acadêmico",
            value=anamnese_atual.get('observacoes_academicas', ''),
            height=120
        )
        
        # Seção 7: Adaptações e Intervenções
        st.subheader("7. Adaptações Curriculares e Intervenções Necessárias")
        
        adaptacoes_metodologicas = st.text_area(
            "7.1 Adaptações Metodológicas",
            value=anamnese_atual.get('adaptacoes_metodologicas', ''),
            height=100,
            help="Ex: tempo estendido, instruções simplificadas, uso de recursos visuais"
        )
        
        adaptacoes_avaliativas = st.text_area(
            "7.2 Adaptações Avaliativas",
            value=anamnese_atual.get('adaptacoes_avaliativas', ''),
            height=100,
            help="Ex: provas orais, avaliações diferenciadas, redução de questões"
        )
        
        recursos_tecnologicos = st.text_area(
            "7.3 Recursos Tecnológicos e Materiais Adaptados",
            value=anamnese_atual.get('recursos_tecnologicos', ''),
            height=100,
            help="Ex: tablets, softwares educacionais, materiais sensoriais"
        )
        
        intervencoes_pedagogicas = st.text_area(
            "7.4 Intervenções Pedagógicas Específicas",
            value=anamnese_atual.get('intervencoes_pedagogicas', ''),
            height=120,
            help="Descreva estratégias e intervenções já aplicadas ou recomendadas"
        )
        
        # Seção 8: Encaminhamentos e Acompanhamentos
        st.subheader("8. Encaminhamentos e Acompanhamentos Profissionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            acompanhamento_psicologia = st.radio(
                "8.1 Acompanhamento Psicológico",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_psicologia', 'Não necessita'))
            )
            
            acompanhamento_psicopedagogia = st.radio(
                "8.2 Acompanhamento Psicopedagógico",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_psicopedagogia', 'Não necessita'))
            )
            
            acompanhamento_fonoaudiologia = st.radio(
                "8.3 Acompanhamento Fonoaudiológico",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_fonoaudiologia', 'Não necessita'))
            )
            
            acompanhamento_terapia_ocupacional = st.radio(
                "8.4 Terapia Ocupacional",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_terapia_ocupacional', 'Não necessita'))
            )
        
        with col2:
            acompanhamento_neurologia = st.radio(
                "8.5 Acompanhamento Neurológico",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_neurologia', 'Não necessita'))
            )
            
            acompanhamento_psiquiatria = st.radio(
                "8.6 Acompanhamento Psiquiátrico",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_psiquiatria', 'Não necessita'))
            )
            
            acompanhamento_assistente_social = st.radio(
                "8.7 Assistência Social",
                ["Não necessita", "Recomendado", "Em curso"],
                index=["Não necessita", "Recomendado", "Em curso"].index(
                    anamnese_atual.get('acompanhamento_assistente_social', 'Não necessita'))
            )
            
            outros_encaminhamentos = st.text_input(
                "8.8 Outros Encaminhamentos",
                value=anamnese_atual.get('outros_encaminhamentos', '')
            )
        
        # Seção 9: Contexto Familiar e Social
        st.subheader("9. Contexto Familiar e Social")
        
        participacao_familia = st.selectbox(
            "9.1 Participação da Família na Vida Escolar",
            ["Muito participativa", "Participativa", "Pouco participativa", "Ausente"],
            index=["Muito participativa", "Participativa", "Pouco participativa", "Ausente"].index(
                anamnese_atual.get('participacao_familia', 'Participativa'))
        )
        
        contexto_familiar = st.text_area(
            "9.2 Contexto Familiar Relevante",
            value=anamnese_atual.get('contexto_familiar', ''),
            height=120,
            help="Descreva aspectos relevantes do contexto familiar que impactam a aprendizagem"
        )
        
        fatores_risco = st.text_area(
            "9.3 Fatores de Risco Identificados",
            value=anamnese_atual.get('fatores_risco', ''),
            height=100,
            help="Ex: violência doméstica, negligência, abuso, pobreza extrema"
        )
        
        fatores_protecao = st.text_area(
            "9.4 Fatores de Proteção Identificados",
            value=anamnese_atual.get('fatores_protecao', ''),
            height=100,
            help="Ex: rede de apoio, resiliência, habilidades sociais"
        )
        
        # Seção 10: Plano de Ação
        st.subheader("10. Plano de Ação e Metas")
        
        metas_curto_prazo = st.text_area(
            "10.1 Metas de Curto Prazo (até 3 meses)",
            value=anamnese_atual.get('metas_curto_prazo', ''),
            height=120
        )
        
        metas_medio_prazo = st.text_area(
            "10.2 Metas de Médio Prazo (3 a 6 meses)",
            value=anamnese_atual.get('metas_medio_prazo', ''),
            height=120
        )
        
        metas_longo_prazo = st.text_area(
            "10.3 Metas de Longo Prazo (6 meses a 1 ano)",
            value=anamnese_atual.get('metas_longo_prazo', ''),
            height=120
        )
        
        estrategias_implementacao = st.text_area(
            "10.4 Estratégias de Implementação",
            value=anamnese_atual.get('estrategias_implementacao', ''),
            height=120,
            help="Descreva como as metas serão alcançadas"
        )
        
        # Seção 11: Observações Finais e Parecer
        st.subheader("11. Observações Finais e Parecer Técnico")
        
        observacoes_gerais = st.text_area(
            "11.1 Observações Gerais",
            value=anamnese_atual.get('observacoes_gerais', ''),
            height=150
        )
        
        parecer_tecnico = st.text_area(
            "11.2 Parecer Técnico do Profissional",
            value=anamnese_atual.get('parecer_tecnico', ''),
            height=150,
            help="Síntese diagnóstica e recomendações profissionais"
        )
        
        profissional_responsavel = st.text_input(
            "Nome do Profissional Responsável *",
            value=anamnese_atual.get('profissional_responsavel', '')
        )
        
        col1, col2 = st.columns(2)
        with col1:
            formacao_profissional = st.text_input(
                "Formação/Cargo *",
                value=anamnese_atual.get('formacao_profissional', '')
            )
        with col2:
            registro_profissional = st.text_input(
                "Registro Profissional",
                value=anamnese_atual.get('registro_profissional', '')
            )
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Anamnese Pedagógica", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not filiacao:
                erros.append("Filiação é obrigatória")
            if not turma_serie:
                erros.append("Ano/Turma é obrigatório")
            if not profissional_responsavel:
                erros.append("Nome do profissional responsável é obrigatório")
            if not formacao_profissional:
                erros.append("Formação/Cargo é obrigatório")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                dados = {
                    'aluno_id': aluno_id,
                    'data_preenchimento': data_preenchimento.strftime('%Y-%m-%d'),
                    'filiacao': filiacao,
                    'turma_serie': turma_serie,
                    'desenvolvimento_motor': desenvolvimento_motor,
                    'coordenacao_motora_fina': coordenacao_motora_fina,
                    'coordenacao_motora_grossa': coordenacao_motora_grossa,
                    'lateralidade': lateralidade,
                    'equilibrio': equilibrio,
                    'observacoes_neuro': observacoes_neuro,
                    'atencao_concentracao': atencao_concentracao,
                    'memoria': memoria,
                    'raciocinio_logico': raciocinio_logico,
                    'resolucao_problemas': resolucao_problemas,
                    'pensamento_abstrato': pensamento_abstrato,
                    'funcoes_executivas': funcoes_executivas,
                    'observacoes_cognitivas': observacoes_cognitivas,
                    'linguagem_oral': linguagem_oral,
                    'articulacao': articulacao,
                    'vocabulario': vocabulario,
                    'compreensao_verbal': compreensao_verbal,
                    'expressao_verbal': expressao_verbal,
                    'linguagem_escrita': linguagem_escrita,
                    'observacoes_linguagem': observacoes_linguagem,
                    'interacao_social': interacao_social,
                    'relacionamento_pares': relacionamento_pares,
                    'relacionamento_professores': relacionamento_professores,
                    'regulacao_emocional': regulacao_emocional,
                    'autoestima': autoestima,
                    'ansiedade': ansiedade,
                    'impulsividade': impulsividade,
                    'agressividade': agressividade,
                    'bullying_vitima': 'Sim' if bullying_vitima else 'Não',
                    'bullying_agressor': 'Sim' if bullying_agressor else 'Não',
                    'comportamento_opositor': 'Sim' if comportamento_opositor else 'Não',
                    'autolesao': 'Sim' if autolesao else 'Não',
                    'fuga_escola': 'Sim' if fuga_escola else 'Não',
                    'isolamento_voluntario': 'Sim' if isolamento_voluntario else 'Não',
                    'observacoes_socioemocionais': observacoes_socioemocionais,
                    'desempenho_portugues': desempenho_portugues,
                    'desempenho_matematica': desempenho_matematica,
                    'desempenho_ciencias': desempenho_ciencias,
                    'desempenho_historia': desempenho_historia,
                    'desempenho_geografia': desempenho_geografia,
                    'desempenho_ingles': desempenho_ingles,
                    'desempenho_ed_fisica': desempenho_ed_fisica,
                    'desempenho_artes': desempenho_artes,
                    'leitura': leitura,
                    'escrita': escrita,
                    'compreensao_leitora': compreensao_leitora,
                    'producao_textual': producao_textual,
                    'observacoes_academicas': observacoes_academicas,
                    'adaptacoes_metodologicas': adaptacoes_metodologicas,
                    'adaptacoes_avaliativas': adaptacoes_avaliativas,
                    'recursos_tecnologicos': recursos_tecnologicos,
                    'intervencoes_pedagogicas': intervencoes_pedagogicas,
                    'acompanhamento_psicologia': acompanhamento_psicologia,
                    'acompanhamento_psicopedagogia': acompanhamento_psicopedagogia,
                    'acompanhamento_fonoaudiologia': acompanhamento_fonoaudiologia,
                    'acompanhamento_terapia_ocupacional': acompanhamento_terapia_ocupacional,
                    'acompanhamento_neurologia': acompanhamento_neurologia,
                    'acompanhamento_psiquiatria': acompanhamento_psiquiatria,
                    'acompanhamento_assistente_social': acompanhamento_assistente_social,
                    'outros_encaminhamentos': outros_encaminhamentos,
                    'participacao_familia': participacao_familia,
                    'contexto_familiar': contexto_familiar,
                    'fatores_risco': fatores_risco,
                    'fatores_protecao': fatores_protecao,
                    'metas_curto_prazo': metas_curto_prazo,
                    'metas_medio_prazo': metas_medio_prazo,
                    'metas_longo_prazo': metas_longo_prazo,
                    'estrategias_implementacao': estrategias_implementacao,
                    'observacoes_gerais': observacoes_gerais,
                    'parecer_tecnico': parecer_tecnico,
                    'profissional_responsavel': profissional_responsavel,
                    'formacao_profissional': formacao_profissional,
                    'registro_profissional': registro_profissional
                }
                
                try:
                    if len(anamnese_existente) > 0:
                        # Atualizar existente
                        data_manager.update_record('anamnese_pei', anamnese_existente.iloc[0]['id'], dados)
                        st.success("✅ Anamnese pedagógica atualizada com sucesso!")
                    else:
                        # Criar novo
                        data_manager.add_record('anamnese_pei', dados)
                        st.success("✅ Anamnese pedagógica cadastrada com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar anamnese: {str(e)}")
