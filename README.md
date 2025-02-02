# yamlTranslator
Esses quatro scripts trabalham juntos para separar, traduzir, limpar e reunir um grande arquivo YAML em um processo estruturado e eficiente. Abaixo está a explicação detalhada de cada etapa

1️⃣ separar.py → Divide um grande arquivo YAML em partes menores
Objetivo:
Decompor arquivos YAML grandes em arquivos menores para facilitar a tradução e o processamento.

Fluxo de funcionamento:

Lê o arquivo principal (exemplo: 0003_ProceduralItemGenerationSettings.yml).
Analisa a estrutura YAML e mantém a hierarquia dos dicionários.
Divide os dicionários grandes em arquivos menores com no máximo 300 linhas cada.
Salva cada parte separadamente na pasta chaves/, nomeando os arquivos no formato:
0001_nomeDoDicionario_01.yml
0001_nomeDoDicionario_02.yml
Para garantir que possam ser reunidos corretamente depois.
Exemplo de entrada (portuguese_brazilian.yml):

yaml
Copiar
Editar
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"
  settings:
    language: "en"
    difficulty: "hard"
Saída esperada (arquivos separados):

yaml
Copiar
Editar
# 0001_config_01.yml
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"

# 0001_config_02.yml
config:
  settings:
    language: "en"
    difficulty: "hard"
2️⃣ python.py → Tradução automática via OpenAI
Objetivo:
Traduzir todos os arquivos da pasta chaves/ para português usando a API da OpenAI.

Fluxo de funcionamento:

Percorre os arquivos na pasta chaves/ e lê cada um.
Envia o conteúdo inteiro para a API do ChatGPT, garantindo que:
A estrutura YAML permaneça intacta.
Somente os valores sejam traduzidos (chaves e dicionários são preservados).
As listas YAML não sejam alteradas (- item continua no mesmo formato).
Variáveis ($valor) e códigos de formatação (&x, §x) não sejam alterados.
Recebe o YAML traduzido e salva na pasta chaves_traduzidos/ com o mesmo nome.
Exemplo de entrada (chaves/0001_config_01.yml):

yaml
Copiar
Editar
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"
Saída esperada (chaves_traduzidos/0001_config_01.yml):

yaml
Copiar
Editar
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
3️⃣ removeryaml.py → Remove formatação desnecessária do YAML
Objetivo:
Remover marcadores de código (```yaml e ```) que a OpenAI às vezes adiciona.

Fluxo de funcionamento:

Percorre todos os arquivos na pasta chaves_traduzidos/.
Verifica se a primeira ou última linha contém ```yaml ou ```.
Remove essas linhas e reescreve o arquivo sem elas.
Problema que resolve:
Às vezes, a OpenAI retorna YAML formatado assim:

yaml
Copiar
Editar
```yaml
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
yaml
Copiar
Editar
Isso pode causar **erros na remontagem do arquivo**. Esse script garante que o YAML fique correto.

---

## **4️⃣ `juntartudo.py` → Junta todas as partes traduzidas em um único arquivo**
**Objetivo:**  
Reunir os arquivos traduzidos da pasta `chaves_traduzidos/` em um único arquivo final `config_final.yml`.

**Fluxo de funcionamento:**
1. **Ordena os arquivos numericamente** (`0001`, `0002`, `0003`, ...).
2. **Lê cada arquivo e junta o conteúdo**, garantindo que:
   - **A sequência original seja preservada**.
   - **Não haja espaços extras entre os blocos YAML**.
3. **Salva o arquivo final como `config_final.yml`**.

**Exemplo de entrada (`chaves_traduzidos/`):**
```yaml
# 0001_config_01.yml
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"

# 0001_config_02.yml
config:
  settings:
    language: "pt-br"
    difficulty: "difícil"
Saída esperada (config_final.yml):

yaml
Copiar
Editar
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
  settings:
    language: "pt-br"
    difficulty: "difícil"
📌 Resumo do Processo Completo
1️⃣ separar.py → Divide um arquivo YAML grande em partes menores para facilitar a tradução.
2️⃣ python.py → Traduz cada parte separadamente usando a API da OpenAI.
3️⃣ removeryaml.py → Corrige erros de formatação gerados pela OpenAI.
4️⃣ juntartudo.py → Reúne todas as partes traduzidas em um único arquivo final.

🔥 Benefícios dessa abordagem:

Evita exceder o limite de caracteres da OpenAI.
Preserva a estrutura original do YAML.
Garante traduções precisas sem alterar variáveis e formatação.
Facilita o processamento e montagem final.
Este conjunto de scripts automatiza a tradução de arquivos YAML mantendo precisão e eficiência. 🚀







