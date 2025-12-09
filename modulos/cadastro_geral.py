"""
Módulo de Cadastro Geral de Alunos
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def render_cadastro_geral(data_manager):
    """Renderiza formulário de cadastro geral"""
    st.header("📝 Cadastro Geral do Aluno")
    st.markdown("---")
    
    with st.form("form_cadastro_geral"):
        st.subheader("Dados Pessoais")
        col1, col2 = st.columns(2)
        
        with col1:
            nome_completo = st.text_input("Nome Completo *", max_chars=100)
            data_nascimento = st.date_input("Data de Nascimento *", 
                                           min_value=datetime(2000, 1, 1),
                                           max_value=datetime.now())
            cpf = st.text_input("CPF", max_chars=14, placeholder="000.000.000-00")
        
        with col2:
            rg = st.text_input("RG", max_chars=20)
            nome_mae = st.text_input("Nome da Mãe *", max_chars=100)
            nome_pai = st.text_input("Nome do Pai", max_chars=100)
        
        st.subheader("Contato")
        col1, col2 = st.columns(2)
        
        with col1:
            telefone = st.text_input("Telefone *", max_chars=20, placeholder="(00) 00000-0000")
        
        with col2:
            email = st.text_input("E-mail", max_chars=100)
        
        st.subheader("Endereço")
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            endereco = st.text_input("Logradouro *", max_chars=200)
        
        with col2:
            numero = st.text_input("Número *", max_chars=10)
        
        with col3:
            complemento = st.text_input("Complemento", max_chars=50)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bairro = st.text_input("Bairro *", max_chars=100)
        
        with col2:
            cidade = st.text_input("Cidade *", max_chars=100)
        
        with col3:
            uf = st.selectbox("UF *", [
                "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ])
        
        with col4:
            cep = st.text_input("CEP *", max_chars=10, placeholder="00000-000")
        
        st.subheader("Dados Escolares")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            escola_origem = st.text_input("Escola de Origem", max_chars=100)
        
        with col2:
            ano_escolar = st.selectbox("Ano Escolar *", [
                "", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", 
                "6º Ano", "7º Ano", "8º Ano", "9º Ano"
            ])
        
        with col3:
            turno = st.selectbox("Turno *", ["", "Matutino", "Vespertino", "Integral"])
        
        status = st.selectbox("Status *", ["", "Ativo", "Aguardando Documentação", "Cancelado"])
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Cadastro", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not nome_completo:
                erros.append("Nome completo é obrigatório")
            if not nome_mae:
                erros.append("Nome da mãe é obrigatório")
            if not telefone:
                erros.append("Telefone é obrigatório")
            if not endereco:
                erros.append("Endereço é obrigatório")
            if not numero:
                erros.append("Número é obrigatório")
            if not bairro:
                erros.append("Bairro é obrigatório")
            if not cidade:
                erros.append("Cidade é obrigatória")
            if not uf:
                erros.append("UF é obrigatório")
            if not cep:
                erros.append("CEP é obrigatório")
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
                # Salvar dados
                dados = {
                    'nome_completo': nome_completo,
                    'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                    'cpf': cpf,
                    'rg': rg,
                    'nome_mae': nome_mae,
                    'nome_pai': nome_pai,
                    'telefone': telefone,
                    'email': email,
                    'endereco': endereco,
                    'numero': numero,
                    'complemento': complemento,
                    'bairro': bairro,
                    'cidade': cidade,
                    'uf': uf,
                    'cep': cep,
                    'escola_origem': escola_origem,
                    'ano_escolar': ano_escolar,
                    'turno': turno,
                    'status': status
                }
                
                try:
                    novo_id = data_manager.add_record('cadastro', dados)
                    st.success(f"✅ Cadastro realizado com sucesso! ID do aluno: {novo_id}")
                    st.balloons()
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
        lambda row: f"{row['nome_mae']}" + (f" / {row['nome_pai']}" if row['nome_pai'] and str(row['nome_pai']).strip() != '' else ""),
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
    if len(df_pei) > 0:
        # Criar dicionário de alunos com PEI
        alunos_com_pei = {}
        for _, pei_row in df_pei.iterrows():
            if pei_row['necessidade_especial'] == 'Sim':
                alunos_com_pei[int(pei_row['aluno_id'])] = 'Sim'
        
        df_filtrado['aluno_especial_pei'] = df_filtrado['id'].apply(
            lambda id_aluno: alunos_com_pei.get(int(id_aluno), 'Não')
        )
    else:
        df_filtrado['aluno_especial_pei'] = 'Não'
    
    # Mostrar dados
    st.markdown(f"**Total de alunos:** {len(df_filtrado)}")
    
    # Selecionar colunas para exibição
    colunas_exibir = ['id', 'nome_completo', 'responsaveis', 'endereco_completo', 
                      'ano_escolar', 'turno', 'telefone', 'aluno_especial_pei', 'status']
    
    st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)
