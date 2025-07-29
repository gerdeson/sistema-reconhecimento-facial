import cv2
import numpy as np
import os
import pickle
from pathlib import Path
import argparse
import time

class SimpleFaceRecognitionSystem:
    def __init__(self, cadastro_dir="cadastro", encodings_file="face_encodings.pkl"):
        """
        Sistema simplificado de reconhecimento facial usando OpenCV.
        
        Args:
            cadastro_dir (str): Diretório contendo as imagens de cadastro
            encodings_file (str): Arquivo para salvar/carregar encodings faciais
        """
        self.cadastro_dir = cadastro_dir
        self.encodings_file = encodings_file
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Carregar classificador de faces do OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Criar diretório de cadastro se não existir
        os.makedirs(cadastro_dir, exist_ok=True)
        
        # Carregar ou criar encodings
        self.load_or_create_encodings()
    
    def load_or_create_encodings(self):
        """
        Carrega encodings existentes ou cria novos a partir das imagens de cadastro.
        """
        # Tentar carregar encodings salvos
        if os.path.exists(self.encodings_file):
            try:
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                print(f"✓ Encodings carregados: {len(self.known_face_names)} pessoas cadastradas")
                return
            except Exception as e:
                print(f"Erro ao carregar encodings: {e}")
        
        # Criar novos encodings a partir das imagens
        self.create_encodings()
    
    def create_encodings(self):
        """
        Cria encodings faciais simples a partir das imagens no diretório de cadastro.
        """
        print("Criando encodings faciais...")
        
        # Extensões de imagem suportadas
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        for image_path in Path(self.cadastro_dir).iterdir():
            if image_path.suffix.lower() in image_extensions:
                try:
                    # Carregar imagem
                    image = cv2.imread(str(image_path))
                    if image is None:
                        print(f"✗ Erro ao carregar imagem: {image_path.name}")
                        continue
                    
                    # Converter para escala de cinza
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                    # Detectar faces
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces) > 0:
                        # Usar apenas o primeiro rosto encontrado
                        x, y, w, h = faces[0]
                        face_roi = gray[y:y+h, x:x+w]
                        
                        # Redimensionar para tamanho padrão
                        face_roi = cv2.resize(face_roi, (100, 100))
                        
                        # Nome da pessoa (nome do arquivo sem extensão)
                        name = image_path.stem.replace('_', ' ').title()
                        
                        self.known_face_encodings.append(face_roi)
                        self.known_face_names.append(name)
                        
                        print(f"✓ Processado: {name}")
                    else:
                        print(f"✗ Nenhum rosto encontrado em: {image_path.name}")
                        
                except Exception as e:
                    print(f"✗ Erro ao processar {image_path.name}: {e}")
        
        # Salvar encodings
        if self.known_face_encodings:
            self.save_encodings()
            print(f"✓ {len(self.known_face_names)} pessoas cadastradas com sucesso!")
        else:
            print("⚠ Nenhuma pessoa foi cadastrada. Adicione imagens ao diretório 'cadastro'.")
    
    def save_encodings(self):
        """
        Salva os encodings faciais em arquivo.
        """
        try:
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(data, f)
            print(f"✓ Encodings salvos em {self.encodings_file}")
        except Exception as e:
            print(f"Erro ao salvar encodings: {e}")
    
    def compare_faces(self, face1, face2, threshold=0.6):
        """
        Compara duas faces usando correlação normalizada.
        """
        try:
            # Redimensionar para o mesmo tamanho
            face1_resized = cv2.resize(face1, (100, 100))
            face2_resized = cv2.resize(face2, (100, 100))
            
            # Calcular correlação normalizada
            result = cv2.matchTemplate(face1_resized, face2_resized, cv2.TM_CCOEFF_NORMED)
            similarity = result[0][0]
            
            return similarity > threshold, similarity
        except:
            return False, 0.0
    
    def recognize_faces_video(self, source=0):
        """
        Reconhece rostos em tempo real usando webcam ou arquivo de vídeo.
        
        Args:
            source: 0 para webcam padrão ou caminho para arquivo de vídeo
        """
        # Inicializar captura de vídeo
        video_capture = cv2.VideoCapture(source)
        
        if not video_capture.isOpened():
            print("Erro: Não foi possível abrir a fonte de vídeo")
            return
        
        print("✓ Iniciando reconhecimento facial em tempo real...")
        print("Pressione 'q' para sair, 'r' para recarregar cadastro")
        
        # Variáveis para otimização
        process_this_frame = True
        fps_counter = 0
        start_time = time.time()
        
        while True:
            # Capturar frame
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Redimensionar frame para processamento mais rápido
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            gray_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            
            # Processar apenas frames alternados para melhor performance
            if process_this_frame:
                # Detectar faces
                faces = self.face_cascade.detectMultiScale(gray_small_frame, 1.1, 4)
                
                face_names = []
                for (x, y, w, h) in faces:
                    # Extrair ROI da face
                    face_roi = gray_small_frame[y:y+h, x:x+w]
                    
                    name = "Desconhecido"
                    best_similarity = 0.0
                    
                    # Comparar com faces conhecidas
                    for i, known_face in enumerate(self.known_face_encodings):
                        is_match, similarity = self.compare_faces(face_roi, known_face)
                        if is_match and similarity > best_similarity:
                            name = self.known_face_names[i]
                            best_similarity = similarity
                    
                    face_names.append((name, best_similarity))
            
            process_this_frame = not process_this_frame
            
            # Desenhar resultados no frame original
            for (x, y, w, h), (name, similarity) in zip(faces, face_names):
                # Escalar coordenadas de volta para o tamanho original
                x *= 2
                y *= 2
                w *= 2
                h *= 2
                
                # Cor do retângulo (verde para conhecido, vermelho para desconhecido)
                color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
                
                # Desenhar retângulo ao redor do rosto
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Desenhar label com nome e confiança
                label = f"{name} ({similarity:.2f})" if name != "Desconhecido" else name
                cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, label, (x+6, y+h-6), font, 0.6, (255, 255, 255), 1)
            
            # Calcular e mostrar FPS
            fps_counter += 1
            if fps_counter % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = fps_counter / elapsed_time
                cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Mostrar frame
            cv2.imshow('Reconhecimento Facial - Pressione "q" para sair', frame)
            
            # Verificar teclas pressionadas
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                print("Recarregando cadastro...")
                self.load_or_create_encodings()
        
        # Limpar recursos
        video_capture.release()
        cv2.destroyAllWindows()
        print("✓ Sistema encerrado")
    
    def recognize_face_in_image(self, image_path):
        """
        Reconhece rostos em uma imagem estática.
        
        Args:
            image_path (str): Caminho para a imagem
            
        Returns:
            list: Lista de nomes identificados
        """
        try:
            # Carregar imagem
            image = cv2.imread(image_path)
            if image is None:
                print(f"Erro ao carregar imagem: {image_path}")
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            identified_faces = []
            
            # Processar cada rosto encontrado
            for (x, y, w, h) in faces:
                # Extrair ROI da face
                face_roi = gray[y:y+h, x:x+w]
                
                name = "Desconhecido"
                best_similarity = 0.0
                
                # Comparar com faces conhecidas
                for i, known_face in enumerate(self.known_face_encodings):
                    is_match, similarity = self.compare_faces(face_roi, known_face)
                    if is_match and similarity > best_similarity:
                        name = self.known_face_names[i]
                        best_similarity = similarity
                
                identified_faces.append(name)
                
                # Cor do retângulo (verde para conhecido, vermelho para desconhecido)
                color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
                
                # Desenhar retângulo e nome na imagem
                cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(image, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                label = f"{name} ({best_similarity:.2f})" if name != "Desconhecido" else name
                cv2.putText(image, label, (x+6, y+h-6), font, 0.6, (255, 255, 255), 1)
            
            # Mostrar resultado
            cv2.imshow('Reconhecimento Facial', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            return identified_faces
            
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            return []


def main():
    """
    Função principal com interface de linha de comando.
    """
    parser = argparse.ArgumentParser(description='Sistema Simples de Reconhecimento Facial')
    parser.add_argument('--mode', choices=['video', 'image', 'setup'], default='video',
                       help='Modo de operação (padrão: video)')
    parser.add_argument('--source', default=0,
                       help='Fonte de vídeo (0 para webcam) ou caminho da imagem')
    parser.add_argument('--cadastro', default='cadastro',
                       help='Diretório com imagens de cadastro')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    print("🔍 Iniciando Sistema Simples de Reconhecimento Facial")
    print("=" * 50)
    
    face_system = SimpleFaceRecognitionSystem(cadastro_dir=args.cadastro)
    
    if args.mode == 'setup':
        # Modo setup - apenas criar encodings
        print("Modo setup concluído!")
        
    elif args.mode == 'image':
        # Modo imagem
        if isinstance(args.source, str) and os.path.exists(args.source):
            print(f"Processando imagem: {args.source}")
            identified = face_system.recognize_face_in_image(args.source)
            print(f"Pessoas identificadas: {identified}")
        else:
            print("✗ Arquivo de imagem não encontrado")
            
    else:
        # Modo vídeo (padrão)
        try:
            source = int(args.source) if args.source.isdigit() else args.source
        except:
            source = args.source
            
        face_system.recognize_faces_video(source)


if __name__ == "__main__":
    print("""
    🎯 Sistema Simples de Reconhecimento Facial
    
    Para usar este sistema:
    
    1. Crie uma pasta 'cadastro' e adicione fotos das pessoas
       - Nomeie os arquivos como: 'joao_silva.jpg', 'maria_santos.png', etc.
       - Use uma foto por pessoa, com o rosto bem visível
    
    2. Execute o programa:
       - python cadastro_simples.py --mode video    # Webcam em tempo real
       - python cadastro_simples.py --mode image --source foto.jpg  # Processar uma imagem
       - python cadastro_simples.py --mode setup    # Apenas criar cadastro
    
    3. No modo vídeo:
       - Pressione 'q' para sair
       - Pressione 'r' para recarregar o cadastro
    
    Bibliotecas necessárias:
    pip install opencv-python numpy pillow
    
    """)
    
    main() 