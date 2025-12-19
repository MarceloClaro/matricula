"""
Módulo de gerenciamento de dados com persistência em CSV
Inclui: Cache, Validação, Indexação e Transações
"""
import pandas as pd
import os
import zipfile
import shutil
import tempfile
from datetime import datetime
from functools import lru_cache
import threading

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        # Use absolute paths to avoid issues with relative paths
        base_dir = os.path.dirname(os.path.abspath(data_dir))
        self.backup_dir = os.path.join(base_dir, 'backups')
        self.backup_before_restore_dir = os.path.join(base_dir, 'backup_before_restore')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.files = {
            'cadastro': os.path.join(data_dir, 'cadastro_geral.csv'),
            'pei': os.path.join(data_dir, 'pei.csv'),
            'socioeconomico': os.path.join(data_dir, 'socioeconomico.csv'),
            'saude': os.path.join(data_dir, 'saude.csv'),
            'questionario_saeb': os.path.join(data_dir, 'questionario_saeb.csv'),
            'anamnese_pei': os.path.join(data_dir, 'anamnese_pei.csv'),
            'face_embeddings': os.path.join(data_dir, 'face_embeddings.csv'),
            'attendance': os.path.join(data_dir, 'attendance.csv')
        }
        
        # Cache de dados em memória para acesso rápido
        self._cache = {}
        self._cache_timestamp = {}
        self._cache_ttl = 60  # TTL em segundos (1 minuto)
        
        # Índices para busca rápida
        self._indexes = {}
        
        # Lock para operações thread-safe
        self._lock = threading.Lock()
        
        # Campos obrigatórios por tipo
        self._required_fields = {
            'cadastro': ['nome_completo', 'data_nascimento', 'status'],
            'pei': ['aluno_id', 'necessidade_especial'],
            'socioeconomico': ['aluno_id'],
            'saude': ['aluno_id'],
            'questionario_saeb': ['aluno_id'],
            'anamnese_pei': ['aluno_id'],
            'face_embeddings': ['aluno_id'],
            'attendance': ['aluno_id', 'data']
        }
        
        self._init_files()
    
    def _validate_data(self, tipo, dados):
        """
        Valida dados antes de salvar
        
        Args:
            tipo: Tipo de dado (cadastro, pei, etc.)
            dados: Dicionário com os dados
            
        Returns:
            tuple: (valido: bool, mensagem_erro: str ou None)
        """
        # Verifica campos obrigatórios
        if tipo in self._required_fields:
            for field in self._required_fields[tipo]:
                if field not in dados or dados[field] is None or str(dados[field]).strip() == '':
                    return False, f"Campo obrigatório ausente ou vazio: {field}"
        
        # Validações específicas por tipo
        if tipo == 'cadastro':
            # Valida CPF (formato básico)
            if 'cpf' in dados and dados['cpf']:
                cpf = str(dados['cpf']).replace('.', '').replace('-', '').strip()
                if cpf and (len(cpf) != 11 or not cpf.isdigit()):
                    return False, "CPF inválido: deve conter 11 dígitos"
            
            # Valida data de nascimento
            if 'data_nascimento' in dados and dados['data_nascimento']:
                try:
                    data = pd.to_datetime(dados['data_nascimento'])
                    if data > pd.Timestamp.now():
                        return False, "Data de nascimento não pode ser futura"
                except:
                    return False, "Data de nascimento inválida"
        
        return True, None
    
    def _invalidate_cache(self, tipo):
        """Invalida cache para um tipo específico"""
        if tipo in self._cache:
            del self._cache[tipo]
        if tipo in self._cache_timestamp:
            del self._cache_timestamp[tipo]
        if tipo in self._indexes:
            del self._indexes[tipo]
    
    def _is_cache_valid(self, tipo):
        """Verifica se cache é válido"""
        if tipo not in self._cache or tipo not in self._cache_timestamp:
            return False
        
        elapsed = (datetime.now() - self._cache_timestamp[tipo]).total_seconds()
        return elapsed < self._cache_ttl
    
    def _build_indexes(self, tipo, df):
        """Cria índices para busca rápida"""
        if len(df) == 0:
            return
        
        self._indexes[tipo] = {}
        
        # Índice por ID
        if 'id' in df.columns:
            self._indexes[tipo]['id'] = df.set_index('id').to_dict('index')
        
        # Índices específicos por tipo
        if tipo == 'cadastro':
            # Índice por CPF
            if 'cpf' in df.columns:
                cpf_index = {}
                for idx, row in df.iterrows():
                    if pd.notna(row.get('cpf')):
                        cpf = str(row['cpf']).replace('.', '').replace('-', '').strip()
                        if cpf:
                            cpf_index[cpf] = row.to_dict()
                self._indexes[tipo]['cpf'] = cpf_index
            
            # Índice por nome (primeira palavra para busca rápida)
            if 'nome_completo' in df.columns:
                name_index = {}
                for idx, row in df.iterrows():
                    if pd.notna(row.get('nome_completo')):
                        first_name = str(row['nome_completo']).split()[0].upper()
                        if first_name not in name_index:
                            name_index[first_name] = []
                        name_index[first_name].append(row.to_dict())
                self._indexes[tipo]['nome'] = name_index
    
    def _init_files(self):
        """Inicializa arquivos CSV se não existirem"""
        # Cadastro Geral
        if not os.path.exists(self.files['cadastro']):
            df = pd.DataFrame(columns=[
                # Identificação básica
                'id', 'nome_completo', 'nome_social', 'data_nascimento', 'cpf', 'codigo_inep', 
                'matricula', 'sexo', 'cor_raca', 'telefone', 'email', 'nis',
                # Nacionalidade
                'nacionalidade', 'uf_nascimento', 'cidade_nascimento', 'pais_nacionalidade',
                # Filiação
                'nome_mae', 'cpf_mae', 'profissao_mae', 
                'nome_pai', 'cpf_pai', 'profissao_pai',
                # Documentação civil
                'rg', 'numero_documento', 'orgao_emissor', 'uf_emissor', 'data_expedicao',
                'modelo_certidao', 'tipo_certidao', 'cartao_sus', 'documento_estrangeiro',
                'justificativa_documentacao',
                # Endereço
                'cep', 'bairro', 'endereco', 'numero', 'complemento', 'zona', 'uf', 'cidade',
                # Saúde
                'cartao_nacional_sus', 'alergia', 'aluno_deficiencia', 'possui_laudo_medico',
                'tipo_deficiencia', 'atendimentos_especializados', 'recursos_saeb',
                'escolarizacao_outro_espaco',
                # Informações médicas detalhadas (CID-10, DSM-5, medicação)
                'cid_10_dsm5', 'medicacao_uso', 'nome_medicacao', 'dosagem_medicacao',
                'horario_medicacao', 'medico_responsavel', 'crm_medico',
                'efeitos_esperados', 'efeitos_colaterais',
                # Histórico escolar
                'escola_origem', 'escola_ano_anterior', 'programas_educacionais',
                'rendimento_ano_anterior', 'movimento_escolar',
                # Dados escolares atuais
                'ano_escolar', 'turno', 'status',
                # Transporte
                'utiliza_transporte', 'poder_responsavel_transporte', 'tipo_veiculo',
                # Metadados
                'data_matricula', 'foto_path'
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
        
        # Face Embeddings (for face recognition)
        if not os.path.exists(self.files['face_embeddings']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'embedding', 'photo_path', 'data_cadastro'
            ])
            df.to_csv(self.files['face_embeddings'], index=False)
        
        # Attendance Records
        if not os.path.exists(self.files['attendance']):
            df = pd.DataFrame(columns=[
                'id', 'aluno_id', 'data', 'hora', 'tipo', 'verificado', 
                'confianca', 'observacoes', 'data_registro'
            ])
            df.to_csv(self.files['attendance'], index=False)
    
    def _get_data_internal(self, tipo):
        """Internal version without lock"""
        # Verifica cache
        if self._is_cache_valid(tipo):
            return self._cache[tipo].copy()
        
        # Carrega do arquivo
        if tipo in self.files:
            try:
                df = pd.read_csv(self.files[tipo], dtype=str, keep_default_na=False)
                if 'id' in df.columns and len(df) > 0:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                if 'aluno_id' in df.columns and len(df) > 0:
                    df['aluno_id'] = pd.to_numeric(df['aluno_id'], errors='coerce').fillna(0).astype(int)
                
                # Atualiza cache
                self._cache[tipo] = df.copy()
                self._cache_timestamp[tipo] = datetime.now()
                
                # Constrói índices
                self._build_indexes(tipo, df)
                
                return df.copy()
            except (FileNotFoundError, pd.errors.EmptyDataError):
                return pd.DataFrame()
        return pd.DataFrame()
    
    def get_data(self, tipo):
        """
        Retorna dados do tipo especificado com cache
        
        Args:
            tipo: Tipo de dado
            
        Returns:
            DataFrame com os dados
        """
        with self._lock:
            return self._get_data_internal(tipo)
    
    def _save_data_internal(self, tipo, df):
        """Internal version without lock"""
        if tipo in self.files:
            df.to_csv(self.files[tipo], index=False)
            # Invalida cache
            self._invalidate_cache(tipo)
            return True
        return False
    
    def save_data(self, tipo, df):
        """
        Salva dados do tipo especificado e invalida cache
        
        Args:
            tipo: Tipo de dado
            df: DataFrame com os dados
            
        Returns:
            bool: True se salvou com sucesso
        """
        with self._lock:
            return self._save_data_internal(tipo, df)
    
    def add_record(self, tipo, dados):
        """
        Adiciona novo registro com validação
        
        Args:
            tipo: Tipo de dado
            dados: Dicionário com os dados
            
        Returns:
            int: ID do novo registro ou None se falhou
            
        Raises:
            ValueError: Se validação falhar
        """
        # Valida dados
        valido, erro = self._validate_data(tipo, dados)
        if not valido:
            raise ValueError(f"Validação falhou: {erro}")
        
        with self._lock:
            df = self._get_data_internal(tipo)
            
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
            
            self._save_data_internal(tipo, df)
            return novo_id
    
    def update_record(self, tipo, record_id, dados):
        """
        Atualiza registro existente com validação
        
        Args:
            tipo: Tipo de dado
            record_id: ID do registro
            dados: Dicionário com os dados a atualizar
            
        Returns:
            bool: True se atualizou com sucesso
            
        Raises:
            ValueError: Se validação falhar
        """
        # Valida apenas os campos fornecidos
        for field in dados:
            if field in self._required_fields.get(tipo, []):
                if dados[field] is None or str(dados[field]).strip() == '':
                    raise ValueError(f"Campo obrigatório não pode ser vazio: {field}")
        
        with self._lock:
            df = self._get_data_internal(tipo)
            
            if len(df) == 0:
                return False
            
            # Atualiza os dados
            idx = df[df['id'] == record_id].index
            if len(idx) > 0:
                for key, value in dados.items():
                    if key in df.columns:
                        df.at[idx[0], key] = value
                
                self._save_data_internal(tipo, df)
                return True
            
            return False
    
    def delete_record(self, tipo, record_id):
        """
        Deleta registro com suporte a transação
        
        Args:
            tipo: Tipo de dado
            record_id: ID do registro
            
        Returns:
            bool: True se deletou com sucesso
        """
        with self._lock:
            df = self._get_data_internal(tipo)
            
            if len(df) == 0:
                return False
            
            df = df[df['id'] != record_id]
            self._save_data_internal(tipo, df)
            return True
    
    def execute_transaction(self, operations):
        """
        Executa múltiplas operações de forma atômica
        
        Args:
            operations: Lista de tuplas (operacao, tipo, *args)
                       operacao pode ser: 'add', 'update', 'delete'
                       
        Returns:
            tuple: (success: bool, results: list, error: str or None)
            
        Example:
            operations = [
                ('add', 'cadastro', {'nome_completo': 'João', 'status': 'Ativo'}),
                ('add', 'pei', {'aluno_id': 1, 'necessidade_especial': 'Sim'})
            ]
        """
        results = []
        backups = {}
        
        try:
            with self._lock:
                # Faz backup de todos os tipos afetados
                tipos_afetados = set(op[1] for op in operations)
                for tipo in tipos_afetados:
                    backups[tipo] = self._get_data_internal(tipo).copy()
                
                # Executa operações SEM nested locks
                for operation in operations:
                    op_type = operation[0]
                    tipo = operation[1]
                    
                    if op_type == 'add':
                        dados = operation[2]
                        # Valida
                        valido, erro = self._validate_data(tipo, dados)
                        if not valido:
                            raise ValueError(f"Validação falhou: {erro}")
                        
                        # Adiciona
                        df = self._get_data_internal(tipo)
                        novo_id = 1 if len(df) == 0 else df['id'].max() + 1
                        dados['id'] = novo_id
                        if 'data_cadastro' in df.columns and 'data_cadastro' not in dados:
                            dados['data_cadastro'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        novo_df = pd.DataFrame([dados])
                        df = pd.concat([df, novo_df], ignore_index=True)
                        self._save_data_internal(tipo, df)
                        results.append(('add', tipo, novo_id))
                    
                    elif op_type == 'update':
                        record_id = operation[2]
                        dados = operation[3]
                        # Atualiza
                        df = self._get_data_internal(tipo)
                        idx = df[df['id'] == record_id].index
                        if len(idx) > 0:
                            for key, value in dados.items():
                                if key in df.columns:
                                    df.at[idx[0], key] = value
                            self._save_data_internal(tipo, df)
                            results.append(('update', tipo, True))
                        else:
                            results.append(('update', tipo, False))
                    
                    elif op_type == 'delete':
                        record_id = operation[2]
                        df = self._get_data_internal(tipo)
                        df = df[df['id'] != record_id]
                        self._save_data_internal(tipo, df)
                        results.append(('delete', tipo, True))
                    
                    else:
                        raise ValueError(f"Operação inválida: {op_type}")
                
                return True, results, None
                
        except Exception as e:
            # Rollback: restaura backups
            for tipo, backup_df in backups.items():
                self._save_data_internal(tipo, backup_df)
            
            return False, results, str(e)
    
    def clear_cache(self):
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._cache_timestamp.clear()
            self._indexes.clear()
    
    def get_cache_stats(self):
        """Retorna estatísticas do cache"""
        stats = {
            'cached_types': list(self._cache.keys()),
            'cache_sizes': {k: len(v) for k, v in self._cache.items()},
            'indexes': {k: list(v.keys()) for k, v in self._indexes.items()}
        }
        return stats
    
    def get_record(self, tipo, record_id):
        """
        Retorna registro específico usando índice quando possível
        
        Args:
            tipo: Tipo de dado
            record_id: ID do registro
            
        Returns:
            dict: Dados do registro ou None
        """
        # Tenta usar índice primeiro (mais rápido)
        if tipo in self._indexes and 'id' in self._indexes[tipo]:
            return self._indexes[tipo]['id'].get(record_id)
        
        # Fallback para busca no DataFrame
        df = self.get_data(tipo)
        
        if len(df) == 0:
            return None
        
        record = df[df['id'] == record_id]
        if len(record) > 0:
            return record.iloc[0].to_dict()
        
        return None
    
    def get_record_by_cpf(self, cpf):
        """
        Busca rápida por CPF usando índice
        
        Args:
            cpf: CPF do aluno
            
        Returns:
            dict: Dados do registro ou None
        """
        cpf_clean = str(cpf).replace('.', '').replace('-', '').strip()
        
        if 'cadastro' in self._indexes and 'cpf' in self._indexes['cadastro']:
            return self._indexes['cadastro']['cpf'].get(cpf_clean)
        
        # Fallback para busca tradicional
        return self.search_records('cadastro', 'cpf', cpf).to_dict('records')[0] if len(self.search_records('cadastro', 'cpf', cpf)) > 0 else None
    
    def search_by_name(self, nome):
        """
        Busca otimizada por nome usando índice
        
        Args:
            nome: Nome ou parte do nome
            
        Returns:
            list: Lista de registros encontrados
        """
        if not nome:
            return []
        
        first_word = str(nome).split()[0].upper()
        
        if 'cadastro' in self._indexes and 'nome' in self._indexes['cadastro']:
            # Busca usando índice
            results = []
            for key, records in self._indexes['cadastro']['nome'].items():
                if first_word in key or key in first_word:
                    results.extend(records)
            return results
        
        # Fallback para busca tradicional
        df = self.search_records('cadastro', 'nome_completo', nome)
        return df.to_dict('records') if len(df) > 0 else []
    
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
        """
        Cria backup de todos os arquivos CSV em formato ZIP
        
        Args:
            backup_path (str, optional): Caminho completo para o arquivo de backup.
                                        Se None, cria automaticamente com timestamp.
        
        Returns:
            str: Caminho completo do arquivo de backup criado
        """
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'backup_matricula_{timestamp}.zip'
            backup_path = os.path.join(self.backup_dir, backup_filename)
        
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
        """
        Restaura backup de um arquivo ZIP
        
        Args:
            backup_file (str): Caminho para o arquivo ZIP de backup
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
                   - sucesso: True se restaurado com sucesso, False caso contrário
                   - mensagem: Mensagem descritiva do resultado
        """
        try:
            # Cria diretório temporário para extração de forma segura
            temp_dir = tempfile.mkdtemp(prefix='matricula_restore_')
            
            try:
                # Extrai arquivos do ZIP
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Valida que todos os arquivos esperados estão presentes
                expected_files = [os.path.basename(f) for f in self.files.values()]
                extracted_files = os.listdir(temp_dir)
                
                missing_files = [f for f in expected_files if f not in extracted_files]
                if missing_files:
                    return False, f"Arquivos faltando no backup: {', '.join(missing_files)}"
                
                # Valida que os arquivos extraídos são CSVs válidos
                for filename in expected_files:
                    filepath = os.path.join(temp_dir, filename)
                    if not os.path.exists(filepath):
                        return False, f"Arquivo não encontrado: {filename}"
                    try:
                        # Tenta ler o arquivo como CSV para validar integridade
                        pd.read_csv(filepath, nrows=0)
                    except Exception as e:
                        return False, f"Arquivo CSV inválido ({filename}): {str(e)}"
                
                # Faz backup dos arquivos atuais antes de substituir
                # Usa método mais seguro para recriar diretório
                shutil.rmtree(self.backup_before_restore_dir, ignore_errors=True)
                os.makedirs(self.backup_before_restore_dir, exist_ok=True)
                
                for filepath in self.files.values():
                    if os.path.exists(filepath):
                        shutil.copy2(filepath, self.backup_before_restore_dir)
                
                # Copia arquivos restaurados para o diretório de dados
                for filename in expected_files:
                    src = os.path.join(temp_dir, filename)
                    dst = os.path.join(self.data_dir, filename)
                    shutil.copy2(src, dst)
                
                return True, "Backup restaurado com sucesso!"
                
            finally:
                # Remove diretório temporário
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            
        except Exception as e:
            return False, f"Erro ao restaurar backup: {str(e)}"
    
    def list_backups(self, backup_dir=None):
        """
        Lista todos os backups disponíveis
        
        Args:
            backup_dir (str, optional): Diretório onde procurar backups.
                                       Se None, usa o diretório padrão 'backups/'
        
        Returns:
            list: Lista de dicionários com informações dos backups.
                  Cada dicionário contém:
                  - filename (str): Nome do arquivo
                  - filepath (str): Caminho completo do arquivo
                  - size (int): Tamanho em bytes
                  - date (str): Data de criação formatada
        """
        if backup_dir is None:
            backup_dir = self.backup_dir
        
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
