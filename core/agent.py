import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Carrega a chave do arquivo .env
load_dotenv()

class AgentIA:
    def __init__(self, modelo="gemini-2.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("ERRO: A chave GOOGLE_API_KEY não foi encontrada no arquivo .env")

        self.llm = ChatGoogleGenerativeAI(
            model=modelo,
            google_api_key=api_key,
            temperature=0.7
        )
        self.system_message = SystemMessage(content="Você é um assistente útil.")

    def definir_persona(self, texto_persona):
        self.system_message = SystemMessage(content=texto_persona)

    def pensar(self, pergunta_usuario, contexto_extra=None):
        messages = [self.system_message]

        if contexto_extra:
            msg_contexto = f"Use as informações abaixo como contexto:\n\n{contexto_extra}"
            messages.append(SystemMessage(content=msg_contexto))

        messages.append(HumanMessage(content=pergunta_usuario))

        try:
            resposta = self.llm.invoke(messages)
            return resposta.content
        except Exception as e:
            return f"Ocorreu um erro na IA: {e}"