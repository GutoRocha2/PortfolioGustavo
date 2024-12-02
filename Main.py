class Main:
    pass

print("Código teste")

from Cliente import Cliente
from Conta import Conta

cliente1 = Cliente("Joãozinho", 123456789100)
conta_cliente1 = Conta(cliente1.get_nome(), 6565)

conta_cliente1.deposita(100)
conta_cliente1.saque(50)
conta_cliente1.extrato()
