from openai import OpenAI
from dotenv import load_dotenv
import os


# Carrega as variáveis do arquivo .env
load_dotenv()


def get_car_openai_bio(model, brand, year):
    # Pega a chave da variável de ambiente
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

    # Inicializa cliente com a chave segura
    client = OpenAI(api_key=api_key)

    message = ''''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year)
    response = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': message
            }
        ],
        max_tokens=1000,
        model='gpt-3.5-turbo',
    )

    return response.choices[0].message.content
