import textwrap

import agencia


def menu():
    menu = '''\n
    ------------- MENU ---------------
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNova conta
    [l]\tListar contas
    [u]\tNovo usuário
    [q]\tSair
    '''
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados= [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
     if not cliente.contas:
         print('\nCliente não possui conta!!')
         return
     return cliente.contas[0]
 
def depositar(clientes):
     cpf = input('Informe o CPF do cliente: ')
     cliente = filtrar_cliente(cpf, clientes)
     
     if not cliente:
         print("\nCliente não encontrado!")
         return
     
     valor = float(input('Informe o valor do depósito: '))
     transacao= agencia.Deposito(valor)
     conta = recuperar_conta_cliente(cliente)
     if not conta:
         return
     cliente.realizar_transacao(conta, cliente)
  
def sacar(clientes):
     cpf = input('Informe o CPF do cliente: ')
     cliente = filtrar_cliente(cpf, clientes)
     
     if not cliente:
         print("\nCliente não encontrado!")
         return
     
     valor = float(input('Informe o valor do saque: '))
     transacao= agencia.Saque(valor)
     cliente.realizar_transacao(conta, transacao)
     conta = recuperar_conta_cliente(cliente)
     if not conta:
         return
     
def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
     
    if not cliente:
        print("\nCliente não encontrado!")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
     
    print('\n ---------- EXTRATO ----------')
    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações!'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}'
    
    print(extrato)
    print('f\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('-------------------------------------------')
     
def criar_conta(numero_conta, contas, clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
     
    if not cliente:
      print("\nCliente não encontrado!\nFluxo de criação de conta encerrado!")
      return
    conta = agencia.Conta_Corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('\n Conta criada com sucesso!!')

def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente numeros): ')
    cliente = filtrar_cliente(cpf, clientes)
     
    if not cliente:
      print("\nCliente não encontrado!\nFluxo de criação de novo usuário encerrado!")
      return 
    nome = input('Informe o nome completo: ')
    data_nascimento =  input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço (logradouro,nro - bairro - cidade/UF)')
    cliente = agencia.Pessoa_Fisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print('\nCliente criado com sucesso!!')
    
def listar_contas(contas):
    for conta in contas:
        print('-'*100)
        print(textwrap.dedent(str(conta)))

def main():
    
    clientes = []
    contas =[]
    while True:
        opcao = menu()
        if opcao=='d':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao=='e':
            exibir_extrato(clientes)
        elif opcao == 'n':
            numero_conta = len(contas)+1
            criar_conta(numero_conta,clientes,contas)
        elif opcao == 'l':
            listar_contas(contas)
        elif opcao == 'u':
            criar_cliente(clientes)
        elif opcao == 'q':
            break
        else:
            print('\nOperação inválida, por favor selecione novamente a operação desejada.')
            
      
            
main()        
   
 

         
    