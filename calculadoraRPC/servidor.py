from xmlrpc.server import SimpleXMLRPCServer

def soma(num1, num2):
    return num1 + num2

def subtracao(num1, num2):
    return num1 - num2

def multiplicacao(num1, num2):
    return num1 * num2

def divisao(num1, num2):
    if num2 == 0:
        return "Não é possível dividir por zero"
    return num1 / num2

server = SimpleXMLRPCServer(("localhost", 8080))
print("Servidor está rodando na porta 8080!")
server.register_function(soma, "soma")
server.register_function(subtracao, "subtracao")
server.register_function(multiplicacao, "multiplicacao")
server.register_function(divisao, "divisao")

server.serve_forever()