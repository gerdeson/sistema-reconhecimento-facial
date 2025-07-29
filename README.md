# Sistema de Reconhecimento Facial

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-gerdeson%2Fsistema--reconhecimento--facial-brightgreen.svg)](https://github.com/gerdeson/sistema-reconhecimento-facial)

Este é um sistema simples de reconhecimento facial desenvolvido em Python usando OpenCV.

## 📋 Pré-requisitos

Antes de usar o sistema, você precisa instalar as bibliotecas necessárias:

```bash
pip install opencv-python numpy pillow
```

Ou use o script de instalação automática:
```bash
# Windows
install.bat

# Linux/Mac
pip install -r requirements.txt
```

## 🚀 Como usar

### 1. Preparar o cadastro

1. Crie uma pasta chamada `cadastro` no diretório do projeto
2. Adicione fotos das pessoas que você quer reconhecer
3. Nomeie os arquivos com o nome da pessoa (ex: `joao_silva.jpg`, `maria_santos.png`)
4. Use uma foto por pessoa, com o rosto bem visível

### 2. Executar o sistema

#### Modo Vídeo (Webcam em tempo real)
```bash
python cadastro_simples.py --mode video
```

#### Modo Imagem (Processar uma foto)
```bash
python cadastro_simples.py --mode image --source caminho/para/foto.jpg
```

#### Modo Setup (Apenas criar cadastro)
```bash
python cadastro_simples.py --mode setup
```

#### Interface Gráfica (Windows)
```bash
executar.bat
```

### 3. Controles no modo vídeo

- **Q**: Sair do programa
- **R**: Recarregar o cadastro (útil quando você adiciona novas fotos)

## 📁 Estrutura de arquivos

```
cadastro/
├── cadastro_simples.py    # Sistema principal
├── cadastro.py            # Versão original (requer face-recognition)
├── cadastro/              # Pasta com fotos das pessoas
│   ├── joao_silva.jpg
│   ├── maria_santos.png
│   └── ...
├── face_encodings.pkl     # Arquivo com dados de reconhecimento (criado automaticamente)
├── install.bat            # Script de instalação (Windows)
├── executar.bat           # Interface gráfica (Windows)
├── requirements.txt       # Dependências Python
└── README.md              # Este arquivo
```

## 🎯 Funcionalidades

- **Detecção facial**: Identifica rostos em imagens e vídeo
- **Reconhecimento**: Compara rostos detectados com o cadastro
- **Tempo real**: Funciona com webcam em tempo real
- **Interface visual**: Mostra retângulos verdes para pessoas conhecidas e vermelhos para desconhecidas
- **Confiança**: Mostra o nível de confiança do reconhecimento

## ⚙️ Configurações

### Parâmetros de linha de comando

- `--mode`: Modo de operação (`video`, `image`, `setup`)
- `--source`: Fonte de vídeo (0 para webcam) ou caminho da imagem
- `--cadastro`: Diretório com imagens de cadastro (padrão: `cadastro`)

### Exemplos de uso

```bash
# Usar webcam
python cadastro_simples.py --mode video

# Usar arquivo de vídeo
python cadastro_simples.py --mode video --source video.mp4

# Processar uma imagem
python cadastro_simples.py --mode image --source foto.jpg

# Usar diretório de cadastro personalizado
python cadastro_simples.py --mode video --cadastro minhas_fotos
```

## 🔧 Solução de problemas

### Erro: "Nenhuma pessoa foi cadastrada"
- Verifique se a pasta `cadastro` existe
- Adicione fotos com rostos visíveis
- Execute o modo setup primeiro

### Erro: "Não foi possível abrir a fonte de vídeo"
- Verifique se a webcam está conectada
- Tente usar um número diferente de câmera (1, 2, etc.)

### Performance lenta
- O sistema processa frames alternados para melhor performance
- Redimensione as imagens de cadastro para melhor velocidade

## 📝 Notas técnicas

- O sistema usa o classificador Haar Cascade do OpenCV para detecção facial
- A comparação é feita usando correlação normalizada
- Os dados de reconhecimento são salvos em `face_encodings.pkl`
- O sistema funciona melhor com fotos de boa qualidade e boa iluminação

## 🤝 Contribuição

Para melhorar o sistema, você pode:

1. Ajustar o threshold de similaridade no método `compare_faces`
2. Implementar algoritmos mais avançados de reconhecimento
3. Adicionar suporte para múltiplas faces por pessoa
4. Melhorar a interface do usuário

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🌟 Agradecimentos

- [OpenCV](https://opencv.org/) - Biblioteca de visão computacional
- [NumPy](https://numpy.org/) - Computação numérica
- [Pillow](https://python-pillow.org/) - Processamento de imagens

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no GitHub!** 