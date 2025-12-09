F = 20
SEPARADOR = "|"

REQUEST = 1
GRANT = 2
RELEASE = 3

def encode(tipo, processo_id):
    base = f"{tipo}{SEPARADOR}{processo_id}{SEPARADOR}"
    tam = F - len(base)
    padding = "0" * tam

    return (base + padding).encode("utf-8")

def decode(bytes_mensagem):
    mensagem = bytes_mensagem.decode("utf-8")
    partes = mensagem.split(SEPARADOR)
    tipo = int(partes[0])
    processo_id = int(partes[1])

    return tipo, processo_id
