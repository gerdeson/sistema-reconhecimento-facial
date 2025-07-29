# 🚀 Deploy no GitHub

## Passos para publicar no GitHub:

### 1. Criar repositório no GitHub
1. Acesse [github.com](https://github.com)
2. Clique em "New repository" (botão verde)
3. Configure o repositório:
   - **Repository name**: `sistema-reconhecimento-facial`
   - **Description**: Sistema de reconhecimento facial em Python usando OpenCV
   - **Visibility**: Public (ou Private se preferir)
   - **NÃO** marque "Add a README file" (já temos um)
   - **NÃO** marque "Add .gitignore" (já temos um)
4. Clique em "Create repository"

### 2. Conectar repositório local ao GitHub
Execute os comandos abaixo no terminal:

```bash
# Adicionar o repositório remoto (substitua SEU_USUARIO pelo seu nome de usuário)
git remote add origin https://github.com/SEU_USUARIO/sistema-reconhecimento-facial.git

# Enviar o código para o GitHub
git branch -M main
git push -u origin main
```

### 3. Verificar se funcionou
1. Acesse seu repositório no GitHub
2. Verifique se todos os arquivos estão lá
3. Teste o botão "Code" para clonar

## 📁 Arquivos incluídos no repositório:

- ✅ `cadastro_simples.py` - Sistema principal
- ✅ `README.md` - Documentação completa
- ✅ `requirements.txt` - Dependências
- ✅ `install.bat` - Script de instalação
- ✅ `executar.bat` - Interface gráfica
- ✅ `.gitignore` - Exclusões do Git
- ✅ `cadastro/` - Pasta com fotos de exemplo

## 🎯 Próximos passos após o deploy:

1. **Adicionar badges** no README.md
2. **Configurar GitHub Actions** para testes automáticos
3. **Adicionar releases** com versões
4. **Configurar Issues** para melhorias

## 🔧 Comandos úteis para manutenção:

```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Enviar para GitHub
git push

# Baixar mudanças do GitHub
git pull
``` 