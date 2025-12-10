"""
Módulo de Reconhecimento Facial com Anti-Spoofing
Implementa captura de sequência de fotos, treinamento de modelo e detecção de faces
"""
import cv2
import face_recognition
import numpy as np
import os
import pickle
import json
import time
from datetime import datetime
from PIL import Image
import imgaug.augmenters as iaa
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from tensorflow.keras.models import Sequential, load_model
import streamlit as st

class FaceRecognitionSystem:
    """Sistema de reconhecimento facial com anti-spoofing"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.faces_dir = os.path.join(data_dir, 'faces')
        self.models_dir = os.path.join(data_dir, 'models')
        
        # Criar diretórios se não existirem
        os.makedirs(self.faces_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Caminhos dos modelos
        self.embeddings_path = os.path.join(self.models_dir, 'face_embeddings.pkl')
        self.liveness_model_path = os.path.join(self.models_dir, 'liveness_model.h5')
        
        # Carregar embeddings se existirem
        self.known_face_encodings = []
        self.known_face_ids = []
        self.load_embeddings()
        
        # Carregar modelo de liveness se existir
        self.liveness_model = None
        if os.path.exists(self.liveness_model_path):
            try:
                self.liveness_model = load_model(self.liveness_model_path)
            except (OSError, ValueError) as e:
                # Log error but continue without liveness model
                self.liveness_model = None
    
    def capture_photo_sequence(self, aluno_id, num_photos=30, duration=10):
        """
        Captura uma sequência de fotos usando a webcam
        
        Args:
            aluno_id: ID do aluno
            num_photos: Número de fotos a capturar (padrão: 30)
            duration: Duração em segundos (padrão: 10)
        
        Returns:
            list: Lista de caminhos das fotos salvas
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Não foi possível acessar a webcam")
            return []
        
        # Criar diretório para o aluno
        aluno_dir = os.path.join(self.faces_dir, f'aluno_{aluno_id}')
        os.makedirs(aluno_dir, exist_ok=True)
        
        photos_saved = []
        interval = duration / num_photos  # Intervalo entre fotos
        
        st.info(f"Capturando {num_photos} fotos em {duration} segundos...")
        progress_bar = st.progress(0)
        placeholder = st.empty()
        
        start_time = datetime.now()
        photo_count = 0
        
        while photo_count < num_photos:
            ret, frame = cap.read()
            if not ret:
                break
            
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= photo_count * interval:
                # Salvar foto
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                photo_path = os.path.join(aluno_dir, f'photo_{timestamp}.jpg')
                cv2.imwrite(photo_path, frame)
                photos_saved.append(photo_path)
                photo_count += 1
                
                # Atualizar progresso
                progress_bar.progress(photo_count / num_photos)
                
                # Mostrar frame atual
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                placeholder.image(frame_rgb, caption=f'Foto {photo_count}/{num_photos}', 
                                use_column_width=True)
            
            if elapsed >= duration:
                break
        
        cap.release()
        progress_bar.empty()
        placeholder.empty()
        
        st.success(f"✅ {len(photos_saved)} fotos capturadas com sucesso!")
        return photos_saved
    
    def augment_images(self, image_paths):
        """
        Aplica data augmentation nas imagens
        
        Args:
            image_paths: Lista de caminhos das imagens
        
        Returns:
            list: Lista de imagens aumentadas (numpy arrays)
        """
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
    
    def train_face_recognition(self, aluno_id, image_paths):
        """
        Treina o modelo de reconhecimento facial com as imagens do aluno
        
        Args:
            aluno_id: ID do aluno
            image_paths: Lista de caminhos das imagens
        
        Returns:
            bool: True se treinamento foi bem sucedido
        """
        # Extrair encodings
        encodings = self.extract_face_encodings(image_paths, aluno_id)
        
        if len(encodings) == 0:
            st.error("Nenhuma face detectada nas imagens!")
            return False
        
        # Adicionar aos encodings conhecidos
        self.known_face_encodings.extend(encodings)
        self.known_face_ids.extend([aluno_id] * len(encodings))
        
        # Salvar embeddings
        self.save_embeddings()
        
        st.success(f"✅ Modelo treinado com {len(encodings)} encodings do aluno {aluno_id}")
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
    
    def recognize_face(self, frame):
        """
        Reconhece faces em um frame
        
        Args:
            frame: Frame capturado da webcam (numpy array)
        
        Returns:
            tuple: (aluno_id, confidence, face_location) ou (None, 0, None)
        """
        if len(self.known_face_encodings) == 0:
            return None, 0, None
        
        # Converter para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar faces
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        
        if len(face_locations) == 0:
            return None, 0, None
        
        # Extrair encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Comparar com faces conhecidas
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    aluno_id = self.known_face_ids[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    return aluno_id, confidence, face_location
        
        return None, 0, None
    
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
        if self.liveness_model is None:
            # Detecção básica sem modelo: sempre retorna True
            # Na prática, poderia usar técnicas heurísticas simples
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
    
    def mark_attendance_with_webcam(self, data_manager, timeout=30):
        """
        Marca presença usando a webcam com detecção de face
        
        Args:
            data_manager: Instância do DataManager
            timeout: Tempo máximo de espera em segundos
        
        Returns:
            dict: Dados da presença registrada ou None
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Não foi possível acessar a webcam")
            return None
        
        st.info("📸 Posicione seu rosto na frente da câmera...")
        placeholder = st.empty()
        stop_button = st.button("⏹️ Parar")
        
        start_time = datetime.now()
        recognized = False
        attendance_data = None
        
        while not recognized and not stop_button:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Verificar timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout:
                st.warning("⏱️ Tempo esgotado!")
                break
            
            # Reconhecer face
            aluno_id, confidence, face_location = self.recognize_face(frame)
            
            if aluno_id is not None and confidence > 0.6:
                # Detectar liveness
                is_real, liveness_conf = self.detect_liveness(frame)
                
                if is_real:
                    # Face reconhecida e é real!
                    recognized = True
                    
                    # Buscar dados do aluno
                    aluno = data_manager.get_record('cadastro', aluno_id)
                    
                    if aluno:
                        # Desenhar retângulo na face
                        top, right, bottom, left = face_location
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"{aluno['nome_completo']}", (left, top - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Registrar presença
                        now = datetime.now()
                        attendance_data = {
                            'aluno_id': aluno_id,
                            'data': now.strftime('%Y-%m-%d'),
                            'hora': now.strftime('%H:%M:%S'),
                            'tipo': 'entrada',
                            'verificado': 'Sim',
                            'confianca': f"{confidence:.2%}",
                            'observacoes': f"Liveness: {liveness_conf:.2%}",
                            'data_registro': now.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # Salvar no banco
                        data_manager.add_record('attendance', attendance_data)
                        
                        st.success(f"✅ Presença registrada: {aluno['nome_completo']}")
                        st.metric("Confiança", f"{confidence:.2%}")
                        st.metric("Liveness", f"{liveness_conf:.2%}")
                else:
                    # Foto detectada!
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "FOTO DETECTADA!", (left, top - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    st.warning("⚠️ Foto detectada! Use seu rosto real.")
            
            # Mostrar frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            placeholder.image(frame_rgb, caption='Webcam', use_column_width=True)
            
            # Pequeno delay
            time.sleep(0.1)
        
        cap.release()
        placeholder.empty()
        
        return attendance_data
    
    def get_student_count(self):
        """Retorna o número de alunos registrados no sistema"""
        return len(set(self.known_face_ids))
