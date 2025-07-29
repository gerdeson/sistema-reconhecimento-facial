import cv2
import face_recognition
import numpy as np
import os
import pickle
from pathlib import Path
import argparse
import time

class FaceRecognitionSystem:
    def __init__(self, cadastro_dir="cadastro", encodings_file="face_encodings.pkl"):
        """
        Inicializa o sistema de reconhecimento facial.
        
        Args:
            cadastro_dir (str): Diretório contendo as imagens de cadastro
            encodings_file (str): Arquivo para salvar/carregar encodings faciais
        """
        self.cadastro_dir = cadastro_dir
        self.encodings_file = encodings_file
        self.known_face_encodings = []
        self.known_face_names = []
        
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
        Cria encodings faciais a partir das imagens no diretório de cadastro.
        """
        print("Criando encodings faciais...")
        
        # Extensões de imagem suportadas
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        for image_path in Path(self.cadastro_dir).iterdir():
            if image_path.suffix.lower() in image_extensions:
                try:
                    # Carregar imagem
                    image = face_recognition.load_image_file(str(image_path))
                    
                    # Encontrar encodings faciais
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        # Usar apenas o primeiro rosto encontrado
                        encoding = encodings[0]
                        
                        # Nome da pessoa (nome do arquivo sem extensão)
                        name = image_path.stem.replace('_', ' ').title()
                        
                        self.known_face_encodings.append(encoding)
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
            image = face_recognition.load_image_file(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Encontrar localizações e encodings dos rostos
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            identified_faces = []
            
            # Processar cada rosto encontrado
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Comparar com rostos conhecidos
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding, tolerance=0.6
                )
                name = "Desconhecido"
                
                # Usar distâncias para encontrar a melhor correspondência
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, face_encoding
                )
                
                if matches and len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        print(f"✓ Identificado: {name} (Confiança: {confidence:.2f})")
                
                identified_faces.append(name)
                
                # Desenhar retângulo e nome na imagem
                cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(rgb_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(rgb_image, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
            
            # Mostrar resultado
            cv2.imshow('Reconhecimento Facial', rgb_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            return identified_faces
            
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            return []
    
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
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Processar apenas frames alternados para melhor performance
            if process_this_frame:
                # Encontrar rostos e encodings
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    # Comparar com faces conhecidas
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding, tolerance=0.6
                    )
                    name = "Desconhecido"
                    
                    # Usar distâncias para melhor precisão
                    if self.known_face_encodings:
                        face_distances = face_recognition.face_distance(
                            self.known_face_encodings, face_encoding
                        )
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                            name = self.known_face_names[best_match_index]
                    
                    face_names.append(name)
            
            process_this_frame = not process_this_frame
            
            # Desenhar resultados no frame original
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Escalar coordenadas de volta para o tamanho original
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Cor do retângulo (verde para conhecido, vermelho para desconhecido)
                color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
                
                # Desenhar retângulo ao redor do rosto
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Desenhar label com nome
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
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
    
    def add_person(self, image_path, person_name):
        """
        Adiciona uma nova pessoa ao cadastro.
        
        Args:
            image_path (str): Caminho para a imagem da pessoa
            person_name (str): Nome da pessoa
        """
        try:
            # Carregar e processar imagem
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            
            if not encodings:
                print("✗ Nenhum rosto encontrado na imagem")
                return False
            
            # Adicionar encoding e nome
            self.known_face_encodings.append(encodings[0])
            self.known_face_names.append(person_name)
            
            # Salvar encodings atualizados
            self.save_encodings()
            
            print(f"✓ {person_name} adicionado ao cadastro")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao adicionar pessoa: {e}")
            return False


def main():
    """
    Função principal com interface de linha de comando.
    """
    parser = argparse.ArgumentParser(description='Sistema de Reconhecimento Facial')
    parser.add_argument('--mode', choices=['video', 'image', 'setup'], default='video',
                       help='Modo de operação (padrão: video)')
    parser.add_argument('--source', default=0,
                       help='Fonte de vídeo (0 para webcam) ou caminho da imagem')
    parser.add_argument('--cadastro', default='cadastro',
                       help='Diretório com imagens de cadastro')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    print("🔍 Iniciando Sistema de Reconhecimento Facial")
    print("=" * 50)
    
    face_system = FaceRecognitionSystem(cadastro_dir=args.cadastro)
    
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
    🎯 Sistema de Reconhecimento Facial
    
    Para usar este sistema:
    
    1. Crie uma pasta 'cadastro' e adicione fotos das pessoas
       - Nomeie os arquivos como: 'joao_silva.jpg', 'maria_santos.png', etc.
       - Use uma foto por pessoa, com o rosto bem visível
    
    2. Execute o programa:
       - python face_recognition.py --mode video    # Webcam em tempo real
       - python face_recognition.py --mode image --source foto.jpg  # Processar uma imagem
       - python face_recognition.py --mode setup    # Apenas criar cadastro
    
    3. No modo vídeo:
       - Pressione 'q' para sair
       - Pressione 'r' para recarregar o cadastro
    
    Bibliotecas necessárias:
    pip install opencv-python face-recognition numpy pillow
    
    """)
    
    main()