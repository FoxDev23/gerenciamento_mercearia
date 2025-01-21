from Models import *

class DaoCategoria:

    '''O @classmethod é um decorador no Python que transforma um método 
    em um método de classe. Diferentemente de um método de instância 
    (que recebe automaticamente a instância como o primeiro parâmetro, 
    geralmente chamado de self), um método de classe recebe a própria classe 
    como o primeiro parâmetro, geralmente chamado de cls.'''
    
    @classmethod
    def salvar(cls, categoria):
        with open("categoria.txt", 'a') as arq:
            arq.writelines(categoria)
            arq.writelines('\n')
