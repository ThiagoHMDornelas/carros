from google import genai
from dotenv import load_dotenv
import os


# Carrega as variáveis do arquivo .env
load_dotenv()


def get_car_gemini_bio(model, brand, year):
    # Inicializa cliente usando variável de ambiente
    # client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Pega a chave da variável de ambiente
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

    # Inicializa cliente com a chave segura
    client = genai.Client(api_key=api_key)

    message = ''''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year)

    # Faz uma requisição simples
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # modelo gratuito recomendado
        contents=message
    )

    return response.text.replace("## Descrição de Venda (250 caracteres)", "").strip()
