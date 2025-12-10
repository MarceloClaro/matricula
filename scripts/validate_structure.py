#!/usr/bin/env python3
"""
Script de validação da estrutura do código
Verifica imports e estrutura sem executar o código completo
"""
import os
import sys
import ast

def check_file_syntax(filepath):
    """Verifica sintaxe de um arquivo Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
            ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def check_imports(filepath):
    """Verifica imports de um arquivo Python"""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        return imports
    except Exception as e:
        print(f"Erro ao analisar imports de {filepath}: {e}")
        return []

def main():
    """Função principal de validação"""
    print("=" * 60)
    print("VALIDAÇÃO DA ESTRUTURA DO CÓDIGO")
    print("=" * 60)
    print()
    
    # Get base directory relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Go up one level from scripts/
    
    # Arquivos para validar
    files_to_check = [
        "app.py",
        "data_manager.py",
        "modulos/reconhecimento_facial.py",
        "modulos/registro_presenca.py",
        "modulos/frequencia_aula.py",
    ]
    
    print("1. Verificando sintaxe dos arquivos...")
    print("-" * 60)
    
    all_valid = True
    for filepath in files_to_check:
        full_path = os.path.join(base_dir, filepath)
        if os.path.exists(full_path):
            valid, error = check_file_syntax(full_path)
            status = "✓ OK" if valid else f"✗ ERRO: {error}"
            print(f"{filepath:45} {status}")
            if not valid:
                all_valid = False
        else:
            print(f"{filepath:45} ✗ ARQUIVO NÃO ENCONTRADO")
            all_valid = False
    
    print()
    print("2. Verificando estrutura de diretórios...")
    print("-" * 60)
    
    dirs_to_check = [
        "data",
        "modulos",
        "scripts",
    ]
    
    for dirname in dirs_to_check:
        full_path = os.path.join(base_dir, dirname)
        exists = os.path.exists(full_path)
        status = "✓ OK" if exists else "✗ NÃO EXISTE"
        print(f"{dirname:45} {status}")
    
    print()
    print("3. Verificando arquivos de configuração...")
    print("-" * 60)
    
    config_files = [
        "requirements.txt",
        "README.md",
    ]
    
    for filename in config_files:
        full_path = os.path.join(base_dir, filename)
        exists = os.path.exists(full_path)
        status = "✓ OK" if exists else "✗ NÃO EXISTE"
        print(f"{filename:45} {status}")
    
    print()
    print("4. Verificando imports dos novos módulos...")
    print("-" * 60)
    
    # Verificar imports do reconhecimento_facial.py
    rf_path = os.path.join(base_dir, "modulos/reconhecimento_facial.py")
    if os.path.exists(rf_path):
        imports = check_imports(rf_path)
        expected_imports = ['cv2', 'face_recognition', 'numpy', 'pickle', 
                          'tensorflow', 'sklearn', 'imgaug']
        
        print("reconhecimento_facial.py:")
        for imp in expected_imports:
            found = any(imp in i for i in imports)
            status = "✓" if found else "✗"
            print(f"  {status} {imp}")
    
    print()
    print("5. Verificando integração com app.py...")
    print("-" * 60)
    
    app_path = os.path.join(base_dir, "app.py")
    if os.path.exists(app_path):
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        checks = {
            "Import registro_presenca": "registro_presenca" in app_content,
            "Import frequencia_aula": "frequencia_aula" in app_content,
            "Menu 'Registro de Presença'": "Registro de Presença" in app_content,
            "Menu 'Frequência de Aula'": "Frequência de Aula" in app_content,
            "Route registro_presenca": "render_registro_presenca" in app_content,
            "Route frequencia_aula": "render_frequencia_aula" in app_content,
        }
        
        for check_name, check_result in checks.items():
            status = "✓ OK" if check_result else "✗ FALTANDO"
            print(f"{check_name:45} {status}")
    
    print()
    print("6. Verificando data_manager.py...")
    print("-" * 60)
    
    dm_path = os.path.join(base_dir, "data_manager.py")
    if os.path.exists(dm_path):
        with open(dm_path, 'r', encoding='utf-8') as f:
            dm_content = f.read()
        
        checks = {
            "face_embeddings table": "face_embeddings" in dm_content,
            "attendance table": "attendance" in dm_content,
        }
        
        for check_name, check_result in checks.items():
            status = "✓ OK" if check_result else "✗ FALTANDO"
            print(f"{check_name:45} {status}")
    
    print()
    print("=" * 60)
    if all_valid:
        print("✓ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("Estrutura do código está correta.")
    else:
        print("✗ VALIDAÇÃO FALHOU")
        print("Verifique os erros acima.")
    print("=" * 60)
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
