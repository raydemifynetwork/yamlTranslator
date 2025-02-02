import os

# Diretório onde estão os arquivos YAML traduzidos
pasta_traduzida = "chaves_traduzidos"
# Arquivo final de saída
arquivo_saida = "config_final.yml"

# Obter lista ordenada dos arquivos
arquivos_yaml = sorted(os.listdir(pasta_traduzida))

# Abrir o arquivo de saída para escrita
with open(arquivo_saida, "w", encoding="utf-8") as saida:
    for i, arquivo in enumerate(arquivos_yaml):
        caminho_arquivo = os.path.join(pasta_traduzida, arquivo)

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as entrada:
                conteudo = entrada.read().strip()  # Remove espaços extras antes e depois

                # Evita pular linha extra no final do arquivo
                if conteudo:
                    if i > 0:  # Apenas adiciona nova linha antes de arquivos subsequentes
                        saida.write("\n")
                    saida.write(conteudo)

            print(f"✅ Arquivo {arquivo} mesclado.")

        except Exception as e:
            print(f"❌ Erro ao ler {arquivo}: {e}")

print(f"✅ Todos os arquivos foram mesclados em '{arquivo_saida}'")
