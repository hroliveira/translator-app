import os
from utils import extrair_texto_url, AzureChatOpenAI

# Carregar variáveis do arquivo .env
from dotenv import load_dotenv

load_dotenv()

# Configuração do cliente AzureChatOpenAI
client = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
)

def translate_article(text, lang):
    messages = [
        ("system", "Você é um tradutor de texto profissional"),
        ("user", f"Traduza o seguinte texto para o idioma {lang} e responda em markdown: {text}")
    ]

    response = client.invoke(messages)
    return response.content

def salvar_como_markdown(texto, nome_arquivo="artigo_traduzido.md"):
    """Salva o texto traduzido em um arquivo Markdown."""
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\nArquivo salvo como: {nome_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    # Solicitar a URL do usuário
    url = input("Informe a URL que deseja extrair e traduzir: ").strip()
    
    # Validar a URL
    if not url.startswith("http"):
        print("Por favor, insira uma URL válida (começando com http ou https).")
    else:
        text = extrair_texto_url(url)
        if text:
            lang = input("Informe o idioma para tradução (exemplo: pt-br, en, es): ").strip()
            article = translate_article(text, lang)
            print("\n--- Artigo Traduzido ---\n")
            print(article)
            
            # Solicitar o nome do arquivo para salvar
            nome_arquivo = input("Digite o nome do arquivo para salvar (sem extensão, ou pressione Enter para 'artigo_traduzido'): ").strip()
            if not nome_arquivo:
                nome_arquivo = "artigo_traduzido"
            salvar_como_markdown(article, f"{nome_arquivo}.md")
        else:
            print("Não foi possível extrair o texto da URL fornecida.")
