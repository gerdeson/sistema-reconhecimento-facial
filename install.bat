@echo off
echo ========================================
echo Instalando dependencias do sistema...
echo ========================================

echo.
echo Instalando OpenCV...
pip install opencv-python

echo.
echo Instalando NumPy...
pip install numpy

echo.
echo Instalando Pillow...
pip install pillow

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Para usar o sistema:
echo 1. Adicione fotos na pasta 'cadastro'
echo 2. Execute: python cadastro_simples.py --mode video
echo.
pause 