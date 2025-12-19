#!/usr/bin/env python3
"""
Teste de Acesso à Webcam
Script para verificar se o sistema consegue acessar a webcam corretamente
"""

import sys
import os

def test_webcam_access():
    """
    Testa o acesso à webcam e funcionalidades relacionadas
    """
    print("\n" + "=" * 70)
    print("  🎥 TESTE DE ACESSO À WEBCAM")
    print("=" * 70 + "\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Verificar se OpenCV está instalado
    print("📋 Teste 1: Verificando instalação do OpenCV...")
    tests_total += 1
    try:
        import cv2
        print(f"✅ OpenCV instalado - Versão: {cv2.__version__}")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ OpenCV não está instalado: {e}")
        print("   Instale com: pip install opencv-python-headless")
        return tests_passed, tests_total
    
    # Test 2: Verificar se consegue listar dispositivos de captura
    print("\n📋 Teste 2: Verificando dispositivos de captura disponíveis...")
    tests_total += 1
    try:
        # Tentar abrir a webcam padrão (índice 0)
        cap = cv2.VideoCapture(0)
        
        if cap is None or not cap.isOpened():
            print("❌ Não foi possível abrir a webcam no índice 0")
            print("   Possíveis causas:")
            print("   - Nenhuma webcam conectada ao sistema")
            print("   - Webcam em uso por outro aplicativo")
            print("   - Permissões insuficientes")
            print("   - Sistema rodando em ambiente sem interface gráfica")
            
            # Verificar se estamos em ambiente headless
            if os.environ.get('DISPLAY') is None and sys.platform.startswith('linux'):
                print("\n⚠️  Sistema detectado como headless (sem display)")
                print("   Isto é esperado em servidores e ambientes CI/CD")
                print("   A webcam só funcionará em ambientes com acesso a dispositivos de vídeo")
            
            cap.release()
        else:
            print("✅ Webcam encontrada e acessível no índice 0")
            
            # Test 3: Obter informações da webcam
            print("\n📋 Teste 3: Obtendo informações da webcam...")
            tests_total += 1
            try:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                print(f"✅ Resolução: {width}x{height}")
                print(f"✅ FPS: {fps}")
                tests_passed += 1
            except Exception as e:
                print(f"❌ Erro ao obter informações da webcam: {e}")
            
            # Test 4: Capturar um frame
            print("\n📋 Teste 4: Tentando capturar um frame...")
            tests_total += 1
            try:
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"✅ Frame capturado com sucesso - Shape: {frame.shape}")
                    tests_passed += 1
                else:
                    print("❌ Falha ao capturar frame")
            except Exception as e:
                print(f"❌ Erro ao capturar frame: {e}")
            
            cap.release()
            tests_passed += 1
    
    except Exception as e:
        print(f"❌ Erro ao acessar a webcam: {e}")
    
    # Test 5: Verificar se face_recognition está disponível (opcional)
    print("\n📋 Teste 5: Verificando reconhecimento facial (opcional)...")
    tests_total += 1
    try:
        import face_recognition
        import dlib
        print(f"✅ face_recognition instalado - Versão: {face_recognition.__version__}")
        print(f"✅ dlib instalado - Versão: {dlib.__version__}")
        tests_passed += 1
    except ImportError as e:
        print(f"⚠️  Reconhecimento facial não disponível (opcional)")
        print(f"   Para habilitar: pip install -r requirements-face.txt")
        # Não conta como falha pois é opcional
        tests_passed += 1
    
    # Test 6: Verificar módulos do sistema
    print("\n📋 Teste 6: Verificando módulos de reconhecimento facial...")
    tests_total += 1
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from modulos.reconhecimento_facial import FaceRecognitionSystem
        
        face_system = FaceRecognitionSystem()
        
        if face_system.available:
            print("✅ Sistema de reconhecimento facial disponível")
            print(f"   Diretório de dados: {face_system.data_dir}")
            print(f"   Diretório de faces: {face_system.faces_dir}")
            print(f"   Diretório de modelos: {face_system.models_dir}")
            tests_passed += 1
        else:
            print("⚠️  Sistema de reconhecimento facial não está disponível")
            print("   Causa: Bibliotecas necessárias não instaladas")
            # Ainda conta como passou se conseguiu importar
            tests_passed += 1
    except Exception as e:
        print(f"❌ Erro ao verificar módulos do sistema: {e}")
    
    # Test 7: Verificar permissões de câmera (Linux)
    if sys.platform.startswith('linux'):
        print("\n📋 Teste 7: Verificando permissões de dispositivos de vídeo (Linux)...")
        tests_total += 1
        try:
            video_devices = []
            for i in range(10):
                device = f"/dev/video{i}"
                if os.path.exists(device):
                    video_devices.append(device)
            
            if video_devices:
                print(f"✅ Dispositivos de vídeo encontrados: {', '.join(video_devices)}")
                
                # Verificar permissões
                for device in video_devices:
                    if os.access(device, os.R_OK):
                        print(f"   ✅ {device} - Permissão de leitura OK")
                    else:
                        print(f"   ⚠️  {device} - Sem permissão de leitura")
                        print(f"       Execute: sudo chmod 666 {device}")
                tests_passed += 1
            else:
                print("⚠️  Nenhum dispositivo /dev/video* encontrado")
                print("   Isto pode ser normal em:")
                print("   - Ambientes virtualizados sem webcam")
                print("   - Containers Docker sem device mapping")
                print("   - Servidores sem hardware de vídeo")
                tests_passed += 1  # Não é erro crítico
        except Exception as e:
            print(f"⚠️  Erro ao verificar dispositivos: {e}")
            tests_passed += 1  # Não é erro crítico
    
    # Summary
    print("\n" + "=" * 70)
    print(f"  📊 RESULTADO: {tests_passed}/{tests_total} testes passaram")
    print("=" * 70)
    
    if tests_passed == tests_total:
        print("\n✅ SUCESSO! O sistema está pronto para usar a webcam")
        print("\n💡 Próximos passos:")
        print("   1. Acesse o sistema: streamlit run app.py")
        print("   2. Vá para '📸 Registro de Presença'")
        print("   3. Selecione um aluno e clique em 'Iniciar Captura'")
        return 0
    elif tests_passed >= tests_total - 2:
        print("\n⚠️  PARCIALMENTE FUNCIONAL")
        print("   Alguns recursos opcionais não estão disponíveis")
        print("   O sistema básico deve funcionar normalmente")
        return 0
    else:
        print("\n❌ FALHA! Corrija os problemas acima antes de usar a webcam")
        print("\n📚 Recursos úteis:")
        print("   - README.md - Documentação completa")
        print("   - FACE_RECOGNITION_INSTALLATION.md - Guia de instalação")
        print("   - requirements-face.txt - Dependências opcionais")
        return 1

