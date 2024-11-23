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
        """Envia mensagens para o endpoint do Azure OpenAI e retorna a resposta."""
        # URL para o endpoint específico do deployment
        #url = f"{self.azure_endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        url = f"{self.azure_endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"

        
        # Cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        # Corpo da requisição
        payload = {
            "messages": [{"role": role, "content": content} for role, content in messages],
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Levanta exceção se o status for 4xx ou 5xx
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar a API do Azure OpenAI: {e}")
            return None

def extrair_texto_url(url):
    """Extrai texto limpo de uma URL."""
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
