"""
Módulo de Geração de PDF Individual
"""
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import os

def render_pdf_generator(data_manager):
    """Renderiza interface para gerar PDF individual"""
    st.header("📄 Geração de PDF Individual")
    st.markdown("---")
    
    # Selecionar aluno
    df_alunos = data_manager.get_data('cadastro')
    
    if len(df_alunos) == 0:
        st.warning("⚠️ Não há alunos cadastrados.")
        return
    
    alunos_opcoes = ["Selecione um aluno"] + [
        f"{row['id']} - {row['nome_completo']}" 
        for _, row in df_alunos.iterrows()
    ]
    
    aluno_selecionado = st.selectbox("Selecione o aluno", alunos_opcoes)
    
    if aluno_selecionado == "Selecione um aluno":
        st.info("Selecione um aluno para gerar o PDF da ficha de matrícula")
        return
    
    aluno_id = int(aluno_selecionado.split(" - ")[0])
    
    # Opções de seções
    st.subheader("Seções a incluir no PDF")
    
    col1, col2 = st.columns(2)
    
    with col1:
        incluir_cadastro = st.checkbox("Cadastro Geral", value=True, disabled=True)
        incluir_pei = st.checkbox("PEI", value=True)
        incluir_anamnese = st.checkbox("🧠 Anamnese Pedagógica (PEI)", value=True)
    
    with col2:
        incluir_socio = st.checkbox("Socioeconômico", value=True)
        incluir_saeb = st.checkbox("📋 Questionário SAEB", value=True)
        incluir_saude = st.checkbox("Saúde", value=True)
    
    # Botão para gerar PDF
    if st.button("📄 Gerar PDF", use_container_width=True):
        with st.spinner("Gerando PDF..."):
            try:
                pdf_buffer = gerar_pdf_aluno(
                    data_manager, 
                    aluno_id,
                    incluir_pei,
                    incluir_anamnese,
                    incluir_socio,
                    incluir_saeb,
                    incluir_saude
                )
                
                if pdf_buffer:
                    st.success("✅ PDF gerado com sucesso!")
                    
                    # Obter dados do aluno para nome do arquivo
                    aluno = data_manager.get_record('cadastro', aluno_id)
                    # Sanitizar nome do arquivo removendo caracteres especiais
                    nome_limpo = "".join(c for c in aluno['nome_completo'] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
                    nome_arquivo = f"ficha_matricula_{nome_limpo}_{aluno_id}.pdf"
                    
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf_buffer,
                        file_name=nome_arquivo,
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error("Erro ao gerar PDF")
            
            except Exception as e:
                st.error(f"❌ Erro ao gerar PDF: {str(e)}")

def gerar_pdf_aluno(data_manager, aluno_id, incluir_pei=True, incluir_anamnese=True, incluir_socio=True, incluir_saeb=True, incluir_saude=True):
    """Gera PDF completo da ficha do aluno"""
    buffer = io.BytesIO()
    
    # Criar documento
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    # Container para elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    # Título
    elements.append(Paragraph("FICHA DE MATRÍCULA ESCOLAR 2026", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Dados do Cadastro Geral
    cadastro = data_manager.get_record('cadastro', aluno_id)
    
    if cadastro:
        # Adicionar foto se disponível
        foto_path = cadastro.get('foto_path', '')
        if foto_path and os.path.exists(foto_path):
            try:
                # Criar tabela com foto e informações básicas lado a lado
                foto_img = RLImage(foto_path, width=3*cm, height=4*cm)
                
                # Dados básicos para exibir ao lado da foto
                dados_basicos_texto = f"""
                <b>ID:</b> {cadastro.get('id', '')}<br/>
                <b>Nome:</b> {cadastro.get('nome_completo', '')}<br/>
                <b>CPF:</b> {cadastro.get('cpf', '')}<br/>
                <b>Data Nasc.:</b> {cadastro.get('data_nascimento', '')}<br/>
                <b>Matrícula:</b> {cadastro.get('data_matricula', '')}
                """
                
                info_style = ParagraphStyle(
                    'InfoStyle',
                    parent=styles['Normal'],
                    fontSize=9,
                    leading=12
                )
                
                dados_basicos_para = Paragraph(dados_basicos_texto, info_style)
                
                # Tabela com foto e dados básicos
                foto_table = Table([[foto_img, dados_basicos_para]], colWidths=[3.5*cm, 15*cm])
                foto_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                elements.append(foto_table)
                elements.append(Spacer(1, 0.3*cm))
            except Exception as e:
                # Se houver erro ao carregar foto, continua sem ela
                pass
        
        elements.append(Paragraph("DADOS PESSOAIS", heading_style))
        
        dados_pessoais = [
            ['ID:', str(cadastro.get('id', '')), 'Data da Matrícula:', cadastro.get('data_matricula', '')],
            ['Nome Completo:', cadastro.get('nome_completo', ''), '', ''],
            ['Data de Nascimento:', cadastro.get('data_nascimento', ''), 'CPF:', cadastro.get('cpf', '')],
            ['RG:', cadastro.get('rg', ''), '', ''],
            ['Nome da Mãe:', cadastro.get('nome_mae', ''), '', ''],
            ['Nome do Pai:', cadastro.get('nome_pai', ''), '', ''],
        ]
        
        table = Table(dados_pessoais, colWidths=[4*cm, 7*cm, 3.5*cm, 4*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f4f8')),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Contato
        elements.append(Paragraph("CONTATO", heading_style))
        
        dados_contato = [
            ['Telefone:', cadastro.get('telefone', ''), 'E-mail:', cadastro.get('email', '')],
        ]
        
        table = Table(dados_contato, colWidths=[3*cm, 6*cm, 3*cm, 6.5*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f4f8')),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Endereço
        elements.append(Paragraph("ENDEREÇO", heading_style))
        
        dados_endereco = [
            ['Logradouro:', cadastro.get('endereco', ''), 'Número:', cadastro.get('numero', '')],
            ['Complemento:', cadastro.get('complemento', ''), 'Bairro:', cadastro.get('bairro', '')],
            ['Cidade:', cadastro.get('cidade', ''), 'UF:', cadastro.get('uf', '')],
            ['CEP:', cadastro.get('cep', ''), '', ''],
        ]
        
        table = Table(dados_endereco, colWidths=[3*cm, 9*cm, 2*cm, 4.5*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f4f8')),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Dados Escolares
        elements.append(Paragraph("DADOS ESCOLARES", heading_style))
        
        dados_escolares = [
            ['Escola de Origem:', cadastro.get('escola_origem', ''), '', ''],
            ['Ano Escolar:', cadastro.get('ano_escolar', ''), 'Turno:', cadastro.get('turno', '')],
            ['Status:', cadastro.get('status', ''), '', ''],
        ]
        
        table = Table(dados_escolares, colWidths=[4*cm, 7*cm, 2*cm, 5.5*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f4f8')),
        ]))
        elements.append(table)
        
        # Informações Médicas (se aluno tem deficiência)
        if cadastro.get('aluno_deficiencia') == 'Sim':
            elements.append(Spacer(1, 0.5*cm))
            elements.append(Paragraph("INFORMAÇÕES MÉDICAS E DIAGNÓSTICO", heading_style))
            
            dados_medicos = [
                ['Aluno com Deficiência:', 'Sim'],
                ['Tipo de Deficiência:', cadastro.get('tipo_deficiencia', '')],
                ['Possui Laudo Médico:', cadastro.get('possui_laudo_medico', '')],
            ]
            
            # Adicionar CID-10/DSM-5 se disponível
            cid_dsm = cadastro.get('cid_10_dsm5', '')
            if cid_dsm and cid_dsm.strip():
                dados_medicos.append(['CID-10 / DSM-5:', cid_dsm])
            
            # Informações de medicação
            if cadastro.get('medicacao_uso') == 'Sim':
                dados_medicos.extend([
                    ['─────────────────', '──────────────────────────'],  # Linha separadora
                    ['Medicação em Uso:', 'Sim'],
                    ['Nome da Medicação:', cadastro.get('nome_medicacao', '')],
                    ['Dosagem:', cadastro.get('dosagem_medicacao', '')],
                    ['Horário:', cadastro.get('horario_medicacao', '')],
                    ['Médico Responsável:', cadastro.get('medico_responsavel', '')],
                    ['CRM:', cadastro.get('crm_medico', '')],
                ])
                
                # Efeitos esperados
                efeitos_esp = cadastro.get('efeitos_esperados', '')
                if efeitos_esp and efeitos_esp.strip():
                    dados_medicos.append(['Efeitos Esperados:', efeitos_esp])
                
                # Efeitos colaterais
                efeitos_col = cadastro.get('efeitos_colaterais', '')
                if efeitos_col and efeitos_col.strip():
                    dados_medicos.append(['Efeitos Colaterais:', efeitos_col])
            
            # Atendimentos e recursos
            dados_medicos.extend([
                ['─────────────────', '──────────────────────────'],  # Linha separadora
                ['Atendimentos Especializados:', cadastro.get('atendimentos_especializados', '')],
                ['Recursos SAEB:', cadastro.get('recursos_saeb', '')],
            ])
            
            table = Table(dados_medicos, colWidths=[5.5*cm, 13*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e0')),
            ]))
            elements.append(table)
    
    # PEI
    if incluir_pei:
        df_pei = data_manager.get_data('pei')
        pei = df_pei[df_pei['aluno_id'] == aluno_id]
        
        if len(pei) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("PLANO EDUCACIONAL INDIVIDUALIZADO (PEI)", heading_style))
            
            pei_data = pei.iloc[0].to_dict()
            
            dados_pei = [
                ['Necessidade Especial:', pei_data.get('necessidade_especial', '')],
                ['Tipo de Deficiência:', pei_data.get('tipo_deficiencia', '')],
                ['Possui Laudo Médico:', pei_data.get('laudo_medico', '')],
                ['Data do Laudo:', pei_data.get('data_laudo', '')],
                ['CID:', pei_data.get('cid', '')],
                ['Medicação:', pei_data.get('medicacao', '')],
                ['Restrições:', pei_data.get('restricoes', '')],
                ['Apoio Necessário:', pei_data.get('apoio_necessario', '')],
                ['Adaptação Curricular:', pei_data.get('adaptacao_curricular', '')],
                ['Acompanhamento Especializado:', pei_data.get('acompanhamento_especializado', '')],
                ['Recursos Necessários:', pei_data.get('recursos_necessarios', '')],
                ['Observações:', pei_data.get('observacoes', '')],
            ]
            
            table = Table(dados_pei, colWidths=[6*cm, 12.5*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff4e6')),
            ]))
            elements.append(table)
    
    # Socioeconômico
    if incluir_socio:
        df_socio = data_manager.get_data('socioeconomico')
        socio = df_socio[df_socio['aluno_id'] == aluno_id]
        
        if len(socio) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("QUESTIONÁRIO SOCIOECONÔMICO", heading_style))
            
            socio_data = socio.iloc[0].to_dict()
            
            dados_socio = [
                ['Renda Familiar:', socio_data.get('renda_familiar', '')],
                ['Pessoas na Residência:', str(socio_data.get('qtd_pessoas_casa', ''))],
                ['Tipo de Moradia:', socio_data.get('tipo_moradia', '')],
                ['Possui Internet:', socio_data.get('possui_internet', '')],
                ['Possui Computador:', socio_data.get('possui_computador', '')],
                ['Possui Smartphone:', socio_data.get('possui_smartphone', '')],
                ['Bolsa Família:', socio_data.get('bolsa_familia', '')],
                ['Auxílio Brasil:', socio_data.get('auxilio_brasil', '')],
                ['Outro Benefício Social:', socio_data.get('beneficio_social', '')],
                ['Situação de Trabalho:', socio_data.get('situacao_trabalho_responsavel', '')],
                ['Profissão do Responsável:', socio_data.get('profissao_responsavel', '')],
                ['Escolaridade da Mãe:', socio_data.get('escolaridade_mae', '')],
                ['Escolaridade do Pai:', socio_data.get('escolaridade_pai', '')],
                ['Transporte Escolar:', socio_data.get('transporte_escolar', '')],
                ['Tempo de Deslocamento:', socio_data.get('tempo_deslocamento', '')],
            ]
            
            table = Table(dados_socio, colWidths=[6*cm, 12.5*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
            ]))
            elements.append(table)
    
    # Saúde
    if incluir_saude:
        df_saude = data_manager.get_data('saude')
        saude = df_saude[df_saude['aluno_id'] == aluno_id]
        
        if len(saude) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("FICHA DE SAÚDE", heading_style))
            
            saude_data = saude.iloc[0].to_dict()
            
            dados_saude = [
                ['Tipo Sanguíneo:', saude_data.get('tipo_sanguineo', '')],
                ['Fator RH:', saude_data.get('fator_rh', '')],
                ['Alergias:', saude_data.get('alergias', '')],
                ['Doenças Crônicas:', saude_data.get('doencas_cronicas', '')],
                ['Medicamentos de Uso Contínuo:', saude_data.get('medicamentos_uso_continuo', '')],
                ['Histórico de Doenças:', saude_data.get('historico_doencas', '')],
                ['Vacinação em Dia:', saude_data.get('vacinacao_em_dia', '')],
                ['Possui Plano de Saúde:', saude_data.get('plano_saude', '')],
                ['Nome do Plano:', saude_data.get('nome_plano_saude', '')],
                ['Número da Carteirinha:', saude_data.get('numero_plano', '')],
                ['Contato de Emergência:', saude_data.get('contato_emergencia', '')],
                ['Telefone de Emergência:', saude_data.get('telefone_emergencia', '')],
                ['Parentesco:', saude_data.get('parentesco_emergencia', '')],
                ['Observações:', saude_data.get('observacoes_saude', '')],
            ]
            
            table = Table(dados_saude, colWidths=[6*cm, 12.5*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ffebee')),
            ]))
            elements.append(table)
    
    # Anamnese Pedagógica (PEI)
    if incluir_anamnese:
        df_anamnese = data_manager.get_data('anamnese_pei')
        anamnese = df_anamnese[df_anamnese['aluno_id'] == aluno_id]
        
        if len(anamnese) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("ANAMNESE PEDAGÓGICA (PEI)", heading_style))
            
            anamnese_data = anamnese.iloc[0].to_dict()
            
            dados_anamnese = [
                ['Data Preenchimento:', anamnese_data.get('data_preenchimento', '')],
                ['Turma/Série:', anamnese_data.get('turma_serie', '')],
                ['Desenvolvimento Motor:', anamnese_data.get('desenvolvimento_motor', '')],
                ['Coordenação Motora Fina:', anamnese_data.get('coordenacao_motora_fina', '')],
                ['Coordenação Motora Grossa:', anamnese_data.get('coordenacao_motora_grossa', '')],
                ['Lateralidade:', anamnese_data.get('lateralidade', '')],
                ['Atenção/Concentração:', anamnese_data.get('atencao_concentracao', '')],
                ['Memória:', anamnese_data.get('memoria', '')],
                ['Raciocínio Lógico:', anamnese_data.get('raciocinio_logico', '')],
                ['Linguagem Oral:', anamnese_data.get('linguagem_oral', '')],
                ['Articulação:', anamnese_data.get('articulacao', '')],
                ['Vocabulário:', anamnese_data.get('vocabulario', '')],
                ['Interação Social:', anamnese_data.get('interacao_social', '')],
                ['Regulação Emocional:', anamnese_data.get('regulacao_emocional', '')],
                ['Desempenho Português:', anamnese_data.get('desempenho_portugues', '')],
                ['Desempenho Matemática:', anamnese_data.get('desempenho_matematica', '')],
                ['Leitura:', anamnese_data.get('leitura', '')],
                ['Escrita:', anamnese_data.get('escrita', '')],
                ['Adaptações Metodológicas:', anamnese_data.get('adaptacoes_metodologicas', '')],
                ['Recursos Tecnológicos:', anamnese_data.get('recursos_tecnologicos', '')],
                ['Metas Curto Prazo:', anamnese_data.get('metas_curto_prazo', '')],
                ['Metas Médio Prazo:', anamnese_data.get('metas_medio_prazo', '')],
                ['Parecer Técnico:', anamnese_data.get('parecer_tecnico', '')],
                ['Profissional Responsável:', anamnese_data.get('profissional_responsavel', '')],
            ]
            
            table = Table(dados_anamnese, colWidths=[6*cm, 12.5*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e5f5')),
            ]))
            elements.append(table)
    
    # Questionário SAEB
    if incluir_saeb:
        df_saeb = data_manager.get_data('questionario_saeb')
        saeb = df_saeb[df_saeb['aluno_id'] == aluno_id]
        
        if len(saeb) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("QUESTIONÁRIO SAEB/SPAECE", heading_style))
            
            saeb_data = saeb.iloc[0].to_dict()
            
            dados_saeb = [
                ['Sexo:', saeb_data.get('sexo', '')],
                ['Idade:', saeb_data.get('idade', '')],
                ['Língua Família:', saeb_data.get('lingua_familia', '')],
                ['Cor/Raça:', saeb_data.get('cor_raca', '')],
                ['Deficiência:', saeb_data.get('deficiencia', '')],
                ['TEA:', saeb_data.get('tea', '')],
                ['Altas Habilidades:', saeb_data.get('altas_habilidades', '')],
                ['Mora com Mãe:', saeb_data.get('mora_mae', '')],
                ['Mora com Pai:', saeb_data.get('mora_pai', '')],
                ['Escolaridade Mãe:', saeb_data.get('escolaridade_mae', '')],
                ['Escolaridade Pai:', saeb_data.get('escolaridade_pai', '')],
                ['Responsável Lê:', saeb_data.get('responsavel_le', '')],
                ['Responsável Incentiva Estudar:', saeb_data.get('responsavel_incentiva_estudar', '')],
                ['Bairro com Asfalto:', saeb_data.get('bairro_asfalto', '')],
                ['Água Tratada:', saeb_data.get('bairro_agua_tratada', '')],
                ['Qtd Geladeira:', saeb_data.get('qtd_geladeira', '')],
                ['Qtd Computador:', saeb_data.get('qtd_computador', '')],
                ['Qtd Quartos:', saeb_data.get('qtd_quartos', '')],
                ['Casa com TV/Internet:', saeb_data.get('casa_tv_internet', '')],
                ['Casa com WiFi:', saeb_data.get('casa_wifi', '')],
                ['Tempo até Escola:', saeb_data.get('tempo_escola', '')],
                ['Transporte Gratuito:', saeb_data.get('transporte_gratuito', '')],
                ['Meio Transporte Principal:', saeb_data.get('meio_transporte_principal', '')],
                ['Idade Entrada Escola:', saeb_data.get('idade_entrada_escola', '')],
                ['Reprovação:', saeb_data.get('reprovacao', '')],
                ['Abandono:', saeb_data.get('abandono', '')],
                ['Prof. Explica:', saeb_data.get('prof_explica', '')],
                ['Prof. Debate:', saeb_data.get('prof_debate', '')],
                ['Escola Segurança:', saeb_data.get('escola_seguranca', '')],
                ['Expectativa Futura:', saeb_data.get('expectativa_futura', '')],
            ]
            
            table = Table(dados_saeb, colWidths=[6*cm, 12.5*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ]))
            elements.append(table)
    
    # Rodapé
    elements.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer.getvalue()