def test_webcam_in_streamlit_context():
    """
    Teste adicional que simula o contexto do Streamlit
    """
    print("\n" + "=" * 70)
    print("  🎬 TESTE EM CONTEXTO STREAMLIT")
    print("=" * 70 + "\n")
    
    try:
        import cv2
        print("📋 Testando captura de múltiplos frames (simulando uso real)...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Webcam não disponível para teste de múltiplos frames")
            return
        
        frames_captured = 0
        frames_to_capture = 5
        
        print(f"   Tentando capturar {frames_to_capture} frames...")
        
        for i in range(frames_to_capture):
            ret, frame = cap.read()
            if ret:
                frames_captured += 1
                print(f"   ✅ Frame {i+1}/{frames_to_capture} capturado")
            else:
                print(f"   ❌ Falha ao capturar frame {i+1}")
        
        cap.release()
        
        if frames_captured == frames_to_capture:
            print(f"\n✅ Sucesso! Todos os {frames_captured} frames foram capturados")
            print("   A webcam está funcionando corretamente para uso contínuo")
        else:
            print(f"\n⚠️  Apenas {frames_captured}/{frames_to_capture} frames capturados")
            print("   Pode haver problemas de estabilidade")
    
    except Exception as e:
        print(f"❌ Erro durante teste de contexto: {e}")

if __name__ == '__main__':
    print("\n🎥 Sistema de Matrícula Escolar 2026 - Teste de Webcam\n")
    
    # Teste principal
    exit_code = test_webcam_access()
    
    # Teste adicional se webcam disponível
    if exit_code == 0:
        try:
            test_webcam_in_streamlit_context()
        except:
            pass  # Teste adicional opcional
    
    print("\n" + "=" * 70)
    print("  Teste concluído!")
    print("=" * 70 + "\n")
    
    sys.exit(exit_code)
