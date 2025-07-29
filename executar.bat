@echo off
echo ========================================
echo Sistema de Reconhecimento Facial
echo ========================================
echo.
echo Escolha uma opcao:
echo.
echo 1. Modo Video (Webcam)
echo 2. Modo Setup (Criar cadastro)
echo 3. Modo Imagem (Processar foto)
echo 4. Sair
echo.
set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" (
    echo.
    echo Iniciando modo video...
    python cadastro_simples.py --mode video
    goto fim
)

if "%opcao%"=="2" (
    echo.
    echo Criando cadastro...
    python cadastro_simples.py --mode setup
    goto fim
)

if "%opcao%"=="3" (
    echo.
    set /p imagem="Digite o caminho da imagem: "
    echo Processando imagem...
    python cadastro_simples.py --mode image --source "%imagem%"
    goto fim
)

if "%opcao%"=="4" (
    echo Saindo...
    goto fim
)

echo Opcao invalida!
pause

:fim
echo.
echo Pressione qualquer tecla para sair...
pause >nul 