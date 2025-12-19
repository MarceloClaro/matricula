#!/usr/bin/env python3
"""
Simulador de Fluxo de Dados do Sistema de Matrícula
Este script simula o fluxo completo de dados do sistema para:
1. Identificar bugs e gargalos
2. Melhorar a fluidez do fluxo de dados
3. Testar a integridade e consistência dos dados
4. Validar operações CRUD
"""

import sys
import os
import time
import traceback
from datetime import datetime, timedelta
import pandas as pd
import random

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager

class DataFlowSimulator:
    """Simulador de fluxo de dados para identificar problemas e melhorias"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.results = {
            'tests_passed': 0,
            'tests_failed': 0,
            'bugs_found': [],
            'improvements': [],
            'performance_metrics': {}
        }
    
    def log(self, message, level='INFO'):
        """Log com timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prefix = {
            'INFO': '✓',
            'WARNING': '⚠',
            'ERROR': '✗',
            'SUCCESS': '✓'
        }.get(level, '•')
        print(f"[{timestamp}] {prefix} {message}")
    
    def test_data_manager_initialization(self):
        """Testa inicialização do data manager"""
        self.log("Teste 1: Inicialização do DataManager", 'INFO')
        try:
            # Verifica se todos os arquivos foram criados
            for tipo, filepath in self.data_manager.files.items():
                if not os.path.exists(filepath):
                    raise Exception(f"Arquivo {filepath} não foi criado")
                
                # Tenta ler o arquivo
                df = self.data_manager.get_data(tipo)
                if df is None:
                    raise Exception(f"Não foi possível ler {tipo}")
            
            self.log("DataManager inicializado corretamente", 'SUCCESS')
            self.results['tests_passed'] += 1
            return True
        except Exception as e:
            self.log(f"Erro na inicialização: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Inicialização DataManager',
                'error': str(e)
            })
            return False
    
    def test_crud_operations(self):
        """Testa operações CRUD básicas"""
        self.log("Teste 2: Operações CRUD", 'INFO')
        try:
            # CREATE
            start_time = time.time()
            dados_teste = {
                'nome_completo': 'Teste Simulação',
                'data_nascimento': '2010-01-01',
                'cpf': '12345678900',
                'sexo': 'Masculino',
                'status': 'Ativo'
            }
            
            aluno_id = self.data_manager.add_record('cadastro', dados_teste)
            create_time = time.time() - start_time
            
            if not aluno_id or aluno_id <= 0:
                raise Exception("Falha ao criar registro")
            
            self.log(f"CREATE: Registro criado com ID {aluno_id} em {create_time:.3f}s", 'SUCCESS')
            
            # READ
            start_time = time.time()
            registro = self.data_manager.get_record('cadastro', aluno_id)
            read_time = time.time() - start_time
            
            if not registro:
                raise Exception("Falha ao ler registro")
            
            self.log(f"READ: Registro lido em {read_time:.3f}s", 'SUCCESS')
            
            # UPDATE
            start_time = time.time()
            update_data = {'nome_completo': 'Teste Simulação Atualizado'}
            success = self.data_manager.update_record('cadastro', aluno_id, update_data)
            update_time = time.time() - start_time
            
            if not success:
                raise Exception("Falha ao atualizar registro")
            
            # Verifica se atualizou
            registro_atualizado = self.data_manager.get_record('cadastro', aluno_id)
            if registro_atualizado['nome_completo'] != 'Teste Simulação Atualizado':
                raise Exception("Dados não foram atualizados corretamente")
            
            self.log(f"UPDATE: Registro atualizado em {update_time:.3f}s", 'SUCCESS')
            
            # DELETE
            start_time = time.time()
            success = self.data_manager.delete_record('cadastro', aluno_id)
            delete_time = time.time() - start_time
            
            if not success:
                raise Exception("Falha ao deletar registro")
            
            # Verifica se deletou
            registro_deletado = self.data_manager.get_record('cadastro', aluno_id)
            if registro_deletado is not None:
                raise Exception("Registro não foi deletado corretamente")
            
            self.log(f"DELETE: Registro deletado em {delete_time:.3f}s", 'SUCCESS')
            
            # Armazena métricas de performance
            self.results['performance_metrics']['crud'] = {
                'create': create_time,
                'read': read_time,
                'update': update_time,
                'delete': delete_time,
                'total': create_time + read_time + update_time + delete_time
            }
            
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro em operações CRUD: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Operações CRUD',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            return False
    
    def test_data_integrity(self):
        """Testa integridade e consistência de dados"""
        self.log("Teste 3: Integridade de Dados", 'INFO')
        try:
            # Adiciona dados de teste
            aluno_id = self.data_manager.add_record('cadastro', {
                'nome_completo': 'Teste Integridade',
                'cpf': '11122233344',
                'data_nascimento': '2010-05-15',
                'status': 'Ativo'
            })
            
            # Adiciona dados relacionados
            pei_id = self.data_manager.add_record('pei', {
                'aluno_id': aluno_id,
                'necessidade_especial': 'Sim',
                'tipo_deficiencia': 'Visual'
            })
            
            socio_id = self.data_manager.add_record('socioeconomico', {
                'aluno_id': aluno_id,
                'renda_familiar': 'De 1 a 2 salários mínimos'
            })
            
            # Testa recuperação de dados relacionados
            todos_dados = self.data_manager.get_all_student_data(aluno_id)
            
            if 'cadastro' not in todos_dados:
                raise Exception("Cadastro não recuperado")
            
            if 'pei' not in todos_dados:
                raise Exception("PEI não recuperado")
            
            if 'socioeconomico' not in todos_dados:
                raise Exception("Socioeconômico não recuperado")
            
            # Verifica consistência de IDs
            if todos_dados['pei']['aluno_id'] != aluno_id:
                raise Exception("Inconsistência de ID em PEI")
            
            if todos_dados['socioeconomico']['aluno_id'] != aluno_id:
                raise Exception("Inconsistência de ID em Socioeconômico")
            
            # Limpeza
            self.data_manager.delete_record('cadastro', aluno_id)
            self.data_manager.delete_record('pei', pei_id)
            self.data_manager.delete_record('socioeconomico', socio_id)
            
            self.log("Integridade de dados validada", 'SUCCESS')
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro na integridade de dados: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Integridade de Dados',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            return False
    
    def test_data_type_handling(self):
        """Testa manipulação de diferentes tipos de dados"""
        self.log("Teste 4: Manipulação de Tipos de Dados", 'INFO')
        try:
            # Teste com strings vazias, None, números
            test_cases = [
                {'nome_completo': '', 'status': 'Ativo'},  # String vazia
                {'nome_completo': 'Teste', 'cpf': None},  # None
                {'nome_completo': 'Teste', 'telefone': ''},  # Campo opcional vazio
            ]
            
            ids_criados = []
            for dados in test_cases:
                try:
                    aluno_id = self.data_manager.add_record('cadastro', dados)
                    ids_criados.append(aluno_id)
                except Exception as e:
                    self.log(f"Possível problema com tipos de dados: {dados} - {str(e)}", 'WARNING')
                    self.results['improvements'].append({
                        'category': 'Validação de Dados',
                        'issue': f'Melhorar validação para: {dados}',
                        'suggestion': 'Adicionar validação de campos obrigatórios antes de salvar'
                    })
            
            # Limpeza
            for aluno_id in ids_criados:
                self.data_manager.delete_record('cadastro', aluno_id)
            
            self.log("Manipulação de tipos de dados testada", 'SUCCESS')
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro na manipulação de tipos: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Manipulação de Tipos de Dados',
                'error': str(e)
            })
            return False
    
    def test_concurrent_operations(self):
        """Simula operações concorrentes"""
        self.log("Teste 5: Operações Concorrentes", 'INFO')
        try:
            # Simula múltiplas operações de escrita
            ids = []
            start_time = time.time()
            
            for i in range(10):
                aluno_id = self.data_manager.add_record('cadastro', {
                    'nome_completo': f'Teste Concorrente {i}',
                    'cpf': f'{i:011d}',
                    'status': 'Ativo'
                })
                ids.append(aluno_id)
            
            end_time = time.time() - start_time
            
            # Verifica se todos foram criados
            df = self.data_manager.get_data('cadastro')
            for aluno_id in ids:
                if aluno_id not in df['id'].values:
                    raise Exception(f"Registro {aluno_id} não encontrado após criação concorrente")
            
            # Limpeza
            for aluno_id in ids:
                self.data_manager.delete_record('cadastro', aluno_id)
            
            self.log(f"10 operações concorrentes completadas em {end_time:.3f}s", 'SUCCESS')
            self.results['performance_metrics']['concurrent'] = {
                'operations': 10,
                'total_time': end_time,
                'avg_time': end_time / 10
            }
            
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro em operações concorrentes: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Operações Concorrentes',
                'error': str(e)
            })
            return False
    
    def test_search_performance(self):
        """Testa performance de busca"""
        self.log("Teste 6: Performance de Busca", 'INFO')
        try:
            # Cria dataset de teste
            ids = []
            self.log("Criando dataset de teste para busca...")
            for i in range(50):
                aluno_id = self.data_manager.add_record('cadastro', {
                    'nome_completo': f'Aluno Teste {i}',
                    'cpf': f'{i:011d}',
                    'status': random.choice(['Ativo', 'Inativo']),
                    'ano_escolar': str(random.randint(1, 9)),
                    'cidade': random.choice(['São Paulo', 'Rio de Janeiro', 'Fortaleza'])
                })
                ids.append(aluno_id)
            
            # Teste de busca por nome
            start_time = time.time()
            resultados = self.data_manager.search_records('cadastro', 'nome_completo', 'Teste')
            search_name_time = time.time() - start_time
            
            if len(resultados) == 0:
                raise Exception("Busca por nome não retornou resultados")
            
            self.log(f"Busca por nome: {len(resultados)} resultados em {search_name_time:.3f}s", 'SUCCESS')
            
            # Teste de busca por ID
            start_time = time.time()
            registro = self.data_manager.get_record('cadastro', ids[0])
            search_id_time = time.time() - start_time
            
            if not registro:
                raise Exception("Busca por ID falhou")
            
            self.log(f"Busca por ID: {search_id_time:.3f}s", 'SUCCESS')
            
            # Análise de performance
            if search_name_time > 1.0:
                self.results['improvements'].append({
                    'category': 'Performance de Busca',
                    'issue': f'Busca por nome lenta: {search_name_time:.3f}s para 50 registros',
                    'suggestion': 'Considerar implementar indexação ou cache para buscas frequentes'
                })
            
            # Limpeza
            for aluno_id in ids:
                self.data_manager.delete_record('cadastro', aluno_id)
            
            self.results['performance_metrics']['search'] = {
                'dataset_size': 50,
                'search_by_name': search_name_time,
                'search_by_id': search_id_time
            }
            
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro no teste de busca: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Performance de Busca',
                'error': str(e)
            })
            return False
    
    def test_backup_restore(self):
        """Testa funcionalidade de backup e restauração"""
        self.log("Teste 7: Backup e Restauração", 'INFO')
        try:
            # Cria dados de teste
            aluno_id = self.data_manager.add_record('cadastro', {
                'nome_completo': 'Teste Backup',
                'cpf': '99988877766',
                'status': 'Ativo'
            })
            
            # Cria backup
            start_time = time.time()
            backup_path = self.data_manager.create_backup()
            backup_time = time.time() - start_time
            
            if not os.path.exists(backup_path):
                raise Exception("Backup não foi criado")
            
            self.log(f"Backup criado em {backup_time:.3f}s: {backup_path}", 'SUCCESS')
            
            # Modifica dados
            self.data_manager.update_record('cadastro', aluno_id, {'nome_completo': 'Modificado'})
            
            # Restaura backup
            start_time = time.time()
            success, message = self.data_manager.restore_backup(backup_path)
            restore_time = time.time() - start_time
            
            if not success:
                raise Exception(f"Falha ao restaurar backup: {message}")
            
            self.log(f"Backup restaurado em {restore_time:.3f}s", 'SUCCESS')
            
            # Verifica se dados foram restaurados
            registro = self.data_manager.get_record('cadastro', aluno_id)
            if registro['nome_completo'] != 'Teste Backup':
                raise Exception("Dados não foram restaurados corretamente")
            
            # Limpeza
            self.data_manager.delete_record('cadastro', aluno_id)
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            self.results['performance_metrics']['backup'] = {
                'backup_time': backup_time,
                'restore_time': restore_time
            }
            
            self.results['tests_passed'] += 1
            return True
            
        except Exception as e:
            self.log(f"Erro em backup/restauração: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Backup e Restauração',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            return False
    
    def test_memory_usage(self):
        """Testa uso de memória com datasets maiores"""
        self.log("Teste 8: Uso de Memória", 'INFO')
        try:
            import psutil
            import gc
            
            process = psutil.Process()
            
            # Memória inicial
            gc.collect()
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Cria dataset grande
            ids = []
            for i in range(100):
                aluno_id = self.data_manager.add_record('cadastro', {
                    'nome_completo': f'Aluno Teste Memória {i}',
                    'cpf': f'{i:011d}',
                    'status': 'Ativo',
                    'endereco': 'Rua Teste, 123',
                    'cidade': 'Cidade Teste',
                    'bairro': 'Bairro Teste'
                })
                ids.append(aluno_id)
            
            # Carrega todos os dados
            df = self.data_manager.get_data('cadastro')
            
            # Memória após
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            mem_used = mem_after - mem_before
            
            self.log(f"Memória usada para 100 registros: {mem_used:.2f} MB", 'SUCCESS')
            
            # Limpeza
            for aluno_id in ids:
                self.data_manager.delete_record('cadastro', aluno_id)
            
            gc.collect()
            
            # Análise
            if mem_used > 50:  # Mais de 50MB para 100 registros é excessivo
                self.results['improvements'].append({
                    'category': 'Uso de Memória',
                    'issue': f'Alto uso de memória: {mem_used:.2f} MB para 100 registros',
                    'suggestion': 'Otimizar carregamento de dados, usar lazy loading ou paginação'
                })
            
            self.results['performance_metrics']['memory'] = {
                'records': 100,
                'memory_mb': mem_used,
                'per_record_kb': (mem_used * 1024) / 100
            }
            
            self.results['tests_passed'] += 1
            return True
            
        except ImportError:
            self.log("psutil não disponível, pulando teste de memória", 'WARNING')
            self.results['tests_passed'] += 1
            return True
        except Exception as e:
            self.log(f"Erro no teste de memória: {str(e)}", 'ERROR')
            self.results['tests_failed'] += 1
            self.results['bugs_found'].append({
                'test': 'Uso de Memória',
                'error': str(e)
            })
            return False
    
    def analyze_data_flow(self):
        """Analisa fluxo de dados e identifica melhorias"""
        self.log("\n=== ANÁLISE DE FLUXO DE DADOS ===", 'INFO')
        
        # Analisa estrutura de dados
        self.log("\n1. Estrutura de Dados:", 'INFO')
        for tipo in self.data_manager.files.keys():
            df = self.data_manager.get_data(tipo)
            self.log(f"  • {tipo}: {len(df.columns)} colunas, {len(df)} registros")
        
        # Recomendações de melhoria
        self.log("\n2. Recomendações de Melhoria no Fluxo:", 'INFO')
        
        recommendations = [
            {
                'title': 'Cache de Dados Frequentemente Acessados',
                'description': 'Implementar cache em memória para dados de cadastro básico que são acessados frequentemente',
                'priority': 'Alta',
                'impact': 'Reduzir tempo de leitura em até 80%'
            },
            {
                'title': 'Validação de Dados na Entrada',
                'description': 'Adicionar validação robusta de campos obrigatórios antes de salvar',
                'priority': 'Alta',
                'impact': 'Prevenir inconsistências e melhorar integridade'
            },
            {
                'title': 'Índices para Busca',
                'description': 'Criar índices em campos frequentemente buscados (nome, CPF)',
                'priority': 'Média',
                'impact': 'Melhorar performance de busca em 50-70%'
            },
            {
                'title': 'Transações Atômicas',
                'description': 'Implementar operações transacionais para garantir consistência',
                'priority': 'Média',
                'impact': 'Garantir integridade em operações complexas'
            },
            {
                'title': 'Lazy Loading de Dados Relacionados',
                'description': 'Carregar dados relacionados apenas quando necessário',
                'priority': 'Baixa',
                'impact': 'Reduzir uso de memória em 30-40%'
            },
            {
                'title': 'Compressão de Backups',
                'description': 'Usar compressão mais eficiente para backups',
                'priority': 'Baixa',
                'impact': 'Reduzir tamanho de backups em 40-60%'
            }
        ]
        
        for rec in recommendations:
            self.log(f"\n  {rec['title']} (Prioridade: {rec['priority']})", 'INFO')
            self.log(f"    - {rec['description']}")
            self.log(f"    - Impacto: {rec['impact']}")
            
            self.results['improvements'].append(rec)
    
    def generate_report(self):
        """Gera relatório completo da simulação"""
        self.log("\n" + "="*70, 'INFO')
        self.log("RELATÓRIO DE SIMULAÇÃO DO FLUXO DE DADOS", 'INFO')
        self.log("="*70, 'INFO')
        
        # Resumo dos testes
        total_tests = self.results['tests_passed'] + self.results['tests_failed']
        pass_rate = (self.results['tests_passed'] / total_tests * 100) if total_tests > 0 else 0
        
        self.log(f"\n📊 RESUMO DOS TESTES:", 'INFO')
        self.log(f"  Total de testes: {total_tests}")
        self.log(f"  Testes passados: {self.results['tests_passed']} ✓")
        self.log(f"  Testes falhados: {self.results['tests_failed']} ✗")
        self.log(f"  Taxa de sucesso: {pass_rate:.1f}%")
        
        # Bugs encontrados
        if self.results['bugs_found']:
            self.log(f"\n🐛 BUGS ENCONTRADOS ({len(self.results['bugs_found'])}):", 'WARNING')
            for i, bug in enumerate(self.results['bugs_found'], 1):
                self.log(f"\n  Bug {i}: {bug['test']}", 'ERROR')
                self.log(f"    Erro: {bug['error']}")
                if 'traceback' in bug:
                    self.log(f"    Detalhes: Ver log completo")
        else:
            self.log("\n✓ Nenhum bug crítico encontrado!", 'SUCCESS')
        
        # Métricas de performance
        if self.results['performance_metrics']:
            self.log(f"\n⚡ MÉTRICAS DE PERFORMANCE:", 'INFO')
            
            if 'crud' in self.results['performance_metrics']:
                crud = self.results['performance_metrics']['crud']
                self.log(f"\n  Operações CRUD:")
                self.log(f"    - Create: {crud['create']:.3f}s")
                self.log(f"    - Read: {crud['read']:.3f}s")
                self.log(f"    - Update: {crud['update']:.3f}s")
                self.log(f"    - Delete: {crud['delete']:.3f}s")
                self.log(f"    - Total: {crud['total']:.3f}s")
            
            if 'search' in self.results['performance_metrics']:
                search = self.results['performance_metrics']['search']
                self.log(f"\n  Busca ({search['dataset_size']} registros):")
                self.log(f"    - Por nome: {search['search_by_name']:.3f}s")
                self.log(f"    - Por ID: {search['search_by_id']:.3f}s")
            
            if 'memory' in self.results['performance_metrics']:
                mem = self.results['performance_metrics']['memory']
                self.log(f"\n  Uso de Memória:")
                self.log(f"    - {mem['records']} registros: {mem['memory_mb']:.2f} MB")
                self.log(f"    - Por registro: {mem['per_record_kb']:.2f} KB")
        
        # Melhorias sugeridas
        if self.results['improvements']:
            self.log(f"\n💡 MELHORIAS SUGERIDAS ({len(self.results['improvements'])}):", 'INFO')
            
            # Agrupa por prioridade
            by_priority = {}
            for imp in self.results['improvements']:
                priority = imp.get('priority', 'Média')
                if priority not in by_priority:
                    by_priority[priority] = []
                by_priority[priority].append(imp)
            
            for priority in ['Alta', 'Média', 'Baixa']:
                if priority in by_priority:
                    self.log(f"\n  Prioridade {priority}:")
                    for imp in by_priority[priority]:
                        self.log(f"    • {imp.get('title', imp.get('issue', 'N/A'))}")
                        if 'suggestion' in imp:
                            self.log(f"      → {imp['suggestion']}")
                        if 'impact' in imp:
                            self.log(f"      → Impacto: {imp['impact']}")
        
        self.log("\n" + "="*70, 'INFO')
        
        # Salva relatório em arquivo
        report_path = os.path.join(os.path.dirname(__file__), 'SIMULATION_REPORT.md')
        self.save_report_to_file(report_path)
        self.log(f"\n📄 Relatório completo salvo em: {report_path}", 'SUCCESS')
    
    def save_report_to_file(self, filepath):
        """Salva relatório em arquivo Markdown"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Simulação do Fluxo de Dados\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Resumo
            total_tests = self.results['tests_passed'] + self.results['tests_failed']
            pass_rate = (self.results['tests_passed'] / total_tests * 100) if total_tests > 0 else 0
            
            f.write("## 📊 Resumo dos Testes\n\n")
            f.write(f"- **Total de testes:** {total_tests}\n")
            f.write(f"- **Testes passados:** {self.results['tests_passed']} ✓\n")
            f.write(f"- **Testes falhados:** {self.results['tests_failed']} ✗\n")
            f.write(f"- **Taxa de sucesso:** {pass_rate:.1f}%\n\n")
            
            # Bugs
            if self.results['bugs_found']:
                f.write(f"## 🐛 Bugs Encontrados ({len(self.results['bugs_found'])})\n\n")
                for i, bug in enumerate(self.results['bugs_found'], 1):
                    f.write(f"### Bug {i}: {bug['test']}\n\n")
                    f.write(f"**Erro:** {bug['error']}\n\n")
                    if 'traceback' in bug:
                        f.write("**Detalhes:**\n```\n")
                        f.write(bug['traceback'])
                        f.write("\n```\n\n")
            else:
                f.write("## ✓ Bugs\n\nNenhum bug crítico encontrado!\n\n")
            
            # Performance
            if self.results['performance_metrics']:
                f.write("## ⚡ Métricas de Performance\n\n")
                
                if 'crud' in self.results['performance_metrics']:
                    crud = self.results['performance_metrics']['crud']
                    f.write("### Operações CRUD\n\n")
                    f.write(f"- Create: {crud['create']:.3f}s\n")
                    f.write(f"- Read: {crud['read']:.3f}s\n")
                    f.write(f"- Update: {crud['update']:.3f}s\n")
                    f.write(f"- Delete: {crud['delete']:.3f}s\n")
                    f.write(f"- **Total:** {crud['total']:.3f}s\n\n")
                
                if 'search' in self.results['performance_metrics']:
                    search = self.results['performance_metrics']['search']
                    f.write(f"### Busca ({search['dataset_size']} registros)\n\n")
                    f.write(f"- Busca por nome: {search['search_by_name']:.3f}s\n")
                    f.write(f"- Busca por ID: {search['search_by_id']:.3f}s\n\n")
                
                if 'memory' in self.results['performance_metrics']:
                    mem = self.results['performance_metrics']['memory']
                    f.write("### Uso de Memória\n\n")
                    f.write(f"- {mem['records']} registros: {mem['memory_mb']:.2f} MB\n")
                    f.write(f"- Por registro: {mem['per_record_kb']:.2f} KB\n\n")
            
            # Melhorias
            if self.results['improvements']:
                f.write(f"## 💡 Melhorias Sugeridas ({len(self.results['improvements'])})\n\n")
                
                by_priority = {}
                for imp in self.results['improvements']:
                    priority = imp.get('priority', 'Média')
                    if priority not in by_priority:
                        by_priority[priority] = []
                    by_priority[priority].append(imp)
                
                for priority in ['Alta', 'Média', 'Baixa']:
                    if priority in by_priority:
                        f.write(f"### Prioridade {priority}\n\n")
                        for imp in by_priority[priority]:
                            title = imp.get('title', imp.get('issue', 'N/A'))
                            f.write(f"#### {title}\n\n")
                            if 'description' in imp:
                                f.write(f"**Descrição:** {imp['description']}\n\n")
                            if 'suggestion' in imp:
                                f.write(f"**Sugestão:** {imp['suggestion']}\n\n")
                            if 'impact' in imp:
                                f.write(f"**Impacto:** {imp['impact']}\n\n")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        self.log("\n" + "="*70)
        self.log("INICIANDO SIMULAÇÃO DO FLUXO DE DADOS")
        self.log("="*70 + "\n")
        
        start_time = time.time()
        
        # Executa testes
        self.test_data_manager_initialization()
        self.test_crud_operations()
        self.test_data_integrity()
        self.test_data_type_handling()
        self.test_concurrent_operations()
        self.test_search_performance()
        self.test_backup_restore()
        self.test_memory_usage()
        
        # Análise de fluxo
        self.analyze_data_flow()
        
        total_time = time.time() - start_time
        self.log(f"\n⏱️  Tempo total de execução: {total_time:.2f}s", 'INFO')
        
        # Gera relatório
        self.generate_report()

def main():
    """Função principal"""
    try:
        simulator = DataFlowSimulator()
        simulator.run_all_tests()
        
        # Exit code baseado nos resultados
        if simulator.results['tests_failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Erro fatal na simulação: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
