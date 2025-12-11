"""
Módulo de Reconhecimento Facial com Anti-Spoofing
Implementa captura de sequência de fotos, treinamento de modelo e detecção de faces
"""
import numpy as np
import os
import pickle
import json
import time
from datetime import datetime
from PIL import Image

# Tentar importar cv2 (opencv)
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Tentar importar face_recognition e bibliotecas opcionais
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

try:
    import imgaug.augmenters as iaa
    IMGAUG_AVAILABLE = True
except ImportError:
    IMGAUG_AVAILABLE = False

# TensorFlow and scikit-learn for anti-spoofing
TENSORFLOW_AVAILABLE = False
SKLEARN_AVAILABLE = False
try:
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    pass

try:
    from tensorflow import keras
    from tensorflow.keras import layers, callbacks
    from tensorflow.keras.models import Sequential, load_model
    TENSORFLOW_AVAILABLE = True
except ImportError:
    pass

# Import streamlit after optional imports to avoid import-time warnings
import streamlit as st

class FaceRecognitionSystem:
    """Sistema de reconhecimento facial com anti-spoofing"""
    
    # Constantes de qualidade de imagem
    MIN_SHARPNESS = 50
    IDEAL_BRIGHTNESS = 128
    MIN_FACE_SIZE_RATIO = 0.2
    MAX_FACE_SIZE_RATIO = 0.4
    
    # Pesos para score de qualidade
    SHARPNESS_WEIGHT = 0.35
    BRIGHTNESS_WEIGHT = 0.25
    FACE_SIZE_WEIGHT = 0.40
    
    # Limites de validação de treinamento
    EXCELLENT_DISTANCE = 0.4
    GOOD_DISTANCE = 0.6
    ACCEPTABLE_DISTANCE = 0.7
    
    # Thresholds adaptativos de reconhecimento
    THRESHOLD_DEFAULT = 0.50
    THRESHOLD_RELAXED = 0.55
    THRESHOLD_STRICT = 0.45
    THRESHOLD_DIFF_MIN = 0.1  # Diferença mínima entre 1º e 2º para usar threshold relaxado
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.faces_dir = os.path.join(data_dir, 'faces')
        self.models_dir = os.path.join(data_dir, 'models')
        # Sistema está disponível apenas se todas as dependências estão instaladas
        self.available = FACE_RECOGNITION_AVAILABLE and CV2_AVAILABLE
        
        # Criar diretórios se não existirem
        os.makedirs(self.faces_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Caminhos dos modelos
        self.embeddings_path = os.path.join(self.models_dir, 'face_embeddings.pkl')
        self.liveness_model_path = os.path.join(self.models_dir, 'liveness_model.h5')
        
        # Carregar embeddings se existirem
        self.known_face_encodings = []
        self.known_face_ids = []
        if self.available:
            self.load_embeddings()
        
        # Carregar modelo de liveness se existir
        self.liveness_model = None
        if TENSORFLOW_AVAILABLE and os.path.exists(self.liveness_model_path):
            try:
                self.liveness_model = load_model(self.liveness_model_path)
            except (OSError, ValueError) as e:
                # Log error but continue without liveness model
                self.liveness_model = None
    
    def assess_image_quality(self, frame):
        """
        Avalia a qualidade de uma imagem para reconhecimento facial
        
        Args:
            frame: Frame capturado (numpy array)
        
        Returns:
            dict: Métricas de qualidade (score, brightness, sharpness, has_face)
        """
        if not CV2_AVAILABLE:
            return {'score': 0, 'brightness': 0, 'sharpness': 0, 'has_face': False}
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Avaliar nitidez (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 100.0, 1.0)  # Normalizar para 0-1
        
        # 2. Avaliar brilho (média de intensidade)
        brightness = gray.mean()
        brightness_score = 1.0 - abs(brightness - self.IDEAL_BRIGHTNESS) / self.IDEAL_BRIGHTNESS
        
        # 3. Detectar face
        has_face = False
        face_size_score = 0.0
        face_locations = None
        
        if self.available:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model='hog')
            
            if len(face_locations) > 0:
                has_face = True
                # Avaliar tamanho da face (face maior = melhor)
                top, right, bottom, left = face_locations[0]
                face_height = bottom - top
                frame_height, frame_width = frame.shape[:2]
                
                # Face ideal ocupa MIN_FACE_SIZE_RATIO-MAX_FACE_SIZE_RATIO da altura do frame
                face_ratio = face_height / frame_height
                if self.MIN_FACE_SIZE_RATIO <= face_ratio <= self.MAX_FACE_SIZE_RATIO:
                    face_size_score = 1.0
                elif face_ratio < self.MIN_FACE_SIZE_RATIO:
                    face_size_score = face_ratio / self.MIN_FACE_SIZE_RATIO
                else:
                    face_size_score = self.MAX_FACE_SIZE_RATIO / face_ratio
        
        # Calcular score geral (ponderado)
        if not has_face:
            overall_score = 0.0
        else:
            overall_score = (
                sharpness_score * self.SHARPNESS_WEIGHT +
                brightness_score * self.BRIGHTNESS_WEIGHT +
                face_size_score * self.FACE_SIZE_WEIGHT
            )
        
        return {
            'score': overall_score,
            'brightness': brightness,
            'sharpness': laplacian_var,
            'has_face': has_face,
            'face_size_score': face_size_score
        }
    
    def capture_photo_sequence(self, aluno_id, num_photos=30, duration=10, quality_threshold=0.5):
        """
        Captura uma sequência de fotos usando a webcam com validação de qualidade
        
        Args:
            aluno_id: ID do aluno
            num_photos: Número de fotos a capturar (padrão: 30)
            duration: Duração em segundos (padrão: 10)
            quality_threshold: Limiar mínimo de qualidade (padrão: 0.5)
        
        Returns:
            list: Lista de caminhos das fotos salvas
        """
        if not CV2_AVAILABLE:
            st.error("❌ OpenCV (cv2) não está disponível. Instale opencv-python ou opencv-python-headless.")
            return []
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Não foi possível acessar a webcam")
            return []
        
        # Criar diretório para o aluno
        aluno_dir = os.path.join(self.faces_dir, f'aluno_{aluno_id}')
        os.makedirs(aluno_dir, exist_ok=True)
        
        photos_saved = []
        quality_scores = []
        interval = duration / num_photos  # Intervalo entre fotos
        
        st.info(f"""
        🎥 **Captura Inteligente de Fotos**
        - Alvo: {num_photos} fotos de alta qualidade
        - Duração: {duration} segundos
        - Qualidade mínima: {quality_threshold*100:.0f}%
        
        💡 **Dicas para melhor qualidade:**
        - Mantenha o rosto centralizado
        - Iluminação uniforme no rosto
        - Evite movimentos bruscos
        """)
        
        progress_bar = st.progress(0)
        placeholder = st.empty()
        quality_placeholder = st.empty()
        
        start_time = datetime.now()
        photo_count = 0
        attempts = 0
        max_attempts = min(num_photos * 3, 150)  # Limitar para evitar loops infinitos
        
        while photo_count < num_photos and attempts < max_attempts:
            ret, frame = cap.read()
            if not ret:
                break
            
            attempts += 1
            elapsed = (datetime.now() - start_time).total_seconds()
            
            # Avaliar qualidade do frame atual
            quality = self.assess_image_quality(frame)
            
            # Mostrar feedback em tempo real
            frame_display = frame.copy()
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            
            # Adicionar indicadores visuais
            if quality['has_face']:
                color = (0, 255, 0) if quality['score'] >= quality_threshold else (255, 165, 0)
                cv2.putText(frame_display, f"Qualidade: {quality['score']:.2f}", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
                # Detectar e desenhar retângulo na face
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame, model='hog')
                if len(face_locations) > 0:
                    top, right, bottom, left = face_locations[0]
                    cv2.rectangle(frame_display, (left, top), (right, bottom), color, 2)
            else:
                cv2.putText(frame_display, "Nenhuma face detectada", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            
            # Capturar foto se qualidade for boa e tempo adequado
            if (elapsed >= photo_count * interval and 
                quality['score'] >= quality_threshold and 
                quality['has_face']):
                
                # Salvar foto
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                photo_path = os.path.join(aluno_dir, f'photo_{timestamp}.jpg')
                cv2.imwrite(photo_path, frame)
                photos_saved.append(photo_path)
                quality_scores.append(quality['score'])
                photo_count += 1
                
                # Atualizar progresso
                progress_bar.progress(photo_count / num_photos)
                
                # Mostrar frame capturado com indicador de sucesso
                cv2.putText(frame_display, "CAPTURADA!", 
                          (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            
            # Atualizar visualização
            placeholder.image(frame_rgb, caption=f'Foto {photo_count}/{num_photos} | Qualidade: {quality["score"]:.2%}', 
                            use_column_width=True)
            
            # Mostrar métricas de qualidade
            quality_placeholder.info(f"""
            📊 **Métricas em Tempo Real:**
            - Face detectada: {'✅ Sim' if quality['has_face'] else '❌ Não'}
            - Brilho: {quality['brightness']:.0f}/255 (ideal: ~128)
            - Nitidez: {quality['sharpness']:.0f} (mínimo: ~50)
            - Score geral: {quality['score']:.2%}
            """)
            
            if elapsed >= duration:
                break
        
        cap.release()
        progress_bar.empty()
        placeholder.empty()
        quality_placeholder.empty()
        
        # Mostrar resumo da captura
        if len(photos_saved) > 0:
            avg_quality = sum(quality_scores) / len(quality_scores)
            st.success(f"""
            ✅ **Captura concluída com sucesso!**
            
            - Fotos capturadas: {len(photos_saved)}
            - Qualidade média: {avg_quality:.2%}
            - Qualidade mínima: {min(quality_scores):.2%}
            - Qualidade máxima: {max(quality_scores):.2%}
            """)
        else:
            st.error("❌ Nenhuma foto de qualidade suficiente foi capturada. Tente novamente com melhor iluminação.")
        
        return photos_saved
    
    def augment_images(self, image_paths):
        """
        Aplica data augmentation nas imagens
        
        Args:
            image_paths: Lista de caminhos das imagens
        
        Returns:
            list: Lista de imagens aumentadas (numpy arrays)
        """
        if not CV2_AVAILABLE:
            # Sem cv2, não podemos processar imagens
            return []
        
        if not IMGAUG_AVAILABLE:
            # Sem augmentation, retornar apenas as imagens originais
            images = []
            for img_path in image_paths:
                image = cv2.imread(img_path)
                if image is not None:
                    images.append(image)
            return images
        
        # Definir augmentations
        seq = iaa.Sequential([
            iaa.Fliplr(0.5),  # Flip horizontal em 50% das imagens
            iaa.Affine(
                rotate=(-10, 10),  # Rotação de -10 a 10 graus
                scale=(0.9, 1.1),  # Escala de 90% a 110%
            ),
            iaa.Multiply((0.8, 1.2)),  # Mudar brilho
            iaa.GaussianBlur(sigma=(0, 0.5)),  # Blur gaussiano leve
        ])
        
        augmented_images = []
        for img_path in image_paths:
            # Carregar imagem
            image = cv2.imread(img_path)
            if image is None:
                continue
            
            # Imagem original
            augmented_images.append(image)
            
            # Aplicar augmentations (2 variações por imagem)
            for _ in range(2):
                aug_image = seq(image=image)
                augmented_images.append(aug_image)
        
        return augmented_images
    
    def extract_face_encodings(self, image_paths, aluno_id):
        """
        Extrai encodings das faces das imagens
        
        Args:
            image_paths: Lista de caminhos das imagens
            aluno_id: ID do aluno
        
        Returns:
            list: Lista de encodings extraídos
        """
        if not self.available:
            st.error("❌ Reconhecimento facial não está disponível. Instale face_recognition e dlib.")
            return []
        
        encodings = []
        
        # Aplicar augmentation
        augmented_images = self.augment_images(image_paths)
        
        progress_bar = st.progress(0)
        st.info(f"Processando {len(augmented_images)} imagens (incluindo augmentation)...")
        
        for idx, image in enumerate(augmented_images):
            # Converter para RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detectar faces
            face_locations = face_recognition.face_locations(rgb_image, model='hog')
            
            if len(face_locations) > 0:
                # Extrair encoding da primeira face detectada
                face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
                if len(face_encodings) > 0:
                    encodings.append(face_encodings[0])
            
            progress_bar.progress((idx + 1) / len(augmented_images))
        
        progress_bar.empty()
        st.success(f"✅ {len(encodings)} encodings extraídos com sucesso!")
        
        return encodings
    
    def validate_training_quality(self, encodings, aluno_id):
        """
        Valida a qualidade do treinamento verificando consistência dos encodings
        
        Args:
            encodings: Lista de encodings para validar
            aluno_id: ID do aluno
        
        Returns:
            dict: Métricas de qualidade (consistency_score, avg_distance, is_valid)
        """
        if len(encodings) < 2:
            return {
                'consistency_score': 0.0,
                'avg_distance': 0.0,
                'is_valid': len(encodings) > 0
            }
        
        # Otimização: Para muitos encodings, amostrar para evitar O(n²)
        max_sample_size = 50
        if len(encodings) > max_sample_size:
            import random
            sample_indices = random.sample(range(len(encodings)), max_sample_size)
            sampled_encodings = [encodings[i] for i in sample_indices]
        else:
            sampled_encodings = encodings
        
        # Calcular distância média entre todos os pares de encodings
        distances = []
        for i in range(len(sampled_encodings)):
            # Calcular distâncias vetorizadas para este encoding
            other_encodings = sampled_encodings[i+1:]
            if other_encodings:
                dists = face_recognition.face_distance(other_encodings, sampled_encodings[i])
                distances.extend(dists)
        
        avg_distance = sum(distances) / len(distances) if distances else 0.0
        
        # Score de consistência (menor distância = maior consistência)
        consistency_score = 1.0 - min(avg_distance / self.GOOD_DISTANCE, 1.0)
        
        # Considerar válido se consistência for razoável
        is_valid = avg_distance < self.ACCEPTABLE_DISTANCE
        
        return {
            'consistency_score': consistency_score,
            'avg_distance': avg_distance,
            'is_valid': is_valid,
            'num_encodings': len(encodings)
        }
    
    def train_face_recognition(self, aluno_id, image_paths):
        """
        Treina o modelo de reconhecimento facial com as imagens do aluno
        Inclui validação de qualidade e métricas detalhadas
        
        Args:
            aluno_id: ID do aluno
            image_paths: Lista de caminhos das imagens
        
        Returns:
            bool: True se treinamento foi bem sucedido
        """
        if not self.available:
            st.error("❌ Reconhecimento facial não está disponível. Instale face_recognition e dlib.")
            return False
        
        # Extrair encodings
        encodings = self.extract_face_encodings(image_paths, aluno_id)
        
        if len(encodings) == 0:
            st.error("❌ Nenhuma face detectada nas imagens!")
            return False
        
        # Validar qualidade do treinamento
        st.info("🔍 Validando qualidade do treinamento...")
        validation = self.validate_training_quality(encodings, aluno_id)
        
        if not validation['is_valid']:
            st.warning(f"""
            ⚠️ **Qualidade do treinamento abaixo do ideal**
            
            A consistência entre as imagens está baixa. Isso pode ocorrer se:
            - A iluminação variou muito durante a captura
            - Houve muitos movimentos ou mudanças de expressão
            - A qualidade das imagens foi inconsistente
            
            **Recomendação:** Considere recapturar as fotos com:
            - Iluminação mais uniforme
            - Menos movimentos bruscos
            - Posição mais centralizada
            
            O sistema ainda funcionará, mas pode ter precisão reduzida.
            """)
        
        # Adicionar aos encodings conhecidos
        self.known_face_encodings.extend(encodings)
        self.known_face_ids.extend([aluno_id] * len(encodings))
        
        # Salvar embeddings
        self.save_embeddings()
        
        # Mostrar métricas detalhadas
        quality_label = (
            '⭐ Excelente' if validation['avg_distance'] < self.EXCELLENT_DISTANCE 
            else '✅ Boa' if validation['avg_distance'] < self.GOOD_DISTANCE 
            else '⚠️ Aceitável'
        )
        
        st.success(f"""
        ✅ **Treinamento concluído com sucesso!**
        
        📊 **Métricas do Modelo:**
        - Encodings gerados: {len(encodings)}
        - Consistência: {validation['consistency_score']:.2%}
        - Distância média interna: {validation['avg_distance']:.3f}
        - Qualidade: {quality_label}
        
        💡 **Interpretação:**
        - Distância < {self.EXCELLENT_DISTANCE}: Excelente qualidade
        - Distância {self.EXCELLENT_DISTANCE}-{self.GOOD_DISTANCE}: Boa qualidade (recomendado)
        - Distância {self.GOOD_DISTANCE}-{self.ACCEPTABLE_DISTANCE}: Aceitável
        - Distância > {self.ACCEPTABLE_DISTANCE}: Considere retreinar
        """)
        
        return True
    
    def save_embeddings(self):
        """Salva os embeddings em arquivo"""
        data = {
            'encodings': self.known_face_encodings,
            'ids': self.known_face_ids
        }
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump(data, f)
    
    def load_embeddings(self):
        """Carrega os embeddings do arquivo"""
        if os.path.exists(self.embeddings_path):
            try:
                with open(self.embeddings_path, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_ids = data['ids']
            except (EOFError, pickle.UnpicklingError, KeyError) as e:
                # If embeddings file is corrupted, start fresh
                self.known_face_encodings = []
                self.known_face_ids = []
    
    def recognize_face(self, frame, return_rankings=False, adaptive_threshold=True):
        """
        Reconhece faces em um frame com ranking de candidatos
        
        Args:
            frame: Frame capturado da webcam (numpy array)
            return_rankings: Se True, retorna top 3 candidatos
            adaptive_threshold: Se True, usa threshold adaptativo
        
        Returns:
            Se return_rankings=False: tuple (aluno_id, confidence, face_location) ou (None, 0, None)
            Se return_rankings=True: tuple (aluno_id, confidence, face_location, rankings)
        """
        if not self.available:
            return (None, 0, None, []) if return_rankings else (None, 0, None)
        
        if len(self.known_face_encodings) == 0:
            return (None, 0, None, []) if return_rankings else (None, 0, None)
        
        # Converter para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar faces
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        
        if len(face_locations) == 0:
            return (None, 0, None, []) if return_rankings else (None, 0, None)
        
        # Extrair encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Calcular distâncias para todas as faces conhecidas
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            if len(face_distances) == 0:
                return (None, 0, None, []) if return_rankings else (None, 0, None)
            
            # Agrupar por aluno_id e calcular distância média
            aluno_distances = {}
            for idx, (aluno_id, distance) in enumerate(zip(self.known_face_ids, face_distances)):
                if aluno_id not in aluno_distances:
                    aluno_distances[aluno_id] = []
                aluno_distances[aluno_id].append(distance)
            
            # Calcular média de distâncias por aluno
            aluno_avg_distances = {
                aluno_id: sum(distances) / len(distances)
                for aluno_id, distances in aluno_distances.items()
            }
            
            # Ordenar por menor distância
            sorted_alunos = sorted(aluno_avg_distances.items(), key=lambda x: x[1])
            
            # Determinar threshold
            if adaptive_threshold and len(sorted_alunos) > 0:
                # Threshold adaptativo: se há diferença significativa entre primeiro e segundo
                best_distance = sorted_alunos[0][1]
                if len(sorted_alunos) > 1:
                    second_distance = sorted_alunos[1][1]
                    # Se a diferença é grande, podemos ser mais confiantes
                    if (second_distance - best_distance) > self.THRESHOLD_DIFF_MIN:
                        threshold = self.THRESHOLD_RELAXED
                    else:
                        threshold = self.THRESHOLD_STRICT
                else:
                    threshold = self.THRESHOLD_DEFAULT
            else:
                threshold = self.THRESHOLD_DEFAULT
            
            # Verificar se melhor match está dentro do threshold
            if len(sorted_alunos) > 0:
                best_aluno_id, best_distance = sorted_alunos[0]
                
                if best_distance < threshold:
                    confidence = 1 - best_distance
                    
                    if return_rankings:
                        # Preparar rankings dos top 3
                        rankings = [
                            {
                                'aluno_id': aluno_id,
                                'distance': distance,
                                'confidence': 1 - distance,
                                'num_samples': len(aluno_distances[aluno_id])
                            }
                            for aluno_id, distance in sorted_alunos[:3]
                        ]
                        return best_aluno_id, confidence, face_location, rankings
                    else:
                        return best_aluno_id, confidence, face_location
        
        return (None, 0, None, []) if return_rankings else (None, 0, None)
    
    def train_liveness_model(self, real_images, fake_images=None, epochs=10):
        """
        Treina modelo de detecção de liveness (anti-spoofing)
        
        Args:
            real_images: Lista de imagens reais
            fake_images: Lista de imagens falsas (fotos de fotos)
            epochs: Número de épocas para treinamento
        
        Returns:
            bool: True se treinamento foi bem sucedido
        """
        if not CV2_AVAILABLE:
            st.warning("OpenCV não está disponível. Anti-spoofing desabilitado.")
            return False
        
        if not TENSORFLOW_AVAILABLE or not SKLEARN_AVAILABLE:
            st.warning("TensorFlow ou scikit-learn não está disponível. Anti-spoofing desabilitado.")
            return False
        
        if fake_images is None or len(fake_images) == 0:
            st.warning("Sem imagens falsas para treinar anti-spoofing. Usando detecção básica.")
            return False
        
        # Preparar dados
        X_real = []
        X_fake = []
        
        # Processar imagens reais
        for img in real_images:
            if isinstance(img, str):
                img = cv2.imread(img)
            img = cv2.resize(img, (64, 64))
            img = img / 255.0
            X_real.append(img)
        
        # Processar imagens falsas
        for img in fake_images:
            if isinstance(img, str):
                img = cv2.imread(img)
            img = cv2.resize(img, (64, 64))
            img = img / 255.0
            X_fake.append(img)
        
        # Combinar dados
        X = np.array(X_real + X_fake)
        y = np.array([1] * len(X_real) + [0] * len(X_fake))
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Criar modelo CNN simples
        model = Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam',
                     loss='binary_crossentropy',
                     metrics=['accuracy'])
        
        # Early stopping
        early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        
        # Treinar
        st.info("Treinando modelo de anti-spoofing...")
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=[early_stop],
            verbose=0
        )
        
        # Salvar modelo
        model.save(self.liveness_model_path)
        self.liveness_model = model
        
        # Avaliar
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
        st.success(f"✅ Modelo de anti-spoofing treinado! Acurácia: {test_acc:.2%}")
        
        return True
    
    def detect_liveness(self, frame):
        """
        Detecta se a face é real ou fake (foto)
        
        Args:
            frame: Frame capturado da webcam
        
        Returns:
            tuple: (is_real, confidence)
        """
        if not CV2_AVAILABLE or self.liveness_model is None:
            # Detecção básica sem modelo: sempre retorna True
            # NOTA DE SEGURANÇA: Quando o modelo de liveness não está disponível,
            # o sistema permite acesso (retorna True) para manter funcionalidade básica.
            # Isto significa que anti-spoofing está DESABILITADO neste caso.
            # A confiança baixa (0.5) indica que a detecção não foi realizada.
            # O sistema ainda pode usar reconhecimento facial, mas sem proteção contra fotos.
            return True, 0.5
        
        # Preparar frame
        img = cv2.resize(frame, (64, 64))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Predição
        prediction = self.liveness_model.predict(img, verbose=0)[0][0]
        
        # prediction > 0.5 = real, < 0.5 = fake
        is_real = prediction > 0.5
        confidence = prediction if is_real else 1 - prediction
        
        return is_real, float(confidence)
    
    def mark_attendance_with_webcam(self, data_manager, timeout=30, min_confidence=0.6, confirmation_frames=3):
        """
        Marca presença usando a webcam com detecção de face e confirmação múltipla
        
        Args:
            data_manager: Instância do DataManager
            timeout: Tempo máximo de espera em segundos
            min_confidence: Confiança mínima para reconhecimento (padrão: 0.6)
            confirmation_frames: Número de frames consecutivos para confirmar (padrão: 3)
        
        Returns:
            dict: Dados da presença registrada ou None
        """
        if not CV2_AVAILABLE:
            st.error("❌ OpenCV (cv2) não está disponível. Instale opencv-python ou opencv-python-headless.")
            return None
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Não foi possível acessar a webcam")
            return None
        
        st.info(f"""
        📸 **Sistema de Reconhecimento Inteligente**
        
        - Confiança mínima: {min_confidence:.0%}
        - Confirmações necessárias: {confirmation_frames} frames
        - Timeout: {timeout} segundos
        
        💡 Posicione seu rosto centralizado e aguarde...
        """)
        
        placeholder = st.empty()
        metrics_placeholder = st.empty()
        stop_button = st.button("⏹️ Parar")
        
        start_time = datetime.now()
        recognized = False
        attendance_data = None
        
        # Tracking de confirmações
        confirmation_buffer = []
        last_aluno_id = None
        consecutive_count = 0
        
        while not recognized and not stop_button:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Verificar timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout:
                st.warning("⏱️ Tempo esgotado!")
                break
            
            # Reconhecer face com rankings
            aluno_id, confidence, face_location, rankings = self.recognize_face(
                frame, 
                return_rankings=True,
                adaptive_threshold=True
            )
            
            # Processar reconhecimento
            frame_display = frame.copy()
            status_text = "Aguardando..."
            status_color = (200, 200, 200)
            
            if aluno_id is not None and confidence > min_confidence:
                # Rastreamento de confirmações
                if aluno_id == last_aluno_id:
                    consecutive_count += 1
                else:
                    consecutive_count = 1
                    last_aluno_id = aluno_id
                
                # Adicionar ao buffer de confirmação
                confirmation_buffer.append({
                    'aluno_id': aluno_id,
                    'confidence': confidence,
                    'timestamp': datetime.now()
                })
                
                # Manter apenas últimos N frames
                if len(confirmation_buffer) > confirmation_frames:
                    confirmation_buffer.pop(0)
                
                # Verificar se temos confirmações suficientes
                if consecutive_count >= confirmation_frames:
                    # Detectar liveness
                    is_real, liveness_conf = self.detect_liveness(frame)
                    
                    if is_real:
                        # Face reconhecida e confirmada!
                        recognized = True
                        
                        # Buscar dados do aluno
                        aluno = data_manager.get_record('cadastro', aluno_id)
                        
                        if aluno:
                            # Calcular confiança média das confirmações
                            avg_confidence = sum(c['confidence'] for c in confirmation_buffer) / len(confirmation_buffer)
                            
                            # Desenhar retângulo na face
                            top, right, bottom, left = face_location
                            cv2.rectangle(frame_display, (left, top), (right, bottom), (0, 255, 0), 3)
                            cv2.putText(frame_display, f"{aluno['nome_completo']}", (left, top - 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            cv2.putText(frame_display, f"Confianca: {avg_confidence:.2%}", (left, top - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            
                            # Registrar presença
                            now = datetime.now()
                            attendance_data = {
                                'aluno_id': aluno_id,
                                'data': now.strftime('%Y-%m-%d'),
                                'hora': now.strftime('%H:%M:%S'),
                                'tipo': 'entrada',
                                'verificado': 'Sim',
                                'confianca': f"{avg_confidence:.2%}",  # Mantém nome do campo para compatibilidade com banco
                                'observacoes': f"Liveness: {liveness_conf:.2%} | Confirmações: {confirmation_frames}",
                                'data_registro': now.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            # Salvar no banco
                            data_manager.add_record('attendance', attendance_data)
                            
                            status_text = f"✅ CONFIRMADO!"
                            status_color = (0, 255, 0)
                    else:
                        # Foto detectada!
                        top, right, bottom, left = face_location
                        cv2.rectangle(frame_display, (left, top), (right, bottom), (0, 0, 255), 3)
                        cv2.putText(frame_display, "FOTO DETECTADA!", (left, top - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        status_text = "⚠️ FOTO DETECTADA!"
                        status_color = (0, 0, 255)
                        consecutive_count = 0  # Reset
                else:
                    # Ainda confirmando
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame_display, (left, top), (right, bottom), (255, 165, 0), 2)
                    cv2.putText(frame_display, f"Confirmando... {consecutive_count}/{confirmation_frames}", 
                              (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)
                    status_text = f"🔄 Confirmando... {consecutive_count}/{confirmation_frames}"
                    status_color = (255, 165, 0)
            else:
                # Reset se não detectar face ou confiança baixa
                consecutive_count = 0
                last_aluno_id = None
                
                if face_location is not None:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame_display, (left, top), (right, bottom), (200, 200, 200), 2)
                    cv2.putText(frame_display, f"Baixa confiança: {confidence:.2%}", 
                              (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
            
            # Adicionar status no frame
            cv2.putText(frame_display, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            
            # Mostrar frame
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            placeholder.image(frame_rgb, caption=f'Tempo: {elapsed:.1f}s / {timeout}s', 
                            use_column_width=True)
            
            # Mostrar métricas em tempo real
            if rankings:
                ranking_text = "📊 **Top 3 Candidatos:**\n\n"
                for i, rank in enumerate(rankings, 1):
                    ranking_text += f"{i}. Aluno {rank['aluno_id']}: {rank['confidence']:.2%} (amostras: {rank['num_samples']})\n"
                metrics_placeholder.info(ranking_text)
            
            # Pequeno delay
            time.sleep(0.05)
        
        cap.release()
        placeholder.empty()
        metrics_placeholder.empty()
        
        # Mostrar resumo final
        if attendance_data:
            aluno = data_manager.get_record('cadastro', attendance_data['aluno_id'])
            st.success(f"""
            ✅ **Presença Registrada com Sucesso!**
            
            👤 **Aluno:** {aluno['nome_completo']}
            📅 **Data:** {attendance_data['data']}
            🕐 **Hora:** {attendance_data['hora']}
            📊 **Confiança:** {attendance_data['confianca']}
            🔒 **Verificação:** {attendance_data['observacoes']}
            """)
            st.balloons()
        
        return attendance_data
    
    def get_student_count(self):
        """Retorna o número de alunos registrados no sistema"""
        return len(set(self.known_face_ids))
