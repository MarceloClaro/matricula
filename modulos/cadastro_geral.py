"""
Módulo de Cadastro Geral de Alunos
"""
import streamlit as st
import pandas as pd
from datetime import datetime

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
                    # TODO: Implementar salvamento real de foto em diretório específico
                    # Por enquanto, deixa vazio para evitar referências incorretas
                    foto_path = ""
                    st.info("ℹ️ Upload de foto será implementado em versão futura.")
                
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
