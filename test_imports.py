#!/usr/bin/env python3
"""
Script de validação para testar importações do sistema
Verifica se o sistema pode ser iniciado sem face_recognition
"""
import sys
import os

def test_basic_imports():
    """Testa importações básicas"""
    print("=" * 60)
    print("Testando importações básicas...")
    print("=" * 60)
    
    modules = [
        'streamlit',
        'pandas',
        'reportlab',
        'PIL',
        'plotly',
        'cv2',
        'numpy',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module} importado com sucesso")
        except ImportError as e:
            print(f"✗ {module} falhou: {e}")
            failed.append(module)
    
    return failed

def test_optional_imports():
    """Testa importações opcionais"""
    print("\n" + "=" * 60)
    print("Testando importações opcionais...")
    print("=" * 60)
    
    optional_modules = {
        'face_recognition': 'Reconhecimento facial',
        'dlib': 'Biblioteca dlib para reconhecimento facial',
        'tensorflow': 'TensorFlow para anti-spoofing',
        'imgaug': 'Data augmentation',
        'sklearn': 'Scikit-learn para machine learning',
    }
    
    available = {}
    for module, description in optional_modules.items():
        try:
            __import__(module)
            print(f"✓ {module} disponível - {description}")
            available[module] = True
        except ImportError:
            print(f"⚠ {module} não disponível - {description}")
            available[module] = False
    
    return available

def test_module_imports():
    """Testa importações dos módulos do sistema"""
    print("\n" + "=" * 60)
    print("Testando módulos do sistema...")
    print("=" * 60)
    
    # Adicionar o diretório atual ao path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    modules = [
        'data_manager',
        'modulos.reconhecimento_facial',
        'modulos.registro_presenca',
        'modulos.frequencia_aula',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module} importado com sucesso")
        except ImportError as e:
            print(f"✗ {module} falhou: {e}")
            failed.append(module)
        except Exception as e:
            print(f"⚠ {module} importado mas com erro: {e}")
    
    return failed

def main():
    """Executa todos os testes"""
    print("\n🔍 Iniciando validação do sistema...\n")
    
    # Testa importações básicas
    basic_failed = test_basic_imports()
    
    # Testa importações opcionais
    optional_available = test_optional_imports()
    
    # Testa módulos do sistema
    module_failed = test_module_imports()
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    
    if basic_failed:
        print(f"\n❌ Falhas críticas: {len(basic_failed)} módulos básicos falharam")
        print(f"   Módulos: {', '.join(basic_failed)}")
        print("   AÇÃO: Instale os módulos básicos com: pip install -r requirements.txt")
        return 1
    else:
        print("\n✅ Todas as importações básicas foram bem-sucedidas!")
    
    if not optional_available.get('face_recognition', False):
        print("\n⚠️  Reconhecimento facial não disponível")
        print("   O sistema funcionará sem esta funcionalidade")
        print("   ")
        print("   📖 Para habilitar o reconhecimento facial, veja o guia completo:")
        print("      FACE_RECOGNITION_INSTALLATION.md")
        print("   ")
        print("   Resumo rápido:")
        print("   1. Instale as dependências do sistema:")
        print("      - Ubuntu/Debian:")
        print("        sudo apt-get install build-essential cmake libopenblas-dev \\")
        print("                             liblapack-dev libx11-dev libgtk-3-dev \\")
        print("                             libatlas-base-dev gfortran")
        print("      - macOS: brew install cmake")
        print("      - Windows: Use Anaconda e instale via 'conda install -c conda-forge dlib'")
        print("   2. Reinstale as dependências Python:")
        print("      pip install --force-reinstall -r requirements.txt")
    else:
        print("\n✅ Reconhecimento facial disponível!")
        print("   Funcionalidades habilitadas:")
        print("   - 📸 Registro de Presença (cadastro facial)")
        print("   - ✅ Frequência de Aula (marcação automática)")
        print("   - 🔐 Anti-spoofing (detecção de fotos falsas)")
    
    if module_failed:
        print(f"\n⚠️  {len(module_failed)} módulos do sistema falharam")
        print(f"   Módulos: {', '.join(module_failed)}")
        return 1
    else:
        print("\n✅ Todos os módulos do sistema foram importados com sucesso!")
    
    print("\n" + "=" * 60)
    print("✅ Sistema pronto para uso!")
    print("   Execute: streamlit run app.py")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
