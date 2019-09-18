import base64

def arquivoParaBase64(arquivo):
    with open(arquivo, "rb") as file:
        return base64.b64encode(file.read())