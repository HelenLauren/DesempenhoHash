import hashlib
import json
import getpass

ARQUIVO_USUARIOS = 'usuarios.json'

def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def cadastrar(self):
        if len(self.nome) != 4 or len(self.senha) != 4:
            print("❗ Nome e senha devem ter exatamente 4 caracteres.")
            return False

        dados_usuarios = carregar_dados(ARQUIVO_USUARIOS)

        if self.nome in dados_usuarios:
            print("❌ Usuário já cadastrado.")
            return False

        dados_usuarios[self.nome] = {
            'senha': hash_senha(self.senha)
        }

        salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
        print("✅ Cadastro realizado com sucesso!")
        return True

    def autenticar(self):
        dados_usuarios = carregar_dados(ARQUIVO_USUARIOS)

        usuario = dados_usuarios.get(self.nome)

        if not usuario:
            return False, "❌ Usuário não encontrado."

        if usuario['senha'] == hash_senha(self.senha):
            return True, "✅ Autenticado com sucesso!"
        else:
            return False, "❌ Senha incorreta."

# Menu principal
while True:
    print("\n" + "="*40)
    print("🔐 MENU INICIAL".center(40))
    opcao = input("\n1 - Cadastrar\n2 - Entrar\n3 - Sair\nEscolha: ")
    print("="*40)

    if opcao == '3':
        print("Saindo do sistema...")
        break

    if opcao not in ['1', '2']:
        print("Opção inválida!")
        continue

    nome = input("👤 Nome (4 letras): ")
    senha = getpass.getpass("🔑 Senha (4 letras): ")

    usuario = Usuario(nome, senha)

    if opcao == '1':
        usuario.cadastrar()
    elif opcao == '2':
        sucesso, mensagem = usuario.autenticar()
        print(mensagem)