import os

def ler_arquivo_texto(caminho_arquivo):
    """
    Lê um arquivo .txt e retorna o conteúdo como string.
    """
    if not os.path.exists(caminho_arquivo):
        return "Erro: Arquivo não encontrado. Verifique o nome."
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"