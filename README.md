YAML Translation Automation with OpenAI GPT-3.5 Turbo 🚀
This project consists of four Python scripts that work together to split, translate, clean, and merge a large YAML file in a structured and efficient process. Below is a detailed explanation of each step:

1️⃣ separar.py → Splitting a Large YAML File into Smaller Parts
Objective:
Break down large YAML files into smaller, manageable parts to facilitate translation and processing.

How It Works:
✅ Reads the main YAML file (e.g., 0003_ProceduralItemGenerationSettings.yml).
✅ Preserves the dictionary hierarchy while splitting the content.
✅ Divides large dictionaries into smaller files, ensuring a maximum of 300 lines per file.
✅ Saves each part in the chaves/ folder, using the following naming format:

```
0001_dictionaryName_01.yml  
0001_dictionaryName_02.yml  
This ensures proper reassembly later.
```
Example Input (portuguese_brazilian.yml):
```
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"
  settings:
    language: "en"
    difficulty: "hard"
```
Expected Output (Split Files in chaves/):
```
# 0001_config_01.yml
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"
```

```
# 0001_config_02.yml
config:
  settings:
    language: "en"
    difficulty: "hard"
```
2️⃣ python.py → Automatic Translation via OpenAI
Objective:
Translate all files inside the chaves/ folder to Portuguese using the OpenAI GPT-3.5 Turbo API.

How It Works:
✅ Reads each file inside chaves/.
✅ Sends the entire content to the OpenAI API while ensuring:

The YAML structure remains intact.
Only values are translated (keys and dictionary names remain unchanged).
Lists remain formatted correctly (- item stays in the same format).
Variables ($value) and color codes (&x, §x) are not altered.
✅ Receives the translated YAML and saves it in the chaves_traduzidos/ folder with the same filename.
Example Input (chaves/0001_config_01.yml):
```
config:
  messages:
    welcome: "Welcome!"
    error: "Something went wrong!"
Expected Output (chaves_traduzidos/0001_config_01.yml):
```

```
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
```
3️⃣ removeryaml.py → Removing Unwanted YAML Formatting
Objective:
Remove unnecessary formatting artifacts (```yaml and ```) that OpenAI sometimes adds.

How It Works:
✅ Scans all files inside the chaves_traduzidos/ folder.
✅ Detects and removes any unwanted formatting from the first and last lines.
✅ Rewrites the cleaned file, ensuring correct YAML formatting.

Problem It Fixes:
Sometimes, OpenAI returns formatted YAML like this:

```
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
This can cause errors when merging the files. This script ensures that the YAML is correctly formatted.
```
4️⃣ juntartudo.py → Merging All Translated Parts into a Single File
Objective:
Reassemble the translated files from chaves_traduzidos/ into a single final YAML file (config_final.yml).

How It Works:
✅ Sorts files numerically (0001, 0002, 0003, ...).
✅ Reads each file and merges the content while ensuring:

The original sequence is preserved.
No extra spaces between YAML blocks.
✅ Saves the final merged file as config_final.yml.
Example Input (chaves_traduzidos/):
```
# 0001_config_01.yml
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
```
```
# 0001_config_02.yml
config:
  settings:
    language: "pt-br"
    difficulty: "difícil"
Expected Output (config_final.yml):
```
```
config:
  messages:
    welcome: "Bem-vindo!"
    error: "Algo deu errado!"
  settings:
    language: "pt-br"
    difficulty: "difícil"
```
📌 Full Process Summary
1️⃣ separar.py → Splits a large YAML file into smaller parts to facilitate translation.
2️⃣ python.py → Translates each part separately using OpenAI’s API.
3️⃣ removeryaml.py → Fixes formatting errors introduced by OpenAI.
4️⃣ juntartudo.py → Merges all translated parts into a final single file.

🔥 Key Benefits of This Approach:
✅ Avoids exceeding OpenAI's character limit.
✅ Preserves the original YAML structure.
✅ Ensures precise translations without modifying variables and formatting.
✅ Facilitates processing and final reassembly.

This set of scripts automates YAML translation while ensuring efficiency and accuracy. 🚀
