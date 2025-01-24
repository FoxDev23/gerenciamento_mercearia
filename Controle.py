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

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaModificada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaModificada, x))
            if len(cat) == 0:
                x = list(map(lambda x: Categoria(categoriaModificada) if(x.categoria == categoriaAlterar) else(x), x))


            else:
                print('A categoria que deseja alterar não existe.')
        else:
            print('A categoria que deseja alterar não existe.')