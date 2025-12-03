from core.agent import AgentIA
from tools.file_reader import ler_arquivo_texto

def main():
    print("--- INICIANDO AGENTE ---")

    # Tenta criar a IA
    try:
        minha_ia = AgentIA()
    except Exception as e:
        print(f"Ops! Deu erro ao criar a IA: {e}")
        return

    # Define que ela é especialista em Vendas
    minha_ia.definir_persona("Você é um gerente comercial experiente e direto.")

    # 1. Teste Básico
    print("\n--- Teste 1: Pergunta Simples ---")
    resp = minha_ia.pensar("Diga uma frase motivacional curta para vendedores.")
    print(f"IA: {resp}")

    # 2. Teste com Contexto (Simulando um lead do Pipedrive)
    print("\n--- Teste 2: Lendo Arquivo ---")
    
    # Criando um arquivo de teste na hora
    with open("lead_teste.txt", "w", encoding="utf-8") as f:
        f.write("Nome: João Silva\nEmpresa: Padaria do João\nDor: Precisa vender mais pão online, mas não sabe usar computador.")
    
    # Lendo o arquivo
    dados = ler_arquivo_texto("lead_teste.txt")
    
    # Perguntando para a IA com base no arquivo
    resp_contexto = minha_ia.pensar("Como eu vendo um software de CRM para esse cliente?", contexto_extra=dados)
    print(f"IA Sugere: {resp_contexto}")

if __name__ == "__main__":
    main()