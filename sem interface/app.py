# Importação da biblioteca necessária
import os

# Criação de um (Dicionário) com os restaurantes
restaurantes = [
                    {'nome':'Praça','categoria':'Japonesa','ativo':False},
                    {'nome':'Pizza suprema','categoria':'Pizza','ativo':True},
                    {'nome':'Cantina','categoria':'Italiano','ativo':False}
                ]

def exibir_nome_do_programa():
    print("""
█▀ ▄▀█ █▄▄ █▀█ █▀█   █▀▀ ▀▄▀ █▀█ █▀█ █▀▀ █▀ █▀
▄█ █▀█ █▄█ █▄█ █▀▄   ██▄ █░█ █▀▀ █▀▄ ██▄ ▄█ ▄█
            """)
    
def exibir_opcoes():
    print('1. Cadastrar restaurante')
    print('2. Listar restaurante')
    print('3. Alterar estado do restaurante')
    print('4. Sair\n')

def finalizar_app():
    exibir_subtitulo('Finalizando o app\n')

def voltar_ao_menu_principal():
    input('\nDigite uma tecla para voltar ao menu principal')
    main()

def opcao_invalida():
    print('Opção inválida!\n')
    voltar_ao_menu_principal()

def exibir_subtitulo(texto):
    os.system('cls') #Limpa a tela
    # Cria uma linha de * com comprimento do texto
    linha = '*' * (len(texto))
    print(linha)
    print(texto)
    print(linha)
    print()

def cadastrar_novo_restaurante():
    # Função para cadastro de um novo restaurante

    exibir_subtitulo('Cadastro de novos restaurantes\n')

    # Coleta de informações
    nome_do_restaurante = input('Digite o nome do restaurante: ')
    categoria = input(f'Digite a categoria do restaurante {nome_do_restaurante}: ')
    dados_do_restaurante = {'nome' :nome_do_restaurante, 'categoria' :categoria, 'ativo':False}

    # Insere os dados coletados acima
    restaurantes.append(dados_do_restaurante)

    # Retorno para o usuário
    print(f'O restaurante {nome_do_restaurante} foi cadastrado com sucesso! ')

    voltar_ao_menu_principal()

def listar_restaurantes():
    # Função para listar os restaurantes

    exibir_subtitulo('Listando os restaurantes\n')

    # Cabeçalho alinhado a esquerda (l.just)
    print(f'{'nome_restaurante'.ljust(21)} | {'categoria'.ljust(20)} | Status')

    # Laço para exibir os restaurantes
    for restaurante in restaurantes:
        nome_restaurante = restaurante['nome']
        categoria = restaurante['categoria']
        ativo ='ativado' if restaurante['ativo'] else 'desativado'
        print(f'-{nome_restaurante.ljust(20)} | {categoria.ljust(20)} | {ativo}')

    voltar_ao_menu_principal()

def alternar_estado_do_restaurante():
    """
    Função para ativar ou desativar um restaurante
    """
    exibir_subtitulo('Alternando estado do restaurante\n')
    nome_restaurante = input('Digite o nome do restaurante que deseja alterar o estado: ')
    restaurante_encontrado = False

    for restaurante in restaurantes:
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True
            restaurante['ativo'] = not restaurante['ativo']  # Inverte o estado (Ex. False para True)
            mensagem = f'O restaurante {nome_restaurante} foi ativado com sucesso!' if restaurante['ativo'] else f'O restaurante {nome_restaurante} foi desativado com sucesso!'
            print(mensagem)
            
    if not restaurante_encontrado:
        print('O restaurante não foi encontrado!')

    voltar_ao_menu_principal()

def escolher_opcao():
    """
        Função para escolha do usuário
    """
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))

        if opcao_escolhida == 1:
            # print('Opção 1 escolhida!\n')
            cadastrar_novo_restaurante()
            # voltar_ao_menu_principal()
        elif opcao_escolhida == 2:
            # print('Opção 2 escolhida!\n')
            listar_restaurantes()
            # voltar_ao_menu_principal()
        elif opcao_escolhida == 3:
            # print('Opção 3 escolhida!\n')
            alternar_estado_do_restaurante()
            # voltar_ao_menu_principal()
        elif opcao_escolhida == 4:
            finalizar_app()
        else:
            opcao_invalida()
    except:
        opcao_invalida()

def main():
    """
        Função para iniciar o programa
    """
    os.system('cls')
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__== '__main__':
    main()