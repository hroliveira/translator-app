import requests
from bs4 import BeautifulSoup

class AzureChatOpenAI:
    def __init__(self, azure_endpoint, api_key, api_version, deployment_name, max_retries=0):
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.deployment_name = deployment_name
        self.max_retries = max_retries

    def invoke(self, messages):
        # Implementação da API de chamada
        pass

def extrair_texto_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        texto = soup.get_text(separator=' ')
        linhas = (line.strip() for line in texto.splitlines())
        parts = (phrase.strip() for line in linhas for phrase in line.split(" "))
        texto_limpo = '\n'.join(part for part in parts if part)
        return texto_limpo
    else:
        print(f"Failed to fetch the URL. Status Code: {response.status_code}")
        return None
