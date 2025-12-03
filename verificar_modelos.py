import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega a chave
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")

if not chave:
    print("ERRO: Chave não encontrada no arquivo .env")
else:
    print(f"Chave carregada: {chave[:5]}... (oculto)")
    
    # Configura o Google
    genai.configure(api_key=chave)

    print("\n--- MODELOS DISPONÍVEIS PARA VOCÊ ---")
    try:
        # Lista todos os modelos que servem para gerar texto
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Nome: {m.name}")
                
    except Exception as e:
        print(f"\nERRO FATAL AO CONECTAR: {e}")
        print("Dica: Verifique se sua chave API está ativa no Google AI Studio.")