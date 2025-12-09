"""
Módulo de Exportação em Lote (ZIP)
"""
import streamlit as st
import zipfile
import io
from datetime import datetime
from modulos.pdf_generator import gerar_pdf_aluno

def render_export_zip(data_manager):
    """Renderiza interface para exportação em lote"""
    st.header("📦 Exportação em Lote (ZIP)")
    st.markdown("---")
    
    df_cadastro = data_manager.get_data('cadastro')
    
    if len(df_cadastro) == 0:
        st.warning("⚠️ Não há alunos cadastrados.")
        return
    
    st.subheader("Configurações de Exportação")
    
    # Opções de filtro
    col1, col2 = st.columns(2)
    
    with col1:
        filtro_status = st.multiselect(
            "Filtrar por Status",
            options=df_cadastro['status'].unique(),
            default=list(df_cadastro['status'].unique())
        )
    
    with col2:
        filtro_ano = st.multiselect(
            "Filtrar por Ano Escolar",
            options=df_cadastro['ano_escolar'].unique(),
            default=list(df_cadastro['ano_escolar'].unique())
        )
    
    # Aplicar filtros
    df_filtrado = df_cadastro.copy()
    
    if filtro_status:
        df_filtrado = df_filtrado[df_filtrado['status'].isin(filtro_status)]
    
    if filtro_ano:
        df_filtrado = df_filtrado[df_filtrado['ano_escolar'].isin(filtro_ano)]
    
    st.info(f"📊 {len(df_filtrado)} aluno(s) selecionado(s) para exportação")
    
    # Opções de conteúdo
    st.subheader("Conteúdo dos PDFs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        incluir_cadastro = st.checkbox("Cadastro Geral", value=True, disabled=True)
    
    with col2:
        incluir_pei = st.checkbox("PEI", value=True, key="zip_pei")
    
    with col3:
        incluir_socio = st.checkbox("Socioeconômico", value=True, key="zip_socio")
    
    with col4:
        incluir_saude = st.checkbox("Saúde", value=True, key="zip_saude")
    
    # Opções de exportação adicional
    st.subheader("Arquivos Adicionais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exportar_csv = st.checkbox("Incluir dados CSV", value=True)
    
    with col2:
        exportar_relatorio = st.checkbox("Incluir relatório resumido", value=True)
    
    st.markdown("---")
    
    # Botão de exportação
    if st.button("📦 Gerar ZIP com PDFs", use_container_width=True):
        if len(df_filtrado) == 0:
            st.error("❌ Nenhum aluno selecionado para exportação")
            return
        
        with st.spinner(f"Gerando {len(df_filtrado)} PDFs..."):
            try:
                zip_buffer = gerar_zip_export(
                    data_manager,
                    df_filtrado,
                    incluir_pei,
                    incluir_socio,
                    incluir_saude,
                    exportar_csv,
                    exportar_relatorio
                )
                
                if zip_buffer:
                    st.success("✅ ZIP gerado com sucesso!")
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nome_arquivo = f"matriculas_2026_{timestamp}.zip"
                    
                    st.download_button(
                        label="📥 Baixar ZIP",
                        data=zip_buffer,
                        file_name=nome_arquivo,
                        mime="application/zip",
                        use_container_width=True
                    )
                else:
                    st.error("❌ Erro ao gerar ZIP")
            
            except Exception as e:
                st.error(f"❌ Erro ao gerar ZIP: {str(e)}")

def gerar_zip_export(data_manager, df_alunos, incluir_pei=True, incluir_socio=True, 
                     incluir_saude=True, exportar_csv=True, exportar_relatorio=True):
    """Gera arquivo ZIP com PDFs e dados"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Gerar PDFs individuais
        for idx, (_, aluno) in enumerate(df_alunos.iterrows(), 1):
            aluno_id = aluno['id']
            nome_aluno = aluno['nome_completo'].replace(' ', '_')
            
            try:
                pdf_data = gerar_pdf_aluno(
                    data_manager,
                    aluno_id,
                    incluir_pei,
                    incluir_socio,
                    incluir_saude
                )
                
                # Adicionar PDF ao ZIP
                pdf_filename = f"pdfs/ficha_{aluno_id}_{nome_aluno}.pdf"
                zip_file.writestr(pdf_filename, pdf_data)
            
            except Exception as e:
                # Log do erro mas continua processando
                error_msg = f"Erro ao gerar PDF do aluno {aluno_id}: {str(e)}\n"
                zip_file.writestr("erros.txt", error_msg)
        
        # Exportar CSVs
        if exportar_csv:
            # Cadastro geral
            csv_cadastro = df_alunos.to_csv(index=False).encode('utf-8')
            zip_file.writestr("dados_csv/cadastro_geral.csv", csv_cadastro)
            
            # PEI
            if incluir_pei:
                df_pei = data_manager.get_data('pei')
                alunos_ids = df_alunos['id'].tolist()
                df_pei_filtrado = df_pei[df_pei['aluno_id'].isin(alunos_ids)]
                if len(df_pei_filtrado) > 0:
                    csv_pei = df_pei_filtrado.to_csv(index=False).encode('utf-8')
                    zip_file.writestr("dados_csv/pei.csv", csv_pei)
            
            # Socioeconômico
            if incluir_socio:
                df_socio = data_manager.get_data('socioeconomico')
                alunos_ids = df_alunos['id'].tolist()
                df_socio_filtrado = df_socio[df_socio['aluno_id'].isin(alunos_ids)]
                if len(df_socio_filtrado) > 0:
                    csv_socio = df_socio_filtrado.to_csv(index=False).encode('utf-8')
                    zip_file.writestr("dados_csv/socioeconomico.csv", csv_socio)
            
            # Saúde
            if incluir_saude:
                df_saude = data_manager.get_data('saude')
                alunos_ids = df_alunos['id'].tolist()
                df_saude_filtrado = df_saude[df_saude['aluno_id'].isin(alunos_ids)]
                if len(df_saude_filtrado) > 0:
                    csv_saude = df_saude_filtrado.to_csv(index=False).encode('utf-8')
                    zip_file.writestr("dados_csv/saude.csv", csv_saude)
        
        # Gerar relatório resumido
        if exportar_relatorio:
            relatorio = gerar_relatorio_resumido(data_manager, df_alunos)
            zip_file.writestr("relatorio_resumido.txt", relatorio.encode('utf-8'))
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def gerar_relatorio_resumido(data_manager, df_alunos):
    """Gera relatório resumido em texto"""
    relatorio = []
    relatorio.append("=" * 80)
    relatorio.append("RELATÓRIO RESUMIDO - SISTEMA DE MATRÍCULA ESCOLAR 2026")
    relatorio.append("=" * 80)
    relatorio.append(f"\nData de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    relatorio.append(f"\nTotal de Alunos no Relatório: {len(df_alunos)}")
    relatorio.append("\n" + "-" * 80)
    
    # Estatísticas gerais
    relatorio.append("\n1. ESTATÍSTICAS GERAIS")
    relatorio.append("-" * 80)
    
    # Por status
    relatorio.append("\nPor Status:")
    status_counts = df_alunos['status'].value_counts()
    for status, count in status_counts.items():
        relatorio.append(f"  - {status}: {count} ({count/len(df_alunos)*100:.1f}%)")
    
    # Por ano escolar
    relatorio.append("\nPor Ano Escolar:")
    ano_counts = df_alunos['ano_escolar'].value_counts().sort_index()
    for ano, count in ano_counts.items():
        relatorio.append(f"  - {ano}: {count}")
    
    # Por turno
    relatorio.append("\nPor Turno:")
    turno_counts = df_alunos['turno'].value_counts()
    for turno, count in turno_counts.items():
        relatorio.append(f"  - {turno}: {count}")
    
    # Completude dos cadastros
    relatorio.append("\n" + "-" * 80)
    relatorio.append("2. COMPLETUDE DOS CADASTROS")
    relatorio.append("-" * 80)
    
    df_pei = data_manager.get_data('pei')
    df_socio = data_manager.get_data('socioeconomico')
    df_saude = data_manager.get_data('saude')
    
    com_pei = 0
    com_socio = 0
    com_saude = 0
    completos = 0
    
    for _, aluno in df_alunos.iterrows():
        aluno_id = aluno['id']
        
        tem_pei = len(df_pei[df_pei['aluno_id'] == aluno_id]) > 0
        tem_socio = len(df_socio[df_socio['aluno_id'] == aluno_id]) > 0
        tem_saude = len(df_saude[df_saude['aluno_id'] == aluno_id]) > 0
        
        if tem_pei:
            com_pei += 1
        if tem_socio:
            com_socio += 1
        if tem_saude:
            com_saude += 1
        if tem_pei and tem_socio and tem_saude:
            completos += 1
    
    relatorio.append(f"\nAlunos com PEI cadastrado: {com_pei} ({com_pei/len(df_alunos)*100:.1f}%)")
    relatorio.append(f"Alunos com dados socioeconômicos: {com_socio} ({com_socio/len(df_alunos)*100:.1f}%)")
    relatorio.append(f"Alunos com dados de saúde: {com_saude} ({com_saude/len(df_alunos)*100:.1f}%)")
    relatorio.append(f"Alunos com cadastro completo: {completos} ({completos/len(df_alunos)*100:.1f}%)")
    
    # Análise socioeconômica (se disponível)
    if len(df_socio) > 0:
        relatorio.append("\n" + "-" * 80)
        relatorio.append("3. ANÁLISE SOCIOECONÔMICA")
        relatorio.append("-" * 80)
        
        alunos_ids = df_alunos['id'].tolist()
        df_socio_filtrado = df_socio[df_socio['aluno_id'].isin(alunos_ids)]
        
        if len(df_socio_filtrado) > 0:
            # Renda
            relatorio.append("\nDistribuição de Renda Familiar:")
            renda_counts = df_socio_filtrado['renda_familiar'].value_counts()
            for renda, count in renda_counts.items():
                relatorio.append(f"  - {renda}: {count}")
            
            # Recursos tecnológicos
            com_internet = len(df_socio_filtrado[df_socio_filtrado['possui_internet'] == 'Sim'])
            com_computador = len(df_socio_filtrado[df_socio_filtrado['possui_computador'] == 'Sim'])
            com_smartphone = len(df_socio_filtrado[df_socio_filtrado['possui_smartphone'] == 'Sim'])
            
            relatorio.append("\nRecursos Tecnológicos:")
            relatorio.append(f"  - Com Internet: {com_internet} ({com_internet/len(df_socio_filtrado)*100:.1f}%)")
            relatorio.append(f"  - Com Computador: {com_computador} ({com_computador/len(df_socio_filtrado)*100:.1f}%)")
            relatorio.append(f"  - Com Smartphone: {com_smartphone} ({com_smartphone/len(df_socio_filtrado)*100:.1f}%)")
            
            # Benefícios sociais
            bolsa = len(df_socio_filtrado[df_socio_filtrado['bolsa_familia'] == 'Sim'])
            auxilio = len(df_socio_filtrado[df_socio_filtrado['auxilio_brasil'] == 'Sim'])
            
            relatorio.append("\nBenefícios Sociais:")
            relatorio.append(f"  - Bolsa Família: {bolsa}")
            relatorio.append(f"  - Auxílio Brasil: {auxilio}")
    
    # Análise de saúde (se disponível)
    if len(df_saude) > 0:
        relatorio.append("\n" + "-" * 80)
        relatorio.append("4. ANÁLISE DE SAÚDE")
        relatorio.append("-" * 80)
        
        alunos_ids = df_alunos['id'].tolist()
        df_saude_filtrado = df_saude[df_saude['aluno_id'].isin(alunos_ids)]
        
        if len(df_saude_filtrado) > 0:
            # Tipo sanguíneo
            relatorio.append("\nDistribuição de Tipo Sanguíneo:")
            tipo_counts = df_saude_filtrado['tipo_sanguineo'].value_counts()
            for tipo, count in tipo_counts.items():
                relatorio.append(f"  - {tipo}: {count}")
            
            # Vacinação
            vacinacao_ok = len(df_saude_filtrado[df_saude_filtrado['vacinacao_em_dia'] == 'Sim'])
            relatorio.append(f"\nVacinação em Dia: {vacinacao_ok} ({vacinacao_ok/len(df_saude_filtrado)*100:.1f}%)")
            
            # Plano de saúde
            com_plano = len(df_saude_filtrado[df_saude_filtrado['plano_saude'] == 'Sim'])
            relatorio.append(f"Com Plano de Saúde: {com_plano} ({com_plano/len(df_saude_filtrado)*100:.1f}%)")
    
    # Análise PEI (se disponível)
    if len(df_pei) > 0:
        relatorio.append("\n" + "-" * 80)
        relatorio.append("5. ANÁLISE PEI")
        relatorio.append("-" * 80)
        
        alunos_ids = df_alunos['id'].tolist()
        df_pei_filtrado = df_pei[df_pei['aluno_id'].isin(alunos_ids)]
        
        com_necessidade = len(df_pei_filtrado[df_pei_filtrado['necessidade_especial'] == 'Sim'])
        relatorio.append(f"\nAlunos com Necessidade Especial: {com_necessidade}")
        
        if com_necessidade > 0:
            relatorio.append("\nTipos de Deficiência:")
            pei_necessidades = df_pei_filtrado[df_pei_filtrado['necessidade_especial'] == 'Sim']
            # Contar tipos (pode haver múltiplos por aluno)
            tipos_dict = {}
            for tipos in pei_necessidades['tipo_deficiencia']:
                if tipos:
                    for tipo in tipos.split(', '):
                        tipos_dict[tipo] = tipos_dict.get(tipo, 0) + 1
            
            for tipo, count in tipos_dict.items():
                relatorio.append(f"  - {tipo}: {count}")
    
    relatorio.append("\n" + "=" * 80)
    relatorio.append("FIM DO RELATÓRIO")
    relatorio.append("=" * 80)
    
    return "\n".join(relatorio)
