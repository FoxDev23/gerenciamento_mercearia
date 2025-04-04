from Models import Categoria, Estoque, Produtos, Fornecedor, Pessoa, Funcionario, Vendas
from Dao import DaoVenda, DaoEstoque, DaoFornecedor, DaoPessoa, DaoFuncionario, DaoCategoria
from datetime import datetime

class ControleCategoria:
    def cadastrarCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True

        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('Essa categoria já existe no sistema.')

    def removerCategoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print('A categoria que deseja remover não existe')
        else:
            for i in range(len(x)):
                if x[1].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso.')
            # Produtos que estavam no estoque com a categoria que foi removida, devem passar para a situação de "Sem Categoria"

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

        estoque = DaoEstoque.ler()

        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade) 
                           if(x.produto.categoria == categoriaRemover) else (x), estoque))

        with open('estoque.txt','w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')  

    def alterarCategoria(self, categoriaAlterar, categoriaModificada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaModificada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaModificada) if(x.categoria == categoriaAlterar) else(x), x))
                print('Categoria alterada com sucesso.')
                # Produtos que estavam no estavam no estoque com a categoria que foi alterada, devem ter a situação atualizada simultaneamente.

            else:
                print('A categoria para a qual deseja alterar já existe.')
        else:
            print('A categoria que deseja alterar não existe.')

        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

        estoque = DaoEstoque.ler()

        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaModificada), x.quantidade) 
                           if(x.produto.categoria == categoriaAlterar) else (x), estoque))

        with open('estoque.txt','w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')  

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Não existem categorias registradas no sistema.')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')

class ControleEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        catg = list(filter(lambda x: x.categoria == categoria, y))
        estq = list(filter(lambda x: x.produto.nome == nome, x))

        if len(catg) > 0:
            if len(estq) == 0:
               produto = Produtos(nome, preco, categoria)
               DaoEstoque.salvar(produto, quantidade)
               print("Produto cadastrado com sucesso.")
            else:
                print("Produto já existente no estoque.")
        else:
            print("Categoria inexistente.")

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        estq = list(filter(lambda x: x.produto.nome == nome, x))
        if len(estq) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('Produto removido com sucesso.')
        else:
            print('O produto que deseja remover não existe.')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        catg = list(filter(lambda x: x.categoria == novaCategoria, y))
        if len(catg) > 0:
            estq = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(estq) > 0:
                estq = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(estq) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), x))
                    print('Produto alterado com sucesso.')
                else:
                    print('Produto já cadastrado.')
            else:
                print('O produto que deseja alterar não existe.')

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                    arq.writelines('\n')
        else:
            print('A categoria informada não existe.')

    def mostrarProduto(self):
        estq = DaoEstoque.ler()
        if len(estq) == 0:
            print('Estoque vazio.')
        else:
            print('===============Produto===============')
            for i in estq:
                
                print(f'Nome: {i.produto.nome}\n'
                      f'Preço: {i.produto.preco}\n'
                      f'Categoria: {i.produto.categoria}\n'
                      f'Quantidade: {i.quantidade}')
                
                print('--------------------------------------')

class ControleVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Vendas(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)

                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])

            arq = open('estoque.txt', 'w')
            arq.write("")

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i[0].nome + "|" + i[0].preco + "|" + i[0].categoria + "|" + str(i[1]))
                arq.writelines('\n')

        if existe == False:
            print('O produto não existe')
            return None
        elif not quantidade:
            print('Quantidade insuficiente no estoque.')
            return None
        else:
            print('Venda realizada com sucesso.')
            return valorCompra

    def relatorioProdutos(self):
        vendas = DaoVenda.ler()
        produtos = []
        
        for i in vendas:
            nome = i.itensVendidos.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)} if (x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esses são os produtos mais vendidos.\n')
        a = 1
        for i in ordenado:
            print(f'====================Produto [{a}]=====================')
            print(f"Produto: {i['produto']}\n"
                    f"Quantidade: {i['quantidade']}\n")
            a += 1

    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataTermino = datetime.strptime(dataTermino, '%d/%m/%Y')

        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y') >= dataInicio and datetime.strptime(x.data, '%d/%m/%Y') <= dataTermino, vendas))

        cont = 1
        total = 0
        for i in vendasSelecionadas:
            print(f'===============Venda [{cont}]===============')
            print(f'Nome: {i.itensVendidos.nome}\n'
            f'Categoria: {i.itensVendidos.categoria}\n'
            f'Data: {i.data}\n'
            f'Quantidade: {i.quantidadeVendida}\n'
            f'Cliente: {i.comprador}\n'
            f'Vendedor: {i.vendedor}')

            total += int(i.itensVendidos.preco) * int(i.quantidadeVendida)
            cont += 1

        print(f'Total Vendido: {total}')

class ControleFornecedor:
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        listaCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listaTelefone = list(filter(lambda x: x.cnpj == cnpj, x))
        if len(listaCnpj) > 0:
            print('CNPJ já cadastrado no sistema.')
        elif len(listaTelefone) > 0:
            print('Telefone já cadastrado no sistema.')
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
            else:
                print('Digite um CNPJ ou telefone válido.')

    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novoCategoria):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            est = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len(est) == 0:
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novoCategoria) if(x.nome == nomeAlterar) else(x), x))
            else:
                print("CNPJ já existente no sistema.")
        else:
            print("O fornecedor que deseja alterar não está cadastrado no sistema.")
        
        with open('fornecedores.txt','w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print("Fornecedor alterado com sucesso.")

    def removerFornecedor(self, nome):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O fornecedor que deseja remover não existe.')
            return None
        
        with open ('fornecedores.txt','w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor removido com sucesso.')

    def mostrarFornecedores(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) == 0:
            print('Lista de fornecedores vazia.')

        for i in fornecedores:
            print('===============Fornecedores===============')
            print(f'Categoria Fornecida: {i.categoria}\n'
                  f'Nome: {i.nome}\n'
                  f'Telefone: {i.telefone}\n'
                  f'Cnpj: {i.cnpj}')

class ControleCliente:
    def cadastrarCliente(self, nome, cpf, telefone, email, endereco):
        x = DaoPessoa.ler()
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        if len(listaCpf) > 0:
            print('CPF já cadastrado no sistema.')
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoPessoa.salvar(Pessoa(nome, cpf, telefone, email, endereco))
            else:
                print('Digite um CPF ou telefone válido.')

    def alterarCliente(self, nomeAlterar, novoNome, novoCpf, novoTelefone, novoEmail, novoEndereco):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
                x = list(map(lambda x: Pessoa(novoNome, novoCpf, novoTelefone, novoEmail, novoEndereco) if(x.nome == nomeAlterar) else(x), x))
            
        else:
            print("O cliente que deseja alterar não está cadastrado no sistema.")
        
        with open('clientes.txt','w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cpf + "|" + i.telefone + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print("Cliente alterado com sucesso.")

    def removerCiente(self, nome):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O cliente que deseja remover não existe.')
            return None
        
        with open ('clientes.txt','w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cpf + "|" + i.telefone + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente removido com sucesso.')

    def mostrarClientes(self):
        clientes = DaoPessoa.ler()
        if len(clientes) == 0:
            print('Lista de clientes vazia.')

        for i in clientes:
            print('===============Clientes===============')
            print(f'Nome: {i.nome}\n'
                  f'Telefone: {i.telefone}\n'
                  f'Cpf: {i.cpf}\n'
                  f'Email: {i.email}\n'
                  f'Endereço: {i.endereco}')

class ControleFuncionario:
    def cadastrarFuncionario(self, clt, nome, cpf, telefone, email, endereco):
        x = DaoFuncionario.ler()
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))
        if len(listaCpf) > 0:
            print('CPF já cadastrado no sistema.')
        elif len(listaClt) > 0:
            print("Já existe um funcionário com essa clt.")
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoFuncionario.salvar(Pessoa(clt, nome, cpf, telefone, email, endereco))
            else:
                print('Digite um CPF ou telefone válido.')

    def alterarFuncionario(self, nomeAlterar, novoNome, novoClt, novoCpf, novoTelefone, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
                x = list(map(lambda x: Funcionario(novoNome, novoClt, novoCpf, novoTelefone, novoEmail, novoEndereco) if(x.nome == nomeAlterar) else(x), x))   
        else:
            print("O funcionário que deseja alterar não está cadastrado no sistema.")
        
        with open('funcionarios.txt','w') as arq:
            for i in x:
                arq.writelines(i.clt + "|" + i.nome + "|" + i.cpf + "|" + i.telefone + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print("Funcionário alterado com sucesso.")

    def removerFuncionario(self, nome):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O funcionário que deseja remover não existe.')
            return None
        
        with open ('funcionarios.txt','w') as arq:
            for i in x:
                arq.writelines(i.clt + "|" + i.nome + "|" + i.cpf + "|" + i.telefone + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Funcionário removido com sucesso.')

    def mostrarFuncionarios(self):
        funcionarios = DaoFuncionario.ler()
        if len(funcionarios) == 0:
            print('Lista de funcionários vazia.')

        for i in funcionarios:
            print('===============Funcionários===============')
            print(f'Clt: {i.clt}\n'
                  f'Nome: {i.nome}\n'
                  f'Telefone: {i.telefone}\n'
                  f'Cpf: {i.cpf}\n'
                  f'Email: {i.email}\n'
                  f'Endereço: {i.endereco}')
            
