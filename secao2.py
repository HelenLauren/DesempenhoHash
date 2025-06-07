# Seção 2, somativa - Desempenho de Hash Criptográfico
# Helen Lauren Bonato. BSI 3°período 
# Utilizei o código base no site: https://www.mdpi.com/2076-3417/13/10/5979?mwg_rnd=7933636 (Item 3.1, Figure 1 e Figure 2)
#Pedi para uma IA adapatar para um ataque de hash SHA-256, pois o código exemplo era uma verificação de igualdade de strings...
import time
import hashlib
import itertools
import json

def hash_sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def brute_force(hash_alvo):
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for tentativa in itertools.product(charset, repeat=4):  #senhas de 4 caracteres
        tentativa_str = ''.join(tentativa)
        if hash_sha256(tentativa_str) == hash_alvo:
            return tentativa_str
    return None

# Carrega usuários do JSON
with open('usuarios.json', 'r', encoding='utf-8') as f:
    usuarios = json.load(f)

tempos = []

print("🔐 Iniciando quebra de até 4 usuários...\n")

for i, (nome, dados) in enumerate(usuarios.items()):
    if i >= 4:
        break

    hash_salvo = dados['senha']
    print(f"Usuário: {nome}")
    print(f"Hash: {hash_salvo}")

    inicio = time.time()
    senha = brute_force(hash_salvo)
    fim = time.time()

    if senha:
        print(f" Senha encontrada: {senha}")
    else:
        print("Senha não encontrada.")

    duracao = fim - inicio
    tempos.append(duracao)
    print(f"⏱ Tempo: {duracao:.2f} segundos\n")

print("📊 Resumo:")
for i, t in enumerate(tempos):
    print(f"Usuário {i+1}: {t:.2f} segundos")

print(f"\nTempo total: {sum(tempos):.2f} segundos")