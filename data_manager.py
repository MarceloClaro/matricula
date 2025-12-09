"""
Módulo de gerenciamento de dados com persistência em CSV
"""
import pandas as pd
import os
import zipfile
import shutil
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
            'saude': os.path.join(data_dir, 'saude.csv'),
            'questionario_saeb': os.path.join(data_dir, 'questionario_saeb.csv'),
            'anamnese_pei': os.path.join(data_dir, 'anamnese_pei.csv')
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
        
        # Questionário SAEB/SPAECE
        if not os.path.exists(self.files['questionario_saeb']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'sexo', 'idade', 'lingua_familia', 'cor_raca',
                'deficiencia', 'tea', 'altas_habilidades',
                'mora_mae', 'mora_pai', 'mora_avo', 'mora_avoh', 'mora_outros',
                'escolaridade_mae', 'escolaridade_pai',
                'responsavel_le', 'responsavel_conversa', 'responsavel_incentiva_estudar',
                'responsavel_incentiva_tarefas', 'responsavel_incentiva_aulas', 
                'responsavel_participa_reunioes',
                'bairro_asfalto', 'bairro_agua_tratada', 'bairro_iluminacao',
                'qtd_geladeira', 'qtd_computador', 'qtd_quartos', 'qtd_televisao',
                'qtd_banheiro', 'qtd_carro', 'qtd_celular_internet',
                'casa_tv_internet', 'casa_wifi', 'casa_mesa_estudar', 'casa_microondas',
                'casa_aspirador', 'casa_maquina_lavar', 'casa_freezer', 'casa_garagem',
                'tempo_escola', 'transporte_gratuito', 'passe_escolar', 'meio_transporte_principal',
                'idade_entrada_escola', 'trajetoria_educacao', 'reprovacao', 'abandono',
                'tempo_estudar', 'tempo_extracurriculares', 'tempo_trabalho_domestico',
                'tempo_trabalho_remunerado', 'tempo_lazer',
                'prof_explica', 'prof_pergunta', 'prof_debate', 'prof_grupos',
                'prof_bullying', 'prof_racismo', 'prof_genero',
                'escola_interesse', 'escola_motivacao', 'escola_opinioes', 'escola_seguranca',
                'escola_vontade_prof', 'escola_dificuldade', 'escola_avaliacoes',
                'escola_prof_acreditam', 'escola_motivacao_continuar',
                'expectativa_futura', 'data_cadastro'
            ])
            df.to_csv(self.files['questionario_saeb'], index=False)
        
        # Anamnese Pedagógica PEI
        if not os.path.exists(self.files['anamnese_pei']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'data_preenchimento', 'filiacao', 'turma_serie',
                'desenvolvimento_motor', 'coordenacao_motora_fina', 'coordenacao_motora_grossa',
                'lateralidade', 'equilibrio', 'observacoes_neuro',
                'atencao_concentracao', 'memoria', 'raciocinio_logico', 'resolucao_problemas',
                'pensamento_abstrato', 'funcoes_executivas', 'observacoes_cognitivas',
                'linguagem_oral', 'articulacao', 'vocabulario', 'compreensao_verbal',
                'expressao_verbal', 'linguagem_escrita', 'observacoes_linguagem',
                'interacao_social', 'relacionamento_pares', 'relacionamento_professores',
                'regulacao_emocional', 'autoestima', 'ansiedade', 'impulsividade', 'agressividade',
                'bullying_vitima', 'bullying_agressor', 'comportamento_opositor', 'autolesao',
                'fuga_escola', 'isolamento_voluntario', 'observacoes_socioemocionais',
                'desempenho_portugues', 'desempenho_matematica', 'desempenho_ciencias',
                'desempenho_historia', 'desempenho_geografia', 'desempenho_ingles',
                'desempenho_ed_fisica', 'desempenho_artes',
                'leitura', 'escrita', 'compreensao_leitora', 'producao_textual', 'observacoes_academicas',
                'adaptacoes_metodologicas', 'adaptacoes_avaliativas', 'recursos_tecnologicos',
                'intervencoes_pedagogicas',
                'acompanhamento_psicologia', 'acompanhamento_psicopedagogia', 'acompanhamento_fonoaudiologia',
                'acompanhamento_terapia_ocupacional', 'acompanhamento_neurologia', 'acompanhamento_psiquiatria',
                'acompanhamento_assistente_social', 'outros_encaminhamentos',
                'participacao_familia', 'contexto_familiar', 'fatores_risco', 'fatores_protecao',
                'metas_curto_prazo', 'metas_medio_prazo', 'metas_longo_prazo', 'estrategias_implementacao',
                'observacoes_gerais', 'parecer_tecnico', 'profissional_responsavel',
                'formacao_profissional', 'registro_profissional', 'data_cadastro'
            ])
            df.to_csv(self.files['anamnese_pei'], index=False)
    
    def get_data(self, tipo):
        """Retorna dados do tipo especificado"""
        if tipo in self.files:
            try:
                # Read CSV and keep string columns as strings (avoid auto-conversion to float for NaN)
                df = pd.read_csv(self.files[tipo], dtype=str, keep_default_na=False)
                # Convert 'id' and numeric columns back to appropriate types
                if 'id' in df.columns and len(df) > 0:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                if 'aluno_id' in df.columns and len(df) > 0:
                    df['aluno_id'] = pd.to_numeric(df['aluno_id'], errors='coerce').fillna(0).astype(int)
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
        
        # Questionário SAEB
        saeb_df = self.get_data('questionario_saeb')
        if len(saeb_df) > 0:
            saeb = saeb_df[saeb_df['aluno_id'] == aluno_id]
            if len(saeb) > 0:
                dados['questionario_saeb'] = saeb.iloc[0].to_dict()
        
        # Anamnese Pedagógica PEI
        anamnese_df = self.get_data('anamnese_pei')
        if len(anamnese_df) > 0:
            anamnese = anamnese_df[anamnese_df['aluno_id'] == aluno_id]
            if len(anamnese) > 0:
                dados['anamnese_pei'] = anamnese.iloc[0].to_dict()
        
        return dados
    
    def create_backup(self, backup_path=None):
        """Cria backup de todos os arquivos CSV em formato ZIP"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'backup_matricula_{timestamp}.zip'
            backup_path = os.path.join(self.data_dir, '..', 'backups', backup_filename)
        
        # Cria diretório de backup se não existir
        backup_dir = os.path.dirname(backup_path)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Cria arquivo ZIP com todos os CSVs
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for tipo, filepath in self.files.items():
                if os.path.exists(filepath):
                    # Adiciona arquivo ao ZIP mantendo apenas o nome do arquivo
                    zipf.write(filepath, os.path.basename(filepath))
        
        return backup_path
    
    def restore_backup(self, backup_file):
        """Restaura backup de um arquivo ZIP"""
        try:
            # Cria diretório temporário para extração
            temp_dir = os.path.join(self.data_dir, '..', 'temp_restore')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extrai arquivos do ZIP
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Valida que todos os arquivos esperados estão presentes
            expected_files = [os.path.basename(f) for f in self.files.values()]
            extracted_files = os.listdir(temp_dir)
            
            missing_files = [f for f in expected_files if f not in extracted_files]
            if missing_files:
                shutil.rmtree(temp_dir)
                return False, f"Arquivos faltando no backup: {', '.join(missing_files)}"
            
            # Faz backup dos arquivos atuais antes de substituir
            backup_current_dir = os.path.join(self.data_dir, '..', 'backup_before_restore')
            if os.path.exists(backup_current_dir):
                shutil.rmtree(backup_current_dir)
            os.makedirs(backup_current_dir)
            
            for filepath in self.files.values():
                if os.path.exists(filepath):
                    shutil.copy2(filepath, backup_current_dir)
            
            # Copia arquivos restaurados para o diretório de dados
            for filename in expected_files:
                src = os.path.join(temp_dir, filename)
                dst = os.path.join(self.data_dir, filename)
                shutil.copy2(src, dst)
            
            # Remove diretório temporário
            shutil.rmtree(temp_dir)
            
            return True, "Backup restaurado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao restaurar backup: {str(e)}"
    
    def list_backups(self, backup_dir=None):
        """Lista todos os backups disponíveis"""
        if backup_dir is None:
            backup_dir = os.path.join(self.data_dir, '..', 'backups')
        
        if not os.path.exists(backup_dir):
            return []
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith('backup_matricula_') and filename.endswith('.zip'):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Ordena por data (mais recente primeiro)
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
