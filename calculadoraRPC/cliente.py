import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8080/")

num1 = float(input("Digite o primeiro numero: "))
num2 = float(input("Digite o segundo numero: "))


print(f"{num1} + {num2} = {proxy.soma(num1, num2)}")
print(f"{num1} - {num2} = {proxy.subtracao(num1, num2)}")
print(f"{num1} * {num2} = {proxy.multiplicacao(num1, num2)}")
print(f"{num1} / {num2} = {proxy.divisao(num1, num2)}")
