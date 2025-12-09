"""
Módulo de Busca Inteligente
"""
import streamlit as st
import pandas as pd

def render_busca(data_manager):
    """Renderiza interface de busca inteligente"""
    st.header("🔍 Busca Inteligente")
    st.markdown("---")
    
    # Tipo de busca
    tipo_busca = st.radio(
        "Tipo de Busca",
        ["Busca Rápida", "Busca Avançada"],
        horizontal=True
    )
    
    if tipo_busca == "Busca Rápida":
        render_busca_rapida(data_manager)
    else:
        render_busca_avancada(data_manager)

def render_busca_rapida(data_manager):
    """Busca rápida por nome ou ID"""
    st.subheader("Busca Rápida")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        termo_busca = st.text_input(
            "Digite o nome do aluno ou ID",
            placeholder="Ex: João Silva ou 123"
        )
    
    with col2:
        buscar = st.button("🔍 Buscar", use_container_width=True)
    
    if buscar and termo_busca:
        df_cadastro = data_manager.get_data('cadastro')
        
        if len(df_cadastro) == 0:
            st.info("Nenhum aluno cadastrado.")
            return
        
        # Buscar por ID ou nome
        resultados = pd.DataFrame()
        
        # Tentar buscar por ID
        if termo_busca.isdigit():
            resultados = df_cadastro[df_cadastro['id'] == int(termo_busca)]
        
        # Buscar por nome se não encontrou por ID
        if len(resultados) == 0:
            mask = df_cadastro['nome_completo'].str.contains(
                termo_busca, 
                case=False, 
                na=False
            )
            resultados = df_cadastro[mask]
        
        # Mostrar resultados
        if len(resultados) == 0:
            st.warning("Nenhum resultado encontrado.")
        else:
            st.success(f"✅ {len(resultados)} resultado(s) encontrado(s)")
            st.markdown("---")
            
            for _, aluno in resultados.iterrows():
                mostrar_detalhes_aluno(data_manager, aluno)

def render_busca_avancada(data_manager):
    """Busca avançada com múltiplos filtros"""
    st.subheader("Busca Avançada")
    
    df_cadastro = data_manager.get_data('cadastro')
    
    if len(df_cadastro) == 0:
        st.info("Nenhum aluno cadastrado.")
        return
    
    with st.form("form_busca_avancada"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome (parcial)")
            ano_escolar = st.multiselect(
                "Ano Escolar",
                options=df_cadastro['ano_escolar'].unique()
            )
            cidade = st.multiselect(
                "Cidade",
                options=df_cadastro['cidade'].unique()
            )
        
        with col2:
            status = st.multiselect(
                "Status",
                options=df_cadastro['status'].unique()
            )
            turno = st.multiselect(
                "Turno",
                options=df_cadastro['turno'].unique()
            )
            uf = st.multiselect(
                "UF",
                options=df_cadastro['uf'].unique()
            )
        
        # Filtros adicionais
        st.markdown("**Filtros Adicionais:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            com_pei = st.checkbox("Apenas com PEI")
        
        with col2:
            com_socio = st.checkbox("Com dados socioeconômicos")
        
        with col3:
            com_saude = st.checkbox("Com dados de saúde")
        
        submitted = st.form_submit_button("🔍 Buscar", use_container_width=True)
        
        if submitted:
            # Aplicar filtros
            resultados = df_cadastro.copy()
            
            if nome:
                mask = resultados['nome_completo'].str.contains(
                    nome, 
                    case=False, 
                    na=False
                )
                resultados = resultados[mask]
            
            if ano_escolar:
                resultados = resultados[resultados['ano_escolar'].isin(ano_escolar)]
            
            if cidade:
                resultados = resultados[resultados['cidade'].isin(cidade)]
            
            if status:
                resultados = resultados[resultados['status'].isin(status)]
            
            if turno:
                resultados = resultados[resultados['turno'].isin(turno)]
            
            if uf:
                resultados = resultados[resultados['uf'].isin(uf)]
            
            # Filtros de módulos complementares
            if com_pei or com_socio or com_saude:
                df_pei = data_manager.get_data('pei')
                df_socio = data_manager.get_data('socioeconomico')
                df_saude = data_manager.get_data('saude')
                
                ids_filtrados = []
                
                for _, aluno in resultados.iterrows():
                    aluno_id = aluno['id']
                    incluir = True
                    
                    if com_pei:
                        tem_pei = len(df_pei[df_pei['aluno_id'] == aluno_id]) > 0
                        if not tem_pei:
                            incluir = False
                    
                    if com_socio:
                        tem_socio = len(df_socio[df_socio['aluno_id'] == aluno_id]) > 0
                        if not tem_socio:
                            incluir = False
                    
                    if com_saude:
                        tem_saude = len(df_saude[df_saude['aluno_id'] == aluno_id]) > 0
                        if not tem_saude:
                            incluir = False
                    
                    if incluir:
                        ids_filtrados.append(aluno_id)
                
                resultados = resultados[resultados['id'].isin(ids_filtrados)]
            
            # Mostrar resultados
            if len(resultados) == 0:
                st.warning("Nenhum resultado encontrado com os filtros aplicados.")
            else:
                st.success(f"✅ {len(resultados)} resultado(s) encontrado(s)")
                st.markdown("---")
                
                # Opção de visualização
                modo_visualizacao = st.radio(
                    "Modo de Visualização",
                    ["Lista Resumida", "Detalhes Completos"],
                    horizontal=True
                )
                
                if modo_visualizacao == "Lista Resumida":
                    colunas = ['id', 'nome_completo', 'ano_escolar', 'turno', 
                              'telefone', 'cidade', 'status']
                    st.dataframe(resultados[colunas], use_container_width=True)
                    
                    # Exportar resultados
                    csv = resultados.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Exportar Resultados",
                        data=csv,
                        file_name=f"busca_resultados.csv",
                        mime="text/csv",
                    )
                else:
                    for _, aluno in resultados.iterrows():
                        mostrar_detalhes_aluno(data_manager, aluno)

def mostrar_detalhes_aluno(data_manager, aluno):
    """Mostra detalhes completos de um aluno"""
    with st.expander(f"👤 {aluno['nome_completo']} (ID: {aluno['id']})", expanded=False):
        # Dados principais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Dados Pessoais**")
            st.write(f"📅 Nascimento: {aluno['data_nascimento']}")
            st.write(f"📱 Telefone: {aluno['telefone']}")
            if aluno['email']:
                st.write(f"📧 Email: {aluno['email']}")
            st.write(f"👨‍👩‍👦 Mãe: {aluno['nome_mae']}")
            if aluno['nome_pai']:
                st.write(f"👨‍👩‍👦 Pai: {aluno['nome_pai']}")
        
        with col2:
            st.write("**Endereço**")
            st.write(f"{aluno['endereco']}, {aluno['numero']}")
            if aluno['complemento']:
                st.write(f"Complemento: {aluno['complemento']}")
            st.write(f"{aluno['bairro']}")
            st.write(f"{aluno['cidade']}/{aluno['uf']}")
            st.write(f"CEP: {aluno['cep']}")
        
        with col3:
            st.write("**Dados Escolares**")
            st.write(f"🎒 Ano: {aluno['ano_escolar']}")
            st.write(f"🕐 Turno: {aluno['turno']}")
            st.write(f"📊 Status: {aluno['status']}")
            if aluno['escola_origem']:
                st.write(f"🏫 Escola Origem: {aluno['escola_origem']}")
            st.write(f"📅 Matrícula: {aluno['data_matricula']}")
        
        # Verificar módulos complementares
        aluno_id = aluno['id']
        
        col1, col2, col3 = st.columns(3)
        
        # PEI
        df_pei = data_manager.get_data('pei')
        pei = df_pei[df_pei['aluno_id'] == aluno_id]
        
        with col1:
            if len(pei) > 0:
                pei_data = pei.iloc[0]
                st.success("✅ PEI Cadastrado")
                if pei_data['necessidade_especial'] == 'Sim':
                    st.write(f"🔹 {pei_data['tipo_deficiencia']}")
            else:
                st.warning("⚠️ PEI não cadastrado")
        
        # Socioeconômico
        df_socio = data_manager.get_data('socioeconomico')
        socio = df_socio[df_socio['aluno_id'] == aluno_id]
        
        with col2:
            if len(socio) > 0:
                socio_data = socio.iloc[0]
                st.success("✅ Socioeconômico Cadastrado")
                st.write(f"💰 {socio_data['renda_familiar']}")
            else:
                st.warning("⚠️ Socioeconômico não cadastrado")
        
        # Saúde
        df_saude = data_manager.get_data('saude')
        saude = df_saude[df_saude['aluno_id'] == aluno_id]
        
        with col3:
            if len(saude) > 0:
                saude_data = saude.iloc[0]
                st.success("✅ Saúde Cadastrada")
                st.write(f"🩸 {saude_data['tipo_sanguineo']} {saude_data['fator_rh']}")
            else:
                st.warning("⚠️ Saúde não cadastrada")
