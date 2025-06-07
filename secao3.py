# Seção 3, somativa - Desempenho de Hash Criptográfico
# Helen Lauren Bonato. BSI 3°período
# Validação de senha forte e hash simples com SHA-256

import hashlib
import json
import getpass
import os
import re

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r'[a-z]', senha):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\[\]\\\/\-+=]', senha):
        return False, "A senha deve conter pelo menos um caractere especial."
    return True, ""

def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4)

ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PERMISSOES = 'permissoes.json'

dados_usuarios = carregar_dados(ARQUIVO_USUARIOS)
dados_permissoes = carregar_dados(ARQUIVO_PERMISSOES)

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def autenticar(self):
        usuario = dados_usuarios.get(self.nome)
        if not usuario:
            return False, "Usuário não encontrado."

        if usuario.get('bloqueado', False):
            return False, "Conta bloqueada permanentemente por excesso de tentativas."

        if usuario['senha'] == hash_senha(self.senha):
            usuario['tentativas'] = 0
            salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
            return True, "✅ Autenticado com sucesso!"
        else:
            usuario['tentativas'] = usuario.get('tentativas', 0) + 1
            if usuario['tentativas'] >= 3:
                usuario['bloqueado'] = True
                salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
                return False, "🚫 Conta bloqueada após 3 tentativas inválidas."
            salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
            tentativas_restantes = 3 - usuario['tentativas']
            return False, f"❌ Senha incorreta. Tentativas restantes: {tentativas_restantes}"

    def cadastrar(self):
        if self.nome in dados_usuarios:
            print("Usuário já existe!")
            return False

        valida, mensagem = validar_senha(self.senha)
        if not valida:
            print(mensagem)
            return False

        dados_usuarios[self.nome] = {
            'senha': hash_senha(self.senha),
            'tentativas': 0,
            'bloqueado': False
        }

        dados_permissoes[self.nome] = {"ler": [], "escrever": [], "apagar": []}

        salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
        salvar_dados(ARQUIVO_PERMISSOES, dados_permissoes)
        print("Cadastro realizado com sucesso!")
        return True

# Menu de login ou cadastro
usuario_autenticado = None

while True:
    print("\n" + "="*40)
    print(" 🔐MENU INICIAL Atividade Somativa Hash Criptográfico".center(40))
    opcao = input("\n1 - Cadastrar\n2 - Entrar\n3 - Sair\nEscolha: ")
    print("\n" + "="*40)
    if opcao not in ['1', '2', '3']:
        print("Opção inválida!")
        continue

    if opcao == '3':
        print("Saindo do sistema...")
        break

    nome = input("\n👤 Nome: ")
    senha = getpass.getpass("\033[1;32m🔑 Senha:\033[m ")
    print("\n" + "="*40)
    usuario = Usuario(nome, senha)

    if opcao == '1':
        usuario.cadastrar()
        continue

    autenticado, mensagem = usuario.autenticar()
    print(mensagem)
    if autenticado:
        usuario_autenticado = nome
        break

# Menu de permissões
if usuario_autenticado:
    while True:
        print("\n" + "="*40)
        print("  MENU DE PERMISSÕES  ".center(40))
        print("\nOPÇÕES:")
        opcao = input("1 - Ler\n2 - Escrever\n3 - Apagar\n4 - Executar\n5 - Consultar arquivos disponíveis permitidos\n0 - Sair\nEscolha: ")
        print("\n" + "="*40)

        if opcao == '0':
            print("Saindo do sistema...")
            break

        if opcao == '5':
            permissoes_usuario = dados_permissoes.get(usuario_autenticado, {})
            arquivos_com_permissoes = {}

            for acao, arquivos in permissoes_usuario.items():
                for arquivo in arquivos:
                    arquivos_com_permissoes.setdefault(arquivo, []).append(acao)

            if arquivos_com_permissoes:
                print("\nArquivos disponíveis e permissões:")
                for arquivo, acoes in arquivos_com_permissoes.items():
                    print(f"  📂 {arquivo}: {', '.join(acoes)}")
            else:
                print("\nNenhum arquivo disponível.")
            continue

        tipo_acao = {"1": "ler", "2": "escrever", "3": "apagar", "4": "executar"}.get(opcao)
        if not tipo_acao:
            print("Opção inválida!")
            continue

        arquivo = input("Insira o nome do arquivo que deseja " + tipo_acao + ": ")

        if arquivo in dados_permissoes.get(usuario_autenticado, {}).get(tipo_acao, []):
            print("Acesso permitido")
            if opcao == '4':
                print(f"Executando o arquivo {arquivo}...")
        else:
            print("Acesso negado")