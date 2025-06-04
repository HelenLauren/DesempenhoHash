# Seção 3, somativa - Desempenho de Hash Criptográfico
# Helen Lauren Bonato. BSI 3°período
# Adicionado o salt que garante que senhas iguais gerem hashes diferentes e pbkdf2_hmac que aplica o hash várias vezes na senha.
import hashlib
import json
import getpass
import os
import base64

#funções de segurança com salt e pbkdf2_hmac
def gerar_salt():
    return base64.b64encode(os.urandom(16)).decode()

def hash_com_salt(senha, salt, iteracoes=100_000):
    senha_bytes = senha.encode()
    salt_bytes = base64.b64decode(salt)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', senha_bytes, salt_bytes, iteracoes)
    return base64.b64encode(hash_bytes).decode()

#carrega e salva dados de um arquivo JSON
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

#carrega os dados
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
            return False, "🚫 Conta bloqueada permanentemente por excesso de tentativas."

        if usuario['senha'] == hash_senha(self.senha):
            usuario['tentativas'] = 0  #zera as tentativas no login bem-sucedido
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
        if len(self.nome) != 4 or len(self.senha) != 4:
            print("❗ Nome e senha devem ter exatamente 4 caracteres.")
            return False

        if self.nome in dados_usuarios:
            print("Usuário já existe!")
            return False

        dados_usuarios[self.nome] = {
            'senha': hash_senha(self.senha),
            'tentativas': 0,
            'bloqueado': False
        }

        dados_permissoes[self.nome] = {"ler": [], "escrever": [], "apagar": []}

        salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
        salvar_dados(ARQUIVO_PERMISSOES, dados_permissoes)
        print("✅ Cadastro realizado com sucesso!")
        return True

# menu de login ou cadastro
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
        if usuario.cadastrar():
            print("✅ Cadastro realizado com sucesso!")
        continue

    autenticado, mensagem = usuario.autenticar()
    print(mensagem)
    if autenticado:
        usuario_autenticado = nome
        break

# menu de permissões
if usuario_autenticado:
    while True:
        print("\n" + "="*40)
        print("📂  MENU DE PERMISSÕES  📂".center(40))
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
                    if arquivo not in arquivos_com_permissoes:
                        arquivos_com_permissoes[arquivo] = []
                    arquivos_com_permissoes[arquivo].append(acao)

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