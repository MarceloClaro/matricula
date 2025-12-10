"""
Módulo de Cadastro Geral de Alunos
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import io
import json
import zipfile

def render_cadastro_geral(data_manager):
    """Renderiza formulário de cadastro geral completo"""
    st.header("📝 Ficha de Matrícula 2025")
    st.markdown("---")
    
    with st.form("form_cadastro_geral"):
        # 1. DOCUMENTAÇÃO / DADOS DO ALUNO
        st.subheader("1. 📄 Documentação / Dados do Aluno")
        
        # 1.1 Foto (placeholder)
        st.markdown("**1.1 Foto do Aluno (3x4)**")
        foto = st.file_uploader("Inserir foto do aluno", type=['jpg', 'jpeg', 'png'], key='foto_aluno')
        
        st.markdown("---")
        st.markdown("**1.2 Identificação Geral**")
        
        col1, col2 = st.columns(2)
        with col1:
            nome_completo = st.text_input("Nome Completo *", max_chars=100)
            nome_social = st.text_input("Nome Social", max_chars=100)
            cpf = st.text_input("CPF *", max_chars=14, placeholder="000.000.000-00")
            codigo_inep = st.text_input("Código INEP (ID CENSO)", max_chars=20)
        
        with col2:
            matricula = st.text_input("Matrícula", max_chars=20)
            sexo = st.selectbox("Sexo *", ["", "Masculino", "Feminino", "Outro"])
            data_nascimento = st.date_input("Data de Nascimento *", 
                                           min_value=datetime(2000, 1, 1),
                                           max_value=datetime.now())
        
        st.markdown("---")
        st.markdown("**1.3 Informações Pessoais Complementares**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cor_raca = st.selectbox("Cor/Raça", [
                "", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Não declarada"
            ])
            telefone = st.text_input("Telefone *", max_chars=20, placeholder="(00) 00000-0000")
            nis = st.text_input("NIS (Número de Identificação Social)", max_chars=20)
        
        with col2:
            nacionalidade = st.selectbox("Nacionalidade", ["", "Brasileira", "Estrangeira"])
            uf_nascimento = st.selectbox("UF de Nascimento", [
                "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ])
            cidade_nascimento = st.text_input("Cidade de Nascimento", max_chars=100)
        
        with col3:
            pais_nacionalidade = st.text_input("País de Nacionalidade", max_chars=100, value="Brasil")
            email = st.text_input("E-mail", max_chars=100)
            justificativa_documentacao = st.text_input("Justificativa de Documentação", 
                                                       max_chars=200,
                                                       placeholder="Ex.: dispensável")
        
        # 2. FILIAÇÃO
        st.markdown("---")
        st.subheader("2. 👨‍👩‍👧 Filiação")
        
        st.markdown("**2.1 Mãe**")
        col1, col2, col3 = st.columns(3)
        with col1:
            nome_mae = st.text_input("Nome da Mãe *", max_chars=100)
        with col2:
            cpf_mae = st.text_input("CPF da Mãe", max_chars=14, placeholder="000.000.000-00")
        with col3:
            profissao_mae = st.text_input("Profissão da Mãe", max_chars=100)
        
        st.markdown("**2.2 Pai**")
        col1, col2, col3 = st.columns(3)
        with col1:
            nome_pai = st.text_input("Nome do Pai", max_chars=100)
        with col2:
            cpf_pai = st.text_input("CPF do Pai", max_chars=14, placeholder="000.000.000-00")
        with col3:
            profissao_pai = st.text_input("Profissão do Pai", max_chars=100)
        
        # 3. DOCUMENTAÇÃO CIVIL
        st.markdown("---")
        st.subheader("3. 📋 Documentação Civil")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            rg = st.text_input("RG", max_chars=20)
            numero_documento = st.text_input("Número do Documento", max_chars=30)
            orgao_emissor = st.text_input("Órgão Emissor", max_chars=20, placeholder="Ex.: SSP")
        
        with col2:
            uf_emissor = st.selectbox("UF Emissor", [
                "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ])
            data_expedicao = st.date_input("Data de Expedição", 
                                          min_value=datetime(1900, 1, 1),
                                          max_value=datetime.now(),
                                          value=None)
            modelo_certidao = st.selectbox("Modelo da Certidão", [
                "", "Novo", "Antigo"
            ])
        
        with col3:
            tipo_certidao = st.selectbox("Tipo de Certidão", [
                "", "Nascimento", "Casamento", "Outro"
            ])
            cartao_sus = st.text_input("Cartão SUS", max_chars=20)
            documento_estrangeiro = st.text_input("Documento Estrangeiro", max_chars=30)
        
        # 4. ENDEREÇO COMPLETO
        st.markdown("---")
        st.subheader("4. 🏠 Endereço Completo")
        
        col1, col2 = st.columns(2)
        with col1:
            cep = st.text_input("CEP *", max_chars=10, placeholder="00000-000")
            bairro = st.text_input("Bairro *", max_chars=100)
            endereco = st.text_input("Rua/Logradouro *", max_chars=200)
        
        with col2:
            numero = st.text_input("Número *", max_chars=10)
            complemento = st.text_input("Complemento", max_chars=50)
            zona = st.selectbox("Zona", ["", "Urbana", "Rural"])
        
        col1, col2 = st.columns(2)
        with col1:
            uf = st.selectbox("Estado (UF) *", [
                "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ])
        with col2:
            cidade = st.text_input("Cidade *", max_chars=100)
        
        # 5. SAÚDE
        st.markdown("---")
        st.subheader("5. 🏥 Saúde")
        
        st.markdown("**5.1 Documentos e Identificadores**")
        cartao_nacional_sus = st.text_input("Cartão Nacional SUS", max_chars=20)
        
        st.markdown("**5.2 Condições Médicas**")
        col1, col2 = st.columns(2)
        with col1:
            alergia = st.text_area("Alergia (descrever)", max_chars=500, height=100)
            aluno_deficiencia = st.selectbox("Aluno com Deficiência?", ["", "Não", "Sim"])
            possui_laudo_medico = st.selectbox("Possui Laudo Médico?", ["", "Não", "Sim"])
        
        with col2:
            tipo_deficiencia = st.text_input("Tipo(s) de Deficiência", max_chars=200)
            atendimentos_especializados = st.text_input("Atendimentos Especializados (AEE, outros)", max_chars=200)
        
        # Se o aluno tem deficiência, mostrar campos adicionais de CID-10 e DSM-5
        if aluno_deficiencia == "Sim":
            st.markdown("---")
            st.markdown("**5.2.1 Classificação Diagnóstica (CID-10 e DSM-5)**")
            st.info("💡 Selecione o diagnóstico principal. A descrição será preenchida automaticamente.")
            
            # Lista dos 50 transtornos e deficiências mais comuns nas escolas
            diagnosticos = {
                "": "Selecione um diagnóstico...",
                
                # DEFICIÊNCIAS INTELECTUAIS E ATRASOS
                "F70 - Deficiência Intelectual Leve": "Deficiência intelectual leve (QI 50-69). Dificuldades na aprendizagem acadêmica, necessita suporte pedagógico individualizado. DSM-5: 317 (F70). Adaptações curriculares e atividades concretas são essenciais.",
                "F71 - Deficiência Intelectual Moderada": "Deficiência intelectual moderada (QI 35-49). Requer supervisão constante e apoio intensivo. DSM-5: 318.0 (F71). Necessita atividades funcionais e treino de habilidades de vida diária.",
                "F72 - Deficiência Intelectual Grave": "Deficiência intelectual grave (QI 20-34). Requer apoio contínuo e extensivo. DSM-5: 318.1 (F72). Foco em comunicação alternativa e autonomia básica.",
                "F79 - Deficiência Intelectual Não Especificada": "Deficiência intelectual não especificada. Diagnóstico em investigação. DSM-5: 319 (F79). Avaliação neuropsicológica em andamento.",
                
                # TRANSTORNOS DO ESPECTRO AUTISTA
                "F84.0 - Autismo Infantil (TEA Nível 3)": "Transtorno do Espectro Autista severo. Requer apoio muito substancial. DSM-5: 299.00 (F84.0). Déficits graves em comunicação e interação social, comportamentos repetitivos marcantes.",
                "F84.5 - Síndrome de Asperger (TEA Nível 1)": "TEA nível 1 sem déficit intelectual. Requer apoio. DSM-5: 299.00 (F84.5). Dificuldades na interação social, interesses restritos, linguagem preservada.",
                "F84.1 - Autismo Atípico": "TEA atípico. DSM-5: 299.00 (F84.1). Manifestações incompletas ou atípicas do autismo.",
                
                # TDAH
                "F90.0 - TDAH Tipo Predominantemente Desatento": "TDAH com predomínio de desatenção. DSM-5: 314.00 (F90.0). Dificuldade em manter foco, esquecimento frequente, desorganização. Responde bem a ambientes estruturados.",
                "F90.1 - TDAH Tipo Predominantemente Hiperativo-Impulsivo": "TDAH hiperativo-impulsivo. DSM-5: 314.01 (F90.1). Agitação motora, impulsividade, dificuldade em esperar. Necessita pausas e movimento.",
                "F90.2 - TDAH Tipo Combinado": "TDAH combinado. DSM-5: 314.01 (F90.2). Desatenção + hiperatividade/impulsividade. Requer manejo comportamental e medicação.",
                
                # DIFICULDADES ESPECÍFICAS DE APRENDIZAGEM
                "F81.0 - Transtorno Específico de Leitura (Dislexia)": "Dislexia. DSM-5: 315.00 (F81.0). Dificuldade na decodificação, fluência e compreensão leitora. Necessita método multissensorial e tempo extra.",
                "F81.1 - Transtorno Específico da Escrita (Disortografia)": "Disortografia. DSM-5: 315.2 (F81.1). Dificuldade na expressão escrita, ortografia, gramática. Requer treino sistemático e tecnologias assistivas.",
                "F81.2 - Transtorno Específico da Aritmética (Discalculia)": "Discalculia. DSM-5: 315.1 (F81.2). Dificuldade com números, cálculos, raciocínio matemático. Necessita materiais concretos e ensino explícito.",
                "F81.3 - Transtorno Misto de Habilidades Escolares": "Transtorno misto de aprendizagem. DSM-5: 315.8 (F81.3). Comprometimento em múltiplas áreas acadêmicas.",
                
                # DEFICIÊNCIAS SENSORIAIS
                "H90.3 - Perda Auditiva Neurossensorial Bilateral": "Deficiência auditiva bilateral. Necessita aparelho auditivo e/ou implante coclear. Beneficia-se de intérprete de Libras, professor bilíngue.",
                "H90.5 - Perda Auditiva Neurossensorial Unilateral": "Deficiência auditiva unilateral. Necessita adaptações na sala (posicionamento preferencial).",
                "H90.0 - Perda Auditiva Condutiva Bilateral": "Perda auditiva condutiva. Geralmente tratável. Necessita acompanhamento otorrinolaringológico.",
                "H54.0 - Cegueira Bilateral": "Cegueira. Necessita sistema Braille, audiodescrição, materiais táteis. Professor de AEE especializado.",
                "H54.4 - Baixa Visão Bilateral": "Baixa visão. Necessita materiais ampliados, alto contraste, boa iluminação, lupa eletrônica.",
                
                # DEFICIÊNCIAS FÍSICAS
                "G80.0 - Paralisia Cerebral Espástica": "Paralisia cerebral espástica. Rigidez muscular. Necessita fisioterapia, adaptações posturais, tecnologia assistiva.",
                "G80.1 - Paralisia Cerebral Diplégica Espástica": "Paralisia cerebral diplégica. Comprometimento de membros inferiores. Necessita órteses, cadeira de rodas.",
                "G80.3 - Paralisia Cerebral Discinética": "Paralisia cerebral discinética. Movimentos involuntários. Necessita comunicação alternativa.",
                "G82.1 - Paraplegia Flácida": "Paraplegia. Paralisia de membros inferiores. Necessita acessibilidade total, cadeira de rodas.",
                "M41.0 - Escoliose Idiopática Infantil": "Escoliose. Desvio da coluna. Necessita mobiliário adaptado, fisioterapia.",
                
                # TRANSTORNOS DE COMUNICAÇÃO
                "F80.0 - Transtorno Específico da Articulação da Fala": "Transtorno fonológico. DSM-5: 315.39 (F80.0). Dificuldade na produção dos sons da fala. Necessita fonoterapia.",
                "F80.1 - Transtorno Expressivo da Linguagem": "Transtorno da linguagem expressiva. DSM-5: 315.39 (F80.1). Dificuldade em expressar-se verbalmente.",
                "F80.2 - Transtorno Receptivo da Linguagem": "Transtorno da linguagem receptiva. DSM-5: 315.32 (F80.2). Dificuldade em compreender a linguagem.",
                "F80.81 - Gagueira Infantil": "Gagueira. DSM-5: 315.35 (F80.81). Disfluência da fala. Necessita fonoterapia, ambiente sem pressão.",
                
                # SÍNDROMES GENÉTICAS
                "Q90 - Síndrome de Down (Trissomia 21)": "Síndrome de Down. Deficiência intelectual variável, características físicas típicas. Necessita estimulação precoce, adaptações curriculares.",
                "Q93.5 - Síndrome de Cri-du-Chat": "Síndrome Cri-du-chat. Deficiência intelectual, choro característico. Necessita apoio intensivo.",
                "Q96 - Síndrome de Turner": "Síndrome de Turner. Baixa estatura, dificuldades específicas. Geralmente inteligência normal.",
                "Q87.1 - Síndrome de Prader-Willi": "Síndrome de Prader-Willi. Hiperfagia, obesidade, dificuldades cognitivas. Necessita controle alimentar.",
                
                # TRANSTORNOS EMOCIONAIS E COMPORTAMENTAIS
                "F41.1 - Transtorno de Ansiedade Generalizada": "TAG. DSM-5: 300.02 (F41.1). Ansiedade excessiva persistente. Responde a técnicas de relaxamento, terapia cognitivo-comportamental.",
                "F93.0 - Transtorno de Ansiedade de Separação": "Ansiedade de separação. DSM-5: 309.21 (F93.0). Angústia ao separar-se dos cuidadores. Comum em crianças pequenas.",
                "F40.10 - Fobia Social": "Fobia social. DSM-5: 300.23 (F40.10). Medo intenso de situações sociais. Necessita exposição gradual, suporte psicológico.",
                "F32 - Episódio Depressivo": "Depressão. DSM-5: 296.2x (F32.x). Tristeza persistente, perda de interesse. Requer acompanhamento psiquiátrico/psicológico.",
                "F91.1 - Transtorno de Conduta Não Socializado": "Transtorno de conduta. DSM-5: 312.81 (F91.1). Comportamento desafiador, agressividade. Necessita intervenção comportamental.",
                "F91.3 - Transtorno Desafiador Opositivo": "TOD. DSM-5: 313.81 (F91.3). Padrão de raiva, argumentação, desafio. Responde a limites claros e consistentes.",
                
                # TRANSTORNOS MOTORES
                "F82 - Transtorno do Desenvolvimento da Coordenação": "Dispraxia. DSM-5: 315.4 (F82). Dificuldade motora fina/grossa. Necessita terapia ocupacional, educação física adaptada.",
                "F95.2 - Síndrome de Tourette": "Síndrome de Tourette. DSM-5: 307.23 (F95.2). Tiques motores e vocais. Necessita compreensão, manejo de estresse.",
                
                # OUTROS TRANSTORNOS NEUROLÓGICOS
                "G40 - Epilepsia": "Epilepsia. Crises convulsivas. Necessita medicação regular, protocolo de emergência, evitar gatilhos (luzes piscantes).",
                "G43 - Enxaqueca": "Enxaqueca. Dores de cabeça intensas. Necessita ambiente calmo, iluminação adequada, pausas.",
                "G35 - Esclerose Múltipla": "Esclerose múltipla. Desmielinização. Fadiga, problemas motores. Necessita pausas, acessibilidade.",
                
                # TRANSTORNOS ALIMENTARES (mais comum em adolescentes)
                "F50.0 - Anorexia Nervosa": "Anorexia nervosa. DSM-5: 307.1 (F50.0). Restrição alimentar severa. Requer acompanhamento multidisciplinar urgente.",
                "F50.2 - Bulimia Nervosa": "Bulimia nervosa. DSM-5: 307.51 (F50.2). Compulsão alimentar seguida de purgação. Necessita tratamento especializado.",
                
                # TRANSTORNOS DO SONO
                "G47.0 - Insônia": "Insônia. Dificuldade para dormir. Afeta concentração e aprendizagem. Necessita higiene do sono.",
                
                # TRAUMA
                "F43.1 - Transtorno de Estresse Pós-Traumático": "TEPT. DSM-5: 309.81 (F43.1). Após evento traumático. Necessita ambiente seguro, psicoterapia especializada.",
                
                # OUTROS
                "F98.0 - Enurese Não Orgânica": "Enurese noturna. DSM-5: 307.6 (F98.0). Micção involuntária. Geralmente resolve espontaneamente.",
                "F98.1 - Encoprese Não Orgânica": "Encoprese. DSM-5: 307.7 (F98.1). Evacuação involuntária. Necessita avaliação médica.",
                "F94.0 - Mutismo Seletivo": "Mutismo seletivo. DSM-5: 312.23 (F94.0). Incapacidade de falar em situações específicas. Necessita paciência, não forçar.",
                "F63.3 - Tricotilomania": "Tricotilomania. DSM-5: 312.39 (F63.3). Arrancar cabelos compulsivamente. Necessita terapia comportamental.",
            }
            
            cid_10_dsm5 = st.selectbox("CID-10 / DSM-5", list(diagnosticos.keys()))
            
            if cid_10_dsm5 and cid_10_dsm5 != "":
                st.text_area("📋 Descrição e Orientações", 
                           value=diagnosticos[cid_10_dsm5], 
                           height=150, 
                           disabled=True,
                           key="descricao_diagnostico")
            
            st.markdown("---")
            st.markdown("**5.2.2 Medicação**")
            
            col1, col2 = st.columns(2)
            with col1:
                medicacao_uso = st.selectbox("Faz uso de medicação?", ["", "Não", "Sim"])
                
            if medicacao_uso == "Sim":
                with col2:
                    nome_medicacao = st.text_input("Nome da Medicação", max_chars=200, 
                                                   placeholder="Ex: Metilfenidato, Risperidona, etc.")
                
                col1, col2 = st.columns(2)
                with col1:
                    dosagem_medicacao = st.text_input("Dosagem", max_chars=100, 
                                                     placeholder="Ex: 10mg, 2x ao dia")
                    horario_medicacao = st.text_input("Horário de Administração", max_chars=100,
                                                     placeholder="Ex: 8h e 14h")
                
                with col2:
                    medico_responsavel = st.text_input("Médico Responsável", max_chars=100)
                    crm_medico = st.text_input("CRM do Médico", max_chars=20)
                
                efeitos_esperados = st.text_area(
                    "Efeitos Esperados da Medicação", 
                    max_chars=500,
                    height=100,
                    placeholder="Descreva os efeitos esperados (ex: melhora na atenção, redução de ansiedade, controle de crises, etc.)"
                )
                
                efeitos_colaterais = st.text_area(
                    "Possíveis Efeitos Colaterais a Observar",
                    max_chars=500,
                    height=100,
                    placeholder="Descreva efeitos colaterais que a escola deve observar (ex: sonolência, irritabilidade, perda de apetite, etc.)"
                )
            else:
                # Valores vazios se não usa medicação
                nome_medicacao = ""
                dosagem_medicacao = ""
                horario_medicacao = ""
                medico_responsavel = ""
                crm_medico = ""
                efeitos_esperados = ""
                efeitos_colaterais = ""
        else:
            # Valores vazios se não tem deficiência
            cid_10_dsm5 = ""
            medicacao_uso = ""
            nome_medicacao = ""
            dosagem_medicacao = ""
            horario_medicacao = ""
            medico_responsavel = ""
            crm_medico = ""
            efeitos_esperados = ""
            efeitos_colaterais = ""
        
        st.markdown("**5.3 Recursos Necessários (SAEB/Prova Brasil)**")
        recursos_saeb = st.multiselect("Selecione recursos necessários:", [
            "Prova ampliada (fonte 18)",
            "Prova superampliada (fonte 24)",
            "Prova em Braille",
            "Prova em Libras",
            "Leitura labial",
            "Intérprete de Libras",
            "Ledor",
            "Transcrição",
            "Guia intérprete",
            "Sala de recursos",
            "Tempo adicional",
            "Nenhum"
        ])
        
        st.markdown("**5.4 Escolarização em Outro Espaço**")
        escolarizacao_outro_espaco = st.text_input("Recebe escolarização em outro local? Qual?", max_chars=200)
        
        # 6. PROGRAMAS, RENDIMENTO E MOVIMENTO
        st.markdown("---")
        st.subheader("6. 📚 Programas, Rendimento e Movimento")
        
        st.markdown("**6.1 Programas Educacionais Frequentados**")
        programas_educacionais = st.multiselect("Programas:", [
            "Mais Educação",
            "Tempo Integral",
            "Reforço Escolar",
            "Contraturno",
            "Nenhum"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**6.2 Rendimento do Ano Anterior**")
            rendimento_ano_anterior = st.selectbox("Situação:", [
                "", "Aprovado", "Reprovado", "Transferido", "Abandonou", "Outra situação", "Não se aplica (1º ano)"
            ])
        
        with col2:
            st.markdown("**6.3 Movimento Escolar**")
            movimento_escolar = st.selectbox("Classificação:", [
                "", "Novato", "Remanescente", "Transferido", "Remanejado", "Outro"
            ])
        
        st.markdown("**6.4 Escola do Ano Anterior**")
        escola_origem = st.text_input("Nome da Escola de Origem", max_chars=100)
        escola_ano_anterior = st.text_input("Escola em que estudou no ano anterior", max_chars=100)
        
        # Dados Escolares Atuais
        st.markdown("---")
        st.subheader("📖 Dados Escolares 2025")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            ano_escolar = st.selectbox("Ano Escolar *", [
                "", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                "6º Ano", "7º Ano", "8º Ano", "9º Ano"
            ])
        with col2:
            turno = st.selectbox("Turno *", ["", "Matutino", "Vespertino", "Integral"])
        with col3:
            status = st.selectbox("Status *", ["", "Ativo", "Aguardando Documentação", "Cancelado"])
        
        # 7. TRANSPORTE ESCOLAR
        st.markdown("---")
        st.subheader("7. 🚌 Transporte Escolar")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            utiliza_transporte = st.selectbox("Utiliza Transporte Escolar?", ["", "Não", "Sim"])
        with col2:
            poder_responsavel_transporte = st.selectbox("Poder Responsável", [
                "", "Municipal", "Estadual", "Particular", "Não se aplica"
            ])
        with col3:
            tipo_veiculo = st.selectbox("Tipo de Veículo", [
                "", "Ônibus", "Van", "Micro-ônibus", "Transporte aquático", "Outros", "Não se aplica"
            ])
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Cadastro Completo", use_container_width=True)
        
        if submitted:
            # Validação de campos obrigatórios
            erros = []
            
            if not nome_completo:
                erros.append("Nome completo é obrigatório")
            if not cpf:
                erros.append("CPF é obrigatório")
            if not sexo:
                erros.append("Sexo é obrigatório")
            if not nome_mae:
                erros.append("Nome da mãe é obrigatório")
            if not telefone:
                erros.append("Telefone é obrigatório")
            if not cep:
                erros.append("CEP é obrigatório")
            if not bairro:
                erros.append("Bairro é obrigatório")
            if not endereco:
                erros.append("Endereço é obrigatório")
            if not numero:
                erros.append("Número é obrigatório")
            if not uf:
                erros.append("UF é obrigatório")
            if not cidade:
                erros.append("Cidade é obrigatória")
            if not ano_escolar:
                erros.append("Ano escolar é obrigatório")
            if not turno:
                erros.append("Turno é obrigatório")
            if not status:
                erros.append("Status é obrigatório")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Processar foto se fornecida
                foto_path = ""
                if foto is not None:
                    try:
                        # Criar diretório de fotos se não existir
                        fotos_dir = os.path.join('data', 'fotos')
                        os.makedirs(fotos_dir, exist_ok=True)
                        
                        # Gerar ID temporário para o nome da foto
                        df_temp = data_manager.get_data('cadastro')
                        if len(df_temp) == 0:
                            temp_id = 1
                        else:
                            temp_id = df_temp['id'].max() + 1
                        
                        # Abrir e redimensionar imagem para tamanho padrão (3x4)
                        img = Image.open(foto)
                        # Redimensionar mantendo proporção para 300x400 pixels (3x4)
                        img.thumbnail((300, 400), Image.Resampling.LANCZOS)
                        
                        # Salvar foto com nome único
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        foto_filename = f"{temp_id}_{timestamp}.jpg"
                        foto_path = os.path.join(fotos_dir, foto_filename)
                        
                        # Converter para RGB se necessário (para salvar como JPEG)
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')
                        
                        img.save(foto_path, 'JPEG', quality=85)
                        st.success(f"✅ Foto salva com sucesso!")
                    except Exception as e:
                        st.warning(f"⚠️ Erro ao salvar foto: {str(e)}. Cadastro será salvo sem foto.")
                        foto_path = ""
                
                # Converter lista de recursos para string
                recursos_saeb_str = ", ".join(recursos_saeb) if recursos_saeb else ""
                programas_educacionais_str = ", ".join(programas_educacionais) if programas_educacionais else ""
                
                # Preparar dados para salvar
                dados = {
                    # Identificação
                    'nome_completo': nome_completo,
                    'nome_social': nome_social,
                    'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                    'cpf': cpf,
                    'codigo_inep': codigo_inep,
                    'matricula': matricula,
                    'sexo': sexo,
                    'cor_raca': cor_raca,
                    'telefone': telefone,
                    'email': email,
                    'nis': nis,
                    # Nacionalidade
                    'nacionalidade': nacionalidade,
                    'uf_nascimento': uf_nascimento,
                    'cidade_nascimento': cidade_nascimento,
                    'pais_nacionalidade': pais_nacionalidade,
                    # Filiação
                    'nome_mae': nome_mae,
                    'cpf_mae': cpf_mae,
                    'profissao_mae': profissao_mae,
                    'nome_pai': nome_pai,
                    'cpf_pai': cpf_pai,
                    'profissao_pai': profissao_pai,
                    # Documentação
                    'rg': rg,
                    'numero_documento': numero_documento,
                    'orgao_emissor': orgao_emissor,
                    'uf_emissor': uf_emissor,
                    'data_expedicao': data_expedicao.strftime('%Y-%m-%d') if data_expedicao else '',
                    'modelo_certidao': modelo_certidao,
                    'tipo_certidao': tipo_certidao,
                    'cartao_sus': cartao_sus,
                    'documento_estrangeiro': documento_estrangeiro,
                    'justificativa_documentacao': justificativa_documentacao,
                    # Endereço
                    'cep': cep,
                    'bairro': bairro,
                    'endereco': endereco,
                    'numero': numero,
                    'complemento': complemento,
                    'zona': zona,
                    'uf': uf,
                    'cidade': cidade,
                    # Saúde
                    'cartao_nacional_sus': cartao_nacional_sus,
                    'alergia': alergia,
                    'aluno_deficiencia': aluno_deficiencia,
                    'possui_laudo_medico': possui_laudo_medico,
                    'tipo_deficiencia': tipo_deficiencia,
                    'atendimentos_especializados': atendimentos_especializados,
                    'recursos_saeb': recursos_saeb_str,
                    'escolarizacao_outro_espaco': escolarizacao_outro_espaco,
                    # Informações médicas detalhadas
                    'cid_10_dsm5': cid_10_dsm5,
                    'medicacao_uso': medicacao_uso,
                    'nome_medicacao': nome_medicacao,
                    'dosagem_medicacao': dosagem_medicacao,
                    'horario_medicacao': horario_medicacao,
                    'medico_responsavel': medico_responsavel,
                    'crm_medico': crm_medico,
                    'efeitos_esperados': efeitos_esperados,
                    'efeitos_colaterais': efeitos_colaterais,
                    # Histórico escolar
                    'escola_origem': escola_origem,
                    'escola_ano_anterior': escola_ano_anterior,
                    'programas_educacionais': programas_educacionais_str,
                    'rendimento_ano_anterior': rendimento_ano_anterior,
                    'movimento_escolar': movimento_escolar,
                    # Dados escolares atuais
                    'ano_escolar': ano_escolar,
                    'turno': turno,
                    'status': status,
                    # Transporte
                    'utiliza_transporte': utiliza_transporte,
                    'poder_responsavel_transporte': poder_responsavel_transporte,
                    'tipo_veiculo': tipo_veiculo,
                    # Metadados
                    'foto_path': foto_path
                }
                
                try:
                    novo_id = data_manager.add_record('cadastro', dados)
                    st.success(f"✅ Cadastro completo realizado com sucesso! ID do aluno: {novo_id}")
                    st.balloons()
                    st.info("📋 Todos os dados foram salvos. Você pode visualizar na Lista de Alunos.")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar cadastro: {str(e)}")

def render_lista_alunos(data_manager):
    """Renderiza lista de alunos cadastrados"""
    st.header("👥 Lista de Alunos")
    
    df = data_manager.get_data('cadastro')
    
    if len(df) == 0:
        st.info("Nenhum aluno cadastrado ainda.")
        return
    
    # Obter dados do PEI para verificar alunos especiais
    df_pei = data_manager.get_data('pei')
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_status = st.selectbox("Filtrar por Status", 
                                     ["Todos"] + list(df['status'].unique()))
    
    with col2:
        filtro_ano = st.selectbox("Filtrar por Ano Escolar", 
                                  ["Todos"] + list(df['ano_escolar'].unique()))
    
    with col3:
        filtro_turno = st.selectbox("Filtrar por Turno", 
                                    ["Todos"] + list(df['turno'].unique()))
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]
    
    if filtro_ano != "Todos":
        df_filtrado = df_filtrado[df_filtrado['ano_escolar'] == filtro_ano]
    
    if filtro_turno != "Todos":
        df_filtrado = df_filtrado[df_filtrado['turno'] == filtro_turno]
    
    # Adicionar coluna de responsáveis
    df_filtrado['responsaveis'] = df_filtrado.apply(
        lambda row: (
            f"{row['nome_mae']}" + 
            (f" / {row['nome_pai']}" if pd.notna(row.get('nome_pai')) and str(row['nome_pai']).strip() != '' else "")
        ) if pd.notna(row.get('nome_mae')) else "Não informado",
        axis=1
    )
    
    # Adicionar coluna de endereço completo
    df_filtrado['endereco_completo'] = df_filtrado.apply(
        lambda row: f"{row['endereco']}, {row['numero']}" + 
                   (f" - {row['complemento']}" if row['complemento'] and str(row['complemento']).strip() != '' else "") +
                   f" - {row['bairro']}, {row['cidade']}/{row['uf']}",
        axis=1
    )
    
    # Adicionar coluna indicando se é aluno especial com PEI
    # Verifica tanto o campo aluno_deficiencia do cadastro quanto registros PEI
    if len(df_pei) > 0:
        # Criar dicionário de alunos com PEI registrado
        alunos_com_pei = {}
        for _, pei_row in df_pei.iterrows():
            try:
                if pei_row['necessidade_especial'] == 'Sim':
                    aluno_id = int(pei_row['aluno_id'])
                    alunos_com_pei[aluno_id] = 'Sim'
            except (ValueError, TypeError):
                # Ignora registros com IDs inválidos
                continue
        
        # Combina informação do cadastro e do PEI
        def determinar_especial_pei(row):
            id_aluno = row['id']
            # Verifica se tem deficiência no cadastro OU tem registro PEI
            tem_deficiencia_cadastro = (
                pd.notna(row.get('aluno_deficiencia')) and 
                row.get('aluno_deficiencia') == 'Sim'
            )
            tem_pei_registrado = (
                pd.notna(id_aluno) and 
                str(id_aluno).isdigit() and 
                alunos_com_pei.get(int(id_aluno), 'Não') == 'Sim'
            )
            return 'Sim' if (tem_deficiencia_cadastro or tem_pei_registrado) else 'Não'
        
        df_filtrado['aluno_especial_pei'] = df_filtrado.apply(determinar_especial_pei, axis=1)
    else:
        # Se não há registros PEI, verifica apenas o campo do cadastro
        df_filtrado['aluno_especial_pei'] = df_filtrado.apply(
            lambda row: 'Sim' if (pd.notna(row.get('aluno_deficiencia')) and row.get('aluno_deficiencia') == 'Sim') else 'Não',
            axis=1
        )
    
    # Mostrar dados
    st.markdown(f"**Total de alunos:** {len(df_filtrado)}")
    
    # Selecionar colunas para exibição
    colunas_exibir = ['id', 'nome_completo', 'responsaveis', 'endereco_completo', 
                      'ano_escolar', 'turno', 'telefone', 'aluno_especial_pei', 'status']
    
    st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)
    
    # Botões para exportação em lote
    st.markdown("---")
    st.subheader("📊 Exportar Lista de Alunos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exportar JSON", use_container_width=True, key="btn_export_json"):
            try:
                import json
                
                # Preparar dados para JSON
                json_data = df_filtrado.to_dict(orient='records')
                
                # Converter para JSON string
                json_str = json.dumps(json_data, ensure_ascii=False, indent=2, default=str)
                
                # Nome do arquivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nome_arquivo = f"lista_alunos_{timestamp}.json"
                
                st.download_button(
                    label="📥 Baixar JSON",
                    data=json_str,
                    file_name=nome_arquivo,
                    mime="application/json",
                    use_container_width=True,
                    key="download_json"
                )
                st.success("✅ JSON gerado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao gerar JSON: {str(e)}")
    
    with col2:
        if st.button("📄 Gerar PDFs em Lote", use_container_width=True, key="btn_bulk_pdf"):
            if len(df_filtrado) == 0:
                st.warning("⚠️ Nenhum aluno na lista filtrada")
            else:
                with st.spinner(f"Gerando {len(df_filtrado)} PDFs..."):
                    try:
                        import zipfile
                        from . import pdf_generator
                        
                        # Criar ZIP em memória
                        zip_buffer = io.BytesIO()
                        
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            for _, row in df_filtrado.iterrows():
                                aluno_id = int(row['id'])
                                
                                # Gerar PDF
                                pdf_buffer = pdf_generator.gerar_pdf_aluno(
                                    data_manager,
                                    aluno_id,
                                    incluir_pei=True,
                                    incluir_anamnese=True,
                                    incluir_socio=True,
                                    incluir_saeb=True,
                                    incluir_saude=True
                                )
                                
                                if pdf_buffer:
                                    # Sanitizar nome
                                    nome_limpo = "".join(c for c in row['nome_completo'] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
                                    pdf_filename = f"ficha_{aluno_id}_{nome_limpo}.pdf"
                                    
                                    # Adicionar ao ZIP
                                    zipf.writestr(pdf_filename, pdf_buffer)
                        
                        zip_buffer.seek(0)
                        
                        # Nome do arquivo ZIP
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        nome_arquivo_zip = f"fichas_alunos_{timestamp}.zip"
                        
                        st.download_button(
                            label="📥 Baixar ZIP com PDFs",
                            data=zip_buffer.getvalue(),
                            file_name=nome_arquivo_zip,
                            mime="application/zip",
                            use_container_width=True,
                            key="download_zip_bulk"
                        )
                        st.success(f"✅ {len(df_filtrado)} PDFs gerados com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar PDFs: {str(e)}")
    
    with col3:
        if st.button("📦 Exportar PDF+JSON", use_container_width=True, key="btn_export_all"):
            if len(df_filtrado) == 0:
                st.warning("⚠️ Nenhum aluno na lista filtrada")
            else:
                with st.spinner(f"Gerando exportação completa..."):
                    try:
                        import zipfile
                        import json
                        from . import pdf_generator
                        
                        # Criar ZIP em memória
                        zip_buffer = io.BytesIO()
                        
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            # Adicionar PDFs
                            for _, row in df_filtrado.iterrows():
                                aluno_id = int(row['id'])
                                
                                # Gerar PDF
                                pdf_buffer = pdf_generator.gerar_pdf_aluno(
                                    data_manager,
                                    aluno_id,
                                    incluir_pei=True,
                                    incluir_anamnese=True,
                                    incluir_socio=True,
                                    incluir_saeb=True,
                                    incluir_saude=True
                                )
                                
                                if pdf_buffer:
                                    # Sanitizar nome
                                    nome_limpo = "".join(c for c in row['nome_completo'] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
                                    pdf_filename = f"pdfs/ficha_{aluno_id}_{nome_limpo}.pdf"
                                    
                                    # Adicionar ao ZIP
                                    zipf.writestr(pdf_filename, pdf_buffer)
                            
                            # Adicionar JSON com dados completos
                            json_data = df_filtrado.to_dict(orient='records')
                            json_str = json.dumps(json_data, ensure_ascii=False, indent=2, default=str)
                            zipf.writestr('dados/lista_alunos.json', json_str)
                            
                            # Adicionar README
                            readme_content = f"""EXPORTAÇÃO DE DADOS - LISTA DE ALUNOS
                            
