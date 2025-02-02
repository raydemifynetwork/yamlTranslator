import os
import yaml
import openai
import time
from collections import OrderedDict

# Configuração da API OpenAI
client = openai.OpenAI(api_key="chaveaqui")

# Diretórios de entrada e saída
pasta_entrada = "chaves"
pasta_saida = "chaves_traduzidos"

# Criar a pasta de saída se não existir
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)


# Carregar YAML mantendo a ordem das chaves
def yaml_load_ordered(stream):
    """Carrega YAML mantendo a ordem das chaves."""

    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


# Salvar YAML mantendo a ordem das chaves
def yaml_dump_ordered(data, stream=None):
    """Salva YAML mantendo a ordem das chaves."""

    class OrderedDumper(yaml.SafeDumper):
        pass

    def dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, dict_representer)

    return yaml.dump(data, stream, OrderedDumper, allow_unicode=True, default_flow_style=False)


# Função para chamar a OpenAI e traduzir um arquivo inteiro
def chamar_openai_para_traducao(nome_arquivo, yaml_texto):
    """ Envia um arquivo inteiro para a API OpenAI para tradução. """
    prompt = f"""
O seguinte é um arquivo de configuração YAML para um servidor de Minecraft:

**Nome do arquivo:** {nome_arquivo}

**Texto original:** 

```yaml
{yaml_texto}
```

**Regras para tradução:**
- Traduza **todo o conteúdo** para **português do Brasil**.
- **Mantenha listas YAML no formato correto** (cada item com `- `).
- **NÃO traduza variáveis que começam com `$`**. Elas são placeholders e devem permanecer iguais.
- **Preserve códigos de formatação** (`&x`, `§x`).
- **Mantenha a estrutura do YAML intacta.**
- **NÃO traduza os nomes das chaves e dicionários. Apenas traduza os valores que não são chaves.**
- **Não adicione explicações, retorne apenas o YAML traduzido.**

Agora, traduza:
"""

    print(f"🚀 Enviando arquivo inteiro para tradução: {nome_arquivo}...")  # Log para depuração

    tentativa = 0
    max_tentativas = 5

    while tentativa < max_tentativas:
        try:
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em tradução de arquivos YAML."},
                    {"role": "user", "content": prompt}
                ]
            )
            yaml_traduzido = resposta.choices[0].message.content.strip()

            print(f"✅ Tradução concluída para {nome_arquivo}")
            return yaml_traduzido

        except openai.RateLimitError:
            print(f"⚠️ Rate Limit atingido. Tentando novamente... ({tentativa + 1}/{max_tentativas})")
            time.sleep(20)
            tentativa += 1

        except Exception as e:
            print(f"❌ Erro ao chamar OpenAI: {e}")
            return yaml_texto  # Retorna o original se der erro

    print("❌ Erro de Rate Limit não resolvido após múltiplas tentativas.")
    return yaml_texto


# Função para processar os arquivos YAML inteiros
def traduzir_arquivos_yaml():
    """Traduz arquivos YAML inteiros ao invés de linha por linha."""
    arquivos_yaml = sorted(os.listdir(pasta_entrada))

    for arquivo in arquivos_yaml:
        caminho_entrada = os.path.join(pasta_entrada, arquivo)
        caminho_saida = os.path.join(pasta_saida, arquivo)

        print(f"📌 Processando arquivo: {arquivo}")

        try:
            with open(caminho_entrada, "r", encoding="utf-8") as file:
                yaml_texto = file.read().strip()

        except Exception as e:
            print(f"❌ Erro ao ler o arquivo {arquivo}: {e}")
            continue

        # Se o arquivo estiver vazio, pula
        if not yaml_texto:
            print(f"⚠️ Arquivo vazio, pulando: {arquivo}")
            continue

        # Traduzir o arquivo inteiro
        yaml_traduzido = chamar_openai_para_traducao(arquivo, yaml_texto)

        # Salvar o arquivo traduzido
        with open(caminho_saida, "w", encoding="utf-8") as file:
            file.write(yaml_traduzido)

        print(f"✅ Tradução salva para {arquivo}")


# Executar o script de tradução
traduzir_arquivos_yaml()

print(f"✅ Todos os arquivos foram traduzidos e salvos em '{pasta_saida}/'.")
