from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Historico:
    def __init__(self) :
        self._transacoes=[]
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo":transacao.__class__.__name__,
                "valor":transacao.valor,
                "data":datetime.now().strftime("%d/%m/%Y -- %H:%M:%s"),
            }
        )
            
class Conta:
    def __init__(self, numero, cliente) :
        self._saldo  = 0
        self._numero = numero
        self._agencia='0001'
        self._cliente=cliente
        self._historico=Historico()
        
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo = self.saldo
        if valor >saldo:
            print('\nOperação falhou! \nVocê não tem saldo suficiente!')
        elif valor > 0:
            self._saldo -=valor
            print('\nSaque realizado com sucesso!!')
            return True
        else:
            print('\n Operação falhou!!\nO valor informado é inválido!')
            return False
        
    def depositar(self, valor):
        if valor >0:
            self._saldo+=valor
            print('\nDepósito realizado com sucesso!!')
        else:
            print('\nOperação falhou!\nO valor informado é inválido!!')
            return False
        return True
            
class Cliente:
    def __init__(self, endereco):
        self.endereco=endereco
        self.contas =[]    
    def realizar_transacao(self, conta ,transacao ):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, nome,data_nascimento,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
    
class Transacao(ABC):
     @property
     @abstractproperty
     def valor(self):
         pass
     @abstractclassmethod
     def registrar(self, conta):
         pass

class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques=limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.trasacoes if transacao['tipo']==Saque.__name__]
        )
        excedeu_limite = valor>self.limite
        excedeu_saques = numero_saques>=self.limite_saques
        if excedeu_limite:
            print('\nOperação falhou! \nO valor do saque excede o limite!')
        elif excedeu_saques:
            print('\nOperação falhou! \nNúmero máximo de saques atingido!')
        else:
            return super().sacar(valor)
        
        return False
    def __str__(self):
        return f""" \
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """
        
        
class Saque(Transacao):
    def __init__(self, valor) :
        self._valor=valor
    
    @property
    def valor(self):
        return self._valor
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor) :
            self._valor=valor
    
    @property
    def valor(self):
        return self._valor
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