Data de Exportação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Total de Alunos: {len(df_filtrado)}

CONTEÚDO:
- pdfs/ - Contém {len(df_filtrado)} fichas de matrícula em PDF
- dados/ - Contém arquivo JSON com todos os dados dos alunos

Para visualizar os dados JSON, abra o arquivo lista_alunos.json em um editor de texto ou navegador web.
"""
                            zipf.writestr('README.txt', readme_content)
                        
                        zip_buffer.seek(0)
                        
                        # Nome do arquivo ZIP
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        nome_arquivo_zip = f"exportacao_completa_{timestamp}.zip"
                        
                        st.download_button(
                            label="📥 Baixar Exportação Completa",
                            data=zip_buffer.getvalue(),
                            file_name=nome_arquivo_zip,
                            mime="application/zip",
                            use_container_width=True,
                            key="download_complete_export"
                        )
                        st.success(f"✅ Exportação completa gerada com sucesso! ({len(df_filtrado)} alunos)")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar exportação: {str(e)}")
    
    # Botão para gerar PDF da lista
    st.markdown("---")
    st.subheader("📄 Gerar PDF Individual")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # Seletor de aluno para gerar PDF
        alunos_pdf = ["Selecione um aluno para gerar PDF"] + [
            f"{row['id']} - {row['nome_completo']}" 
            for _, row in df_filtrado.iterrows()
        ]
        aluno_pdf_selecionado = st.selectbox("Aluno:", alunos_pdf, key="pdf_lista")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacer
        gerar_pdf_button = st.button("🖨️ Gerar PDF", use_container_width=True, key="btn_pdf_lista")
    
    if gerar_pdf_button and aluno_pdf_selecionado != "Selecione um aluno para gerar PDF":
        try:
            aluno_id_pdf = int(aluno_pdf_selecionado.split(" - ")[0])
        except (ValueError, IndexError):
            st.error("❌ Formato de seleção inválido")
            return
        
        with st.spinner("Gerando PDF..."):
            try:
                # Import necessário
                from . import pdf_generator
                
                # Gerar PDF com todas as seções
                pdf_buffer = pdf_generator.gerar_pdf_aluno(
                    data_manager, 
                    aluno_id_pdf,
                    incluir_pei=True,
                    incluir_anamnese=True,
                    incluir_socio=True,
                    incluir_saeb=True,
                    incluir_saude=True
                )
                
                if pdf_buffer:
                    st.success("✅ PDF gerado com sucesso!")
                    
                    # Obter dados do aluno para nome do arquivo
                    aluno_data = data_manager.get_record('cadastro', aluno_id_pdf)
                    # Sanitizar nome do arquivo removendo caracteres especiais
                    nome_limpo = "".join(c for c in aluno_data['nome_completo'] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
                    nome_arquivo = f"ficha_matricula_{nome_limpo}_{aluno_id_pdf}.pdf"
                    
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf_buffer,
                        file_name=nome_arquivo,
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_pdf_lista"
                    )
                else:
                    st.error("❌ Erro ao gerar PDF")
                    
            except Exception as e:
                st.error(f"❌ Erro ao gerar PDF: {str(e)}")
    elif gerar_pdf_button:
        st.warning("⚠️ Selecione um aluno para gerar o PDF")
