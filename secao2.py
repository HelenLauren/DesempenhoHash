# Seção 2, somativa - Desempenho de Hash Criptográfico
# Helen Lauren Bonato. BSI 3°período 
# Utilizei o código base no site: https://www.mdpi.com/2076-3417/13/10/5979?mwg_rnd=7933636 (Item 3.1, Figure 1 e Figure 2)
#Pedi para uma IA adapatar para um ataque de hash SHA-256, pois o código exemplo era uma verificação de igualdade de strings...
import time
import hashlib
import itertools
import concurrent.futures
import os

#função de hash
def hash_sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

#função de tentativa de combinação
def attempt_match(length, target_hash):
    for attempt in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzç0123456789!@#$%&*_-?", repeat=length):
        attempt_str = "".join(attempt)
        if hash_sha256(attempt_str) == target_hash:
            print("Senha encontrada:", attempt_str)
            return attempt_str
    return None

if __name__ == '__main__':
    target_password = input("Digite a senha a ser descoberta: ")
    target_hash = hash_sha256(target_password)

    total_cores = os.cpu_count()
    num_cores = max(1, total_cores // 2)  #usa apenas metade dos núcleos disponíveis

    print(f"\nNúcleos disponíveis: {total_cores}")
    print(f"Usando {num_cores} núcleo(s) para processamento...\n")

    start_time = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(attempt_match, length, target_hash) for length in range(1, 5)]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                break

    end_time = time.perf_counter()
    print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
