"""
Módulo Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard(data_manager):
    """Renderiza dashboard com estatísticas"""
    st.header("📊 Dashboard - Matrícula Escolar 2026")
    st.markdown("---")
    
    # Carregar dados
    df_cadastro = data_manager.get_data('cadastro')
    df_pei = data_manager.get_data('pei')
    df_socio = data_manager.get_data('socioeconomico')
    df_saude = data_manager.get_data('saude')
    df_saeb = data_manager.get_data('questionario_saeb')
    
    # Verificar se há dados
    if len(df_cadastro) == 0:
        st.info("📝 Ainda não há alunos cadastrados. Comece cadastrando os alunos!")
        return
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Alunos",
            value=len(df_cadastro),
            delta=None
        )
    
    with col2:
        ativos = len(df_cadastro[df_cadastro['status'] == 'Ativo'])
        st.metric(
            label="Alunos Ativos",
            value=ativos,
            delta=f"{(ativos/len(df_cadastro)*100):.1f}%"
        )
    
    with col3:
        com_pei = len(df_pei[df_pei['necessidade_especial'] == 'Sim'])
        st.metric(
            label="Com PEI",
            value=com_pei,
            delta=None
        )
    
    with col4:
        completos = len(df_cadastro)
        for _, row in df_cadastro.iterrows():
            aluno_id = row['id']
            tem_pei = len(df_pei[df_pei['aluno_id'] == aluno_id]) > 0
            tem_socio = len(df_socio[df_socio['aluno_id'] == aluno_id]) > 0
            tem_saude = len(df_saude[df_saude['aluno_id'] == aluno_id]) > 0
            tem_saeb = len(df_saeb[df_saeb['aluno_id'] == aluno_id]) > 0
            if not (tem_pei and tem_socio and tem_saude and tem_saeb):
                completos -= 1
        
        st.metric(
            label="Cadastros Completos",
            value=completos,
            delta=f"{(completos/len(df_cadastro)*100):.1f}%"
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Alunos por Ano Escolar")
        if 'ano_escolar' in df_cadastro.columns:
            ano_counts = df_cadastro['ano_escolar'].value_counts().reset_index()
            ano_counts.columns = ['Ano Escolar', 'Quantidade']
            
            fig = px.bar(
                ano_counts,
                x='Ano Escolar',
                y='Quantidade',
                color='Quantidade',
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🕐 Alunos por Turno")
        if 'turno' in df_cadastro.columns:
            turno_counts = df_cadastro['turno'].value_counts().reset_index()
            turno_counts.columns = ['Turno', 'Quantidade']
            
            fig = px.pie(
                turno_counts,
                values='Quantidade',
                names='Turno',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status das Matrículas")
        if 'status' in df_cadastro.columns:
            status_counts = df_cadastro['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Quantidade']
            
            fig = px.pie(
                status_counts,
                values='Quantidade',
                names='Status',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏙️ Alunos por Cidade")
        if 'cidade' in df_cadastro.columns:
            cidade_counts = df_cadastro['cidade'].value_counts().head(10).reset_index()
            cidade_counts.columns = ['Cidade', 'Quantidade']
            
            fig = px.bar(
                cidade_counts,
                x='Quantidade',
                y='Cidade',
                orientation='h',
                color='Quantidade',
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Análise Socioeconômica
    if len(df_socio) > 0:
        st.markdown("---")
        st.subheader("💰 Análise Socioeconômica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Renda Familiar**")
            if 'renda_familiar' in df_socio.columns:
                renda_counts = df_socio['renda_familiar'].value_counts().reset_index()
                renda_counts.columns = ['Renda Familiar', 'Quantidade']
                
                fig = px.bar(
                    renda_counts,
                    x='Renda Familiar',
                    y='Quantidade',
                    color='Quantidade',
                    color_continuous_scale='Oranges'
                )
                fig.update_layout(showlegend=False, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Recursos Tecnológicos**")
            recursos = {
                'Internet': len(df_socio[df_socio['possui_internet'] == 'Sim']),
                'Computador': len(df_socio[df_socio['possui_computador'] == 'Sim']),
                'Smartphone': len(df_socio[df_socio['possui_smartphone'] == 'Sim'])
            }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(recursos.keys()),
                    y=list(recursos.values()),
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
                )
            ])
            fig.update_layout(
                yaxis_title="Quantidade de Alunos",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Benefícios Sociais**")
            beneficios = {
                'Bolsa Família': len(df_socio[df_socio['bolsa_familia'] == 'Sim']),
                'Auxílio Brasil': len(df_socio[df_socio['auxilio_brasil'] == 'Sim']),
                'Outros': len(df_socio[df_socio['beneficio_social'] == 'Sim'])
            }
            
            fig = px.pie(
                values=list(beneficios.values()),
                names=list(beneficios.keys()),
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Transporte Escolar**")
            if 'transporte_escolar' in df_socio.columns:
                transp_counts = df_socio['transporte_escolar'].value_counts().reset_index()
                transp_counts.columns = ['Transporte', 'Quantidade']
                
                fig = px.pie(
                    transp_counts,
                    values='Quantidade',
                    names='Transporte',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Análise de Saúde
    if len(df_saude) > 0:
        st.markdown("---")
        st.subheader("🏥 Análise de Saúde")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tipo Sanguíneo**")
            if 'tipo_sanguineo' in df_saude.columns:
                tipo_counts = df_saude['tipo_sanguineo'].value_counts().reset_index()
                tipo_counts.columns = ['Tipo Sanguíneo', 'Quantidade']
                
                fig = px.bar(
                    tipo_counts,
                    x='Tipo Sanguíneo',
                    y='Quantidade',
                    color='Tipo Sanguíneo',
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Vacinação e Plano de Saúde**")
            vacinacao_sim = len(df_saude[df_saude['vacinacao_em_dia'] == 'Sim'])
            plano_sim = len(df_saude[df_saude['plano_saude'] == 'Sim'])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['Vacinação em Dia', 'Possui Plano de Saúde'],
                    y=[vacinacao_sim, plano_sim],
                    marker_color=['#17becf', '#bcbd22']
                )
            ])
            fig.update_layout(
                yaxis_title="Quantidade de Alunos",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de alunos com cadastro incompleto
    st.markdown("---")
    st.subheader("⚠️ Alunos com Cadastro Incompleto")
    
    incompletos = []
    for _, row in df_cadastro.iterrows():
        aluno_id = row['id']
        faltando = []
        
        if len(df_pei[df_pei['aluno_id'] == aluno_id]) == 0:
            faltando.append("PEI")
        if len(df_socio[df_socio['aluno_id'] == aluno_id]) == 0:
            faltando.append("Socioeconômico")
        if len(df_saeb[df_saeb['aluno_id'] == aluno_id]) == 0:
            faltando.append("Quest. SAEB")
        if len(df_saude[df_saude['aluno_id'] == aluno_id]) == 0:
            faltando.append("Saúde")
        
        if faltando:
            incompletos.append({
                'ID': aluno_id,
                'Nome': row['nome_completo'],
                'Ano Escolar': row['ano_escolar'],
                'Faltando': ', '.join(faltando)
            })
    
    if incompletos:
        df_incompletos = pd.DataFrame(incompletos)
        st.dataframe(df_incompletos, use_container_width=True)
    else:
        st.success("✅ Todos os alunos possuem cadastro completo!")
