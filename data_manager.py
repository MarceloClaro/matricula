"""
Módulo de gerenciamento de dados com persistência em CSV
"""
import pandas as pd
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.files = {
            'cadastro': os.path.join(data_dir, 'cadastro_geral.csv'),
            'pei': os.path.join(data_dir, 'pei.csv'),
            'socioeconomico': os.path.join(data_dir, 'socioeconomico.csv'),
            'saude': os.path.join(data_dir, 'saude.csv')
        }
        
        self._init_files()
    
    def _init_files(self):
        """Inicializa arquivos CSV se não existirem"""
        # Cadastro Geral
        if not os.path.exists(self.files['cadastro']):
            df = pd.DataFrame(columns=[
                'id', 'nome_completo', 'data_nascimento', 'cpf', 'rg', 
                'nome_mae', 'nome_pai', 'telefone', 'email',
                'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
                'escola_origem', 'ano_escolar', 'turno', 'data_matricula', 'status'
            ])
            df.to_csv(self.files['cadastro'], index=False)
        
        # PEI - Plano Educacional Individualizado
        if not os.path.exists(self.files['pei']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'necessidade_especial', 'tipo_deficiencia',
                'laudo_medico', 'data_laudo', 'cid', 'medicacao',
                'restricoes', 'apoio_necessario', 'adaptacao_curricular',
                'acompanhamento_especializado', 'recursos_necessarios',
                'observacoes', 'data_cadastro'
            ])
            df.to_csv(self.files['pei'], index=False)
        
        # Socioeconômico
        if not os.path.exists(self.files['socioeconomico']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'renda_familiar', 'qtd_pessoas_casa',
                'tipo_moradia', 'possui_internet', 'possui_computador',
                'possui_smartphone', 'bolsa_familia', 'auxilio_brasil',
                'beneficio_social', 'situacao_trabalho_responsavel',
                'profissao_responsavel', 'escolaridade_mae', 'escolaridade_pai',
                'transporte_escolar', 'tempo_deslocamento', 'data_cadastro'
            ])
            df.to_csv(self.files['socioeconomico'], index=False)
        
        # Saúde
        if not os.path.exists(self.files['saude']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'tipo_sanguineo', 'fator_rh',
                'alergias', 'doencas_cronicas', 'medicamentos_uso_continuo',
                'historico_doencas', 'vacinacao_em_dia', 'plano_saude',
                'nome_plano_saude', 'numero_plano', 'contato_emergencia',
                'telefone_emergencia', 'parentesco_emergencia',
                'observacoes_saude', 'data_cadastro'
            ])
            df.to_csv(self.files['saude'], index=False)
    
    def get_data(self, tipo):
        """Retorna dados do tipo especificado"""
        if tipo in self.files:
            try:
                df = pd.read_csv(self.files[tipo])
                return df
            except (FileNotFoundError, pd.errors.EmptyDataError):
                return pd.DataFrame()
        return pd.DataFrame()
    
    def save_data(self, tipo, df):
        """Salva dados do tipo especificado"""
        if tipo in self.files:
            df.to_csv(self.files[tipo], index=False)
            return True
        return False
    
    def add_record(self, tipo, dados):
        """Adiciona novo registro"""
        df = self.get_data(tipo)
        
        # Gera novo ID
        if len(df) == 0:
            novo_id = 1
        else:
            novo_id = df['id'].max() + 1
        
        dados['id'] = novo_id
        
        # Adiciona data de cadastro se não existir
        if 'data_cadastro' in df.columns and 'data_cadastro' not in dados:
            dados['data_cadastro'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Adiciona data de matrícula para cadastro geral
        if tipo == 'cadastro' and 'data_matricula' not in dados:
            dados['data_matricula'] = datetime.now().strftime('%Y-%m-%d')
        
        # Converte para DataFrame e concatena
        novo_df = pd.DataFrame([dados])
        df = pd.concat([df, novo_df], ignore_index=True)
        
        self.save_data(tipo, df)
        return novo_id
    
    def update_record(self, tipo, record_id, dados):
        """Atualiza registro existente"""
        df = self.get_data(tipo)
        
        if len(df) == 0:
            return False
        
        # Atualiza os dados
        idx = df[df['id'] == record_id].index
        if len(idx) > 0:
            for key, value in dados.items():
                if key in df.columns:
                    df.at[idx[0], key] = value
            
            self.save_data(tipo, df)
            return True
        
        return False
    
    def delete_record(self, tipo, record_id):
        """Deleta registro"""
        df = self.get_data(tipo)
        
        if len(df) == 0:
            return False
        
        df = df[df['id'] != record_id]
        self.save_data(tipo, df)
        return True
    
    def get_record(self, tipo, record_id):
        """Retorna registro específico"""
        df = self.get_data(tipo)
        
        if len(df) == 0:
            return None
        
        record = df[df['id'] == record_id]
        if len(record) > 0:
            return record.iloc[0].to_dict()
        
        return None
    
    def search_records(self, tipo, campo, valor):
        """Busca registros por campo"""
        df = self.get_data(tipo)
        
        if len(df) == 0 or campo not in df.columns:
            return pd.DataFrame()
        
        # Busca case-insensitive para strings
        if df[campo].dtype == 'object':
            mask = df[campo].astype(str).str.contains(str(valor), case=False, na=False)
            return df[mask]
        else:
            return df[df[campo] == valor]
    
    def get_all_student_data(self, aluno_id):
        """Retorna todos os dados de um aluno"""
        dados = {}
        
        # Cadastro geral
        cadastro = self.get_record('cadastro', aluno_id)
        if cadastro:
            dados['cadastro'] = cadastro
        
        # PEI
        pei_df = self.get_data('pei')
        if len(pei_df) > 0:
            pei = pei_df[pei_df['aluno_id'] == aluno_id]
            if len(pei) > 0:
                dados['pei'] = pei.iloc[0].to_dict()
        
        # Socioeconômico
        socio_df = self.get_data('socioeconomico')
        if len(socio_df) > 0:
            socio = socio_df[socio_df['aluno_id'] == aluno_id]
            if len(socio) > 0:
                dados['socioeconomico'] = socio.iloc[0].to_dict()
        
        # Saúde
        saude_df = self.get_data('saude')
        if len(saude_df) > 0:
            saude = saude_df[saude_df['aluno_id'] == aluno_id]
            if len(saude) > 0:
                dados['saude'] = saude.iloc[0].to_dict()
        
        return dados
