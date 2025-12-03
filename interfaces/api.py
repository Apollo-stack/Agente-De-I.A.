from flask import Flask, request, jsonify
import sys
import os
import requests
from dotenv import load_dotenv

# 1. Configurações
load_dotenv()
PIPEDRIVE_TOKEN = os.getenv("PIPEDRIVE_TOKEN")
PIPEDRIVE_DOMAIN = os.getenv("PIPEDRIVE_DOMAIN")

app = Flask(__name__)

# 2. Caminhos e IA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.agent import AgentIA

print("Carregando IA...")
try:
    # Usando gemini-pro que é o estável
    minha_ia = AgentIA(modelo="gemini-2.5-flash") 
    minha_ia.definir_persona("Você é um gerente de vendas sênior. Dê dicas táticas e curtas.")
    print("✅ IA Pronta!")
except Exception as e:
    print(f"❌ Erro na IA: {e}")

# 3. Função de Salvar
def salvar_nota_pipedrive(deal_id, conteudo):
    if not PIPEDRIVE_TOKEN or not PIPEDRIVE_DOMAIN:
        print("⚠️ Token do Pipedrive não configurado.")
        return

    url = f"https://{PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/notes?api_token={PIPEDRIVE_TOKEN}"
    payload = {
        "deal_id": deal_id,
        "content": f"🤖 <b>Análise da IA:</b><br>{conteudo.replace('\n', '<br>')}"
    }
    requests.post(url, json=payload)

# 4. A Rota Corrigida
@app.route('/analisar_lead', methods=['POST'])
def receber_pedido():
    dados = request.json
    print(f"\n📦 DADOS RECEBIDOS: {dados}\n") # Debug mantido

    if not dados:
        return jsonify({"erro": "Sem dados"}), 400

    # --- A CORREÇÃO ESTÁ AQUI EMBAIXO ---
    # O código agora procura por 'data' (o que você recebeu) OU 'current' (padrão antigo)
    # Assim ele funciona em qualquer situação.
    
    info_negocio = dados.get('data') or dados.get('current')

    if info_negocio:
        # É o Pipedrive falando!
        deal_id = info_negocio.get('id')
        nome_cliente = info_negocio.get('title')
        valor = info_negocio.get('value', 0)
        observacoes = f"Cliente: {nome_cliente}. Valor da oportunidade: {valor}"
    else:
        # É seu teste manual (PowerShell)
        deal_id = None
        nome_cliente = dados.get('nome')
        observacoes = dados.get('obs')

    print(f"🚀 Processando estratégia para: {nome_cliente}...")

    # A IA pensa
    resposta = minha_ia.pensar(
        f"Analise este negócio e sugira 3 passos táticos para fechar a venda: {nome_cliente}", 
        contexto_extra=observacoes
    )

    # Salva no Pipedrive
    if deal_id:
        salvar_nota_pipedrive(deal_id, resposta)
        print(f"✅ Nota salva no negócio {deal_id}!")

    return jsonify({"status": "sucesso", "dica": resposta})

if __name__ == '__main__':
    app.run(port=5000)