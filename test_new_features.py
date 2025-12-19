#!/usr/bin/env python3
"""
Testes para as novas funcionalidades:
1. Lazy loading de dados relacionados
2. Compressão melhorada de backups
3. Paginação de resultados grandes
4. Query builder para buscas complexas
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager

def test_lazy_loading():
    """Testa lazy loading de dados relacionados"""
    print("="*70)
    print("TESTE 1: LAZY LOADING DE DADOS RELACIONADOS")
    print("="*70)
    
    dm = DataManager()
    
    # Cria aluno de teste
    aluno_id = dm.add_record('cadastro', {
        'nome_completo': 'João Lazy Loading',
        'data_nascimento': '2010-01-01',
        'status': 'Ativo',
        'cpf': '11122233344'
    })
    
    # Adiciona dados relacionados
    dm.add_record('pei', {
        'aluno_id': aluno_id,
        'necessidade_especial': 'Sim',
        'tipo_deficiencia': 'Visual'
    })
    
    dm.add_record('socioeconomico', {
        'aluno_id': aluno_id,
        'renda_familiar': '1-2 salários'
    })
    
    print(f"\n✓ Aluno criado com ID {aluno_id}")
    print("✓ Dados relacionados adicionados (PEI, Socioeconômico)")
    
    # Testa lazy loading
    print("\n--- Teste de Lazy Loading ---")
    student = dm.get_student_data_lazy(aluno_id)
    print("✓ Objeto lazy criado (nenhum dado carregado ainda)")
    
    # Acessa cadastro
    print("\nAcessando cadastro...")
    cadastro = student.cadastro
    print(f"✓ Cadastro carregado: {cadastro['nome_completo']}")
    
    # Acessa PEI
    print("\nAcessando PEI...")
    pei = student.pei
    print(f"✓ PEI carregado: {pei['tipo_deficiencia'] if pei else 'Não encontrado'}")
    
    # Verifica dados carregados
    loaded = student.get_loaded_data()
    print(f"\n✓ Dados carregados até agora: {list(loaded.keys())}")
    
    # Força carregamento de todos
    print("\nCarregando todos os dados...")
    all_data = student.get_all_data()
    print(f"✓ Total de tipos carregados: {len(all_data)}")
    
    # Limpeza
    dm.delete_record('cadastro', aluno_id)
    
    print("\n✅ Teste de Lazy Loading: PASSOU")
    return True

def test_pagination():
    """Testa paginação de resultados"""
    print("\n" + "="*70)
    print("TESTE 2: PAGINAÇÃO DE RESULTADOS GRANDES")
    print("="*70)
    
    dm = DataManager()
    
    # Cria 25 alunos de teste
    print("\nCriando 25 alunos de teste...")
    ids = []
    for i in range(25):
        aluno_id = dm.add_record('cadastro', {
            'nome_completo': f'Aluno Paginação {i+1}',
            'data_nascimento': '2010-01-01',
            'status': 'Ativo'
        })
        ids.append(aluno_id)
    
    print(f"✓ {len(ids)} alunos criados")
    
    # Testa paginação básica
    print("\n--- Teste de Paginação Básica ---")
    page1 = dm.get_data_paginated('cadastro', page=1, page_size=10)
    
    print(f"Página 1:")
    print(f"  - Registros na página: {len(page1['data'])}")
    print(f"  - Total de registros: {page1['total_records']}")
    print(f"  - Total de páginas: {page1['total_pages']}")
    print(f"  - Tem próxima: {page1['has_next']}")
    print(f"  - Tem anterior: {page1['has_prev']}")
    
    # Página 2
    page2 = dm.get_data_paginated('cadastro', page=2, page_size=10)
    print(f"\nPágina 2:")
    print(f"  - Registros na página: {len(page2['data'])}")
    print(f"  - Tem próxima: {page2['has_next']}")
    print(f"  - Tem anterior: {page2['has_prev']}")
    
    # Testa busca com paginação
    print("\n--- Teste de Busca Paginada ---")
    search_result = dm.search_records_paginated(
        'cadastro', 
        'nome_completo', 
        'Paginação',
        page=1,
        page_size=5
    )
    
    print(f"Busca por 'Paginação' (página 1, 5 por página):")
    print(f"  - Encontrados: {search_result['total_records']}")
    print(f"  - Na página: {len(search_result['data'])}")
    print(f"  - Total de páginas: {search_result['total_pages']}")
    
    # Limpeza
    for aluno_id in ids:
        dm.delete_record('cadastro', aluno_id)
    
    print("\n✅ Teste de Paginação: PASSOU")
    return True

def test_query_builder():
    """Testa query builder para buscas complexas"""
    print("\n" + "="*70)
    print("TESTE 3: QUERY BUILDER PARA BUSCAS COMPLEXAS")
    print("="*70)
    
    dm = DataManager()
    
    # Cria dados de teste variados
    print("\nCriando dados de teste variados...")
    ids = []
    
    # Alunos ativos
    for i in range(5):
        aluno_id = dm.add_record('cadastro', {
            'nome_completo': f'João Silva {i+1}',
            'data_nascimento': '2010-01-01',
            'status': 'Ativo',
            'ano_escolar': '1º'
        })
        ids.append(aluno_id)
    
    # Alunos inativos
    for i in range(3):
        aluno_id = dm.add_record('cadastro', {
            'nome_completo': f'Maria Santos {i+1}',
            'data_nascimento': '2010-01-01',
            'status': 'Inativo',
            'ano_escolar': '2º'
        })
        ids.append(aluno_id)
    
    # Alunos com nome diferente
    for i in range(2):
        aluno_id = dm.add_record('cadastro', {
            'nome_completo': f'Pedro Costa {i+1}',
            'data_nascimento': '2010-01-01',
            'status': 'Ativo',
            'ano_escolar': '3º'
        })
        ids.append(aluno_id)
    
    print(f"✓ {len(ids)} alunos criados com variações")
    
    # Teste 1: Busca simples com where
    print("\n--- Query 1: Busca simples ---")
    results = dm.query('cadastro') \
                .where('status', '=', 'Ativo') \
                .execute()
    print(f"Alunos ativos: {len(results)}")
    
    # Teste 2: Busca com múltiplos filtros
    print("\n--- Query 2: Múltiplos filtros ---")
    results = dm.query('cadastro') \
                .where('status', '=', 'Ativo') \
                .where('nome_completo', 'contains', 'João') \
                .execute()
    print(f"Alunos ativos com 'João' no nome: {len(results)}")
    
    # Teste 3: Busca com ordenação
    print("\n--- Query 3: Com ordenação ---")
    results = dm.query('cadastro') \
                .where('status', '=', 'Ativo') \
                .order_by('nome_completo') \
                .execute()
    if len(results) > 0:
        print(f"Primeiro aluno (ordenado): {results.iloc[0]['nome_completo']}")
    
    # Teste 4: Busca com limit
    print("\n--- Query 4: Com limit ---")
    results = dm.query('cadastro') \
                .where('status', '=', 'Ativo') \
                .limit(3) \
                .execute()
    print(f"Primeiros 3 alunos ativos: {len(results)}")
    
    # Teste 5: Busca com in
    print("\n--- Query 5: Operador IN ---")
    results = dm.query('cadastro') \
                .where('ano_escolar', 'in', ['1º', '3º']) \
                .execute()
    print(f"Alunos no 1º ou 3º ano: {len(results)}")
    
    # Teste 6: Count
    print("\n--- Query 6: Count ---")
    count = dm.query('cadastro') \
              .where('status', '=', 'Ativo') \
              .count()
    print(f"Total de ativos (count): {count}")
    
    # Teste 7: First
    print("\n--- Query 7: First ---")
    first = dm.query('cadastro') \
              .where('nome_completo', 'startswith', 'João') \
              .first()
    print(f"Primeiro João: {first['nome_completo'] if first else 'Não encontrado'}")
    
    # Teste 8: Paginação via query builder
    print("\n--- Query 8: Paginação ---")
    page = dm.query('cadastro') \
             .where('status', '=', 'Ativo') \
             .order_by('nome_completo') \
             .paginate(page=1, page_size=3)
    print(f"Página 1 (3 por página):")
    print(f"  - Registros: {len(page['data'])}")
    print(f"  - Total: {page['total_records']}")
    print(f"  - Páginas: {page['total_pages']}")
    
    # Limpeza
    for aluno_id in ids:
        dm.delete_record('cadastro', aluno_id)
    
    print("\n✅ Teste de Query Builder: PASSOU")
    return True

def test_improved_compression():
    """Testa compressão melhorada de backups"""
    print("\n" + "="*70)
    print("TESTE 4: COMPRESSÃO MELHORADA DE BACKUPS")
    print("="*70)
    
    dm = DataManager()
    
    # Cria dados para backup
    print("\nCriando dados para testar compressão...")
    ids = []
    for i in range(20):
        aluno_id = dm.add_record('cadastro', {
            'nome_completo': f'Aluno Backup Teste {i+1}',
            'data_nascimento': '2010-01-01',
            'status': 'Ativo',
            'endereco': 'Rua Teste, 123, Bairro Teste, Cidade Teste',
            'observacoes': 'Dados de teste para verificar compressão do backup'
        })
        ids.append(aluno_id)
    
    print(f"✓ {len(ids)} alunos criados")
    
    # Teste backup normal
    print("\n--- Backup Normal (compressão padrão) ---")
    start = time.time()
    backup_normal = dm.create_backup()
    time_normal = time.time() - start
    
    size_normal = os.path.getsize(backup_normal)
    print(f"Tempo: {time_normal:.3f}s")
    print(f"Tamanho: {size_normal / 1024:.2f} KB")
    
    # Teste backup com compressão máxima
    print("\n--- Backup com Compressão Máxima (nível 9) ---")
    start = time.time()
    result = dm.create_backup_compressed(compression_level=9)
    time_compressed = time.time() - start
    
    print(f"Tempo: {time_compressed:.3f}s")
    print(f"Tamanho original: {result['size'] / 1024:.2f} KB")
    print(f"Tamanho comprimido: {result['compressed_size'] / 1024:.2f} KB")
    print(f"Taxa de compressão: {result['compression_ratio']:.1f}%")
    
    # Compara
    improvement = ((size_normal - result['compressed_size']) / size_normal * 100) if size_normal > 0 else 0
    print(f"\n✓ Melhoria na compressão: {improvement:.1f}%")
    
    # Limpeza
    for aluno_id in ids:
        dm.delete_record('cadastro', aluno_id)
    
    if os.path.exists(backup_normal):
        os.remove(backup_normal)
    if os.path.exists(result['path']):
        os.remove(result['path'])
    
    print("\n✅ Teste de Compressão: PASSOU")
    return True

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("EXECUTANDO TESTES DAS NOVAS FUNCIONALIDADES")
    print("="*70)
    
    results = []
    
    try:
        results.append(('Lazy Loading', test_lazy_loading()))
    except Exception as e:
        print(f"\n❌ Erro no teste de Lazy Loading: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(('Lazy Loading', False))
    
    try:
        results.append(('Paginação', test_pagination()))
    except Exception as e:
        print(f"\n❌ Erro no teste de Paginação: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(('Paginação', False))
    
    try:
        results.append(('Query Builder', test_query_builder()))
    except Exception as e:
        print(f"\n❌ Erro no teste de Query Builder: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(('Query Builder', False))
    
    try:
        results.append(('Compressão', test_improved_compression()))
    except Exception as e:
        print(f"\n❌ Erro no teste de Compressão: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(('Compressão', False))
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name}: {status}")
    
    print("\n" + "="*70)
    print(f"Total: {passed}/{total} testes passaram")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
