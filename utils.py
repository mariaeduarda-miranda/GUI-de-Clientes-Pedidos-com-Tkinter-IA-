import re
import logging
import os
import requests  # Certifique-se de instalar: pip install requests
import json
import time
import random

# Configuração de Logs
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_acao(mensagem):
    logging.info(mensagem)
    print(f"LOG: {mensagem}")

def validar_nome(nome):
    """Valida se o nome é obrigatório e contém apenas letras e espaços """
    # 1. Checa se está vazio
    if not nome or nome.strip() == "":
        return False, "O nome do cliente é obrigatório e não pode estar vazio"

    # 2. Checa se contém caracteres que não são letras, espaços, acentos ou hífens
    # \D -> Qualquer caractere que NÃO é dígito. Se acharmos um dígito, o nome não é válido (a menos que seja um nome composto por letras/espaços)
    # Vamos simplificar para garantir que não haja apenas números.
    if nome.strip().isdigit():
        return False, "O nome não pode consistir apenas em números."

    return True, ""

def validar_email(email):
    """Valida o formato simples de e-mail."""
    if not email or email.strip() == "":
        return True, ""

    # Padrão: qualquer caractere (exceto espaço) + @ + qualquer caractere + . + 2 a 4 letras
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"


    if re.fullmatch(padrao, email.strip()):
        return True, ""

    return False, "Formato de e-mail inválido (ex: nome@dominio.com)."

def validar_telefone(telefone):
    """Valida se o telefone tem entre 8 e 15 dígitos numéricos."""
    if not telefone or telefone.strip() == "":
        return True, ""  # Telefone opcional, se estiver vazio, é válido

    # Remove todos os caracteres não numéricos
    nums = re.sub(r'\D', '', telefone)

    # Requisito: telefone com 8-15 dígitos
    if 8 <= len(nums) <= 15:
        return True, ""

    return False, "O telefone deve conter entre 8 e 15 dígitos numéricos."

def analisar_pedidos_ia(texto_pedidos):
    """
    Envia os dados para o Ollama rodando localmente.
    """
    url = "http://localhost:11434/api/generate"

    prompt_sistema = (
        "Você é um analista de vendas experiente. "
        "Analise a lista de pedidos abaixo e forneça um resumo curto contendo: "
        "1) Produtos mais vendidos, 2) Ticket médio aproximado e 3) Uma sugestão de negócio. "
        "Seja direto e use tópicos."
    )

    payload = {
        "model": "llama3",  # <--- MUDE AQUI SE USAR OUTRO MODELO (ex: "mistral")
        "prompt": f"{prompt_sistema}\n\nDADOS DOS PEDIDOS:\n{texto_pedidos}",
        "stream": False
    }

    try:
        log_acao("Enviando dados para o Ollama local...")
        response = requests.post(url, json=payload, timeout=60)  # Timeout de 60s para a IA pensar

        if response.status_code == 200:
            resultado = response.json()
            resposta_ia = resultado.get('response', 'Sem resposta do modelo.')
            return f"--- Análise do Ollama ---\n{resposta_ia}"
        else:
            return f"Erro no Ollama: Código {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return (
            "Erro: Não foi possível conectar ao Ollama.\n"
            "Verifique se ele está rodando (comando: 'ollama serve')\n"
            "e se o modelo está baixado."
        )
    except Exception as e:
        log_acao(f"Erro IA: {e}")
        return f"Erro inesperado: {e}"