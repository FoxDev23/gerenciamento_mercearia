import Controle
import os.path

def criarArquivos(*nome):
    for i in nome:
        if not os.path.exists(i):
            with open(i, "w") as arq:
                arq.write("")

criarArquivos('categoria.txt', 'clientes.txt', 'estoque.txt', 'fornecedores.txt', 'funcionarios.txt', 'venda.txt')