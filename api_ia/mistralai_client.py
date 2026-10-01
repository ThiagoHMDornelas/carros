import os

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()


def get_car_mistralai_bio(model, brand, year):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

    client = Mistral(api_key=api_key)

    message = ''''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year)

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": message,
            },
        ]
    )

    return chat_response.choices[0].message.content.replace("### **Descrição de Venda (250 caracteres)**", "").strip()
