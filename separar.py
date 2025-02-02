import os
import yaml

# Nome do arquivo YAML de entrada
arquivo_yaml = "0003_ProceduralItemGenerationSettings.yml"
pasta_saida = "chaves"
LINHAS_LIMITE = 300  # Número máximo de linhas por arquivo

# Criar a pasta "chaves" se não existir
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# Ler o arquivo YAML
with open(arquivo_yaml, "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)


# Criar arquivos divididos para dicionários grandes
def dividir_e_salvar(dicionario_pai, conteudo, prefixo, contador=1):
    """Divide um dicionário grande em partes menores e salva como arquivos numerados."""
    yaml_texto = yaml.dump({dicionario_pai: conteudo}, allow_unicode=True, default_flow_style=False)
    linhas = yaml_texto.split("\n")

    partes = [linhas[i:i + LINHAS_LIMITE] for i in range(0, len(linhas), LINHAS_LIMITE)]

    for parte in partes:
        nome_arquivo = f"{pasta_saida}/{prefixo}_{str(contador).zfill(2)}.yml"
        with open(nome_arquivo, "w", encoding="utf-8") as file:
            file.write("\n".join(parte))
        contador += 1


# Processar os dicionários
for index, (dicionario_pai, conteudo) in enumerate(yaml_data.items(), start=1):
    prefixo = f"{str(index).zfill(4)}_{dicionario_pai}"

    if isinstance(conteudo, dict) or isinstance(conteudo, list):  # Se for um dicionário grande
        dividir_e_salvar(dicionario_pai, conteudo, prefixo)

print(f"✅ Extração e divisão concluída! Arquivos gerados na pasta '{pasta_saida}/'.")
