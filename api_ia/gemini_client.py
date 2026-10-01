import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_car_gemini_bio(model, brand, year):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

    client = genai.Client(api_key=api_key)

    message = ''''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message
    )

    return response.text.replace("## Descrição de Venda (250 caracteres)", "").strip()
