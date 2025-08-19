import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from functools import partial
import os 
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para dev e para o PyInstaller"""
    try:
        # PyInstaller cria um diretorio temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Caso não esteja usando PyInstaller usa o caminho atual do diretório
        base_path = os.path.abspath(".")

    # Retorna o caminho completo para o recurso
    return os.path.join(base_path, relative_path)

class Calculadora:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ttk.Window(themename="darkly") # Cria a janela principal usando ttkbootstrap
        self.janela.geometry('400x750') # Define o tamanho da janela
        self.janela.title('Calculadora SENAI') # Define o título

        # Definição de cores e fonte
        self.cor_fundo = 'black' # cor de fundo da interface
        self.cor_botao = 'secondary' # cor dos botões numériocos e de ponto
        self.cor_texto = 'white' # cor do texto
        self.cor_operacao = 'warning' # Cor do botões de operadores
        self.fonte_padrao = ('Roboto', 18) # fonte padrão dos botões
        self.fonte_display = ('Roboto', 36) # fonte do display

        # Cnofiguração do ícone da janela
        icon_path = resource_path("calc.ico") # Obtem o caminho do icone
        self.janela.iconbitmap(icon_path) # Define o icone da janela

        # Frame para o display
        self.frame_display = ttk.Frame(self.janela) # Cria um frame para o display
        self.frame_display.pack(fill='both', expand=True) # Adiciona o frame ao layout da janela

        # Display para os cálculos
        self.display = ttk.Label(
            self.frame_display,
            text='',
            font=self.fonte_display,
            anchor='e', # Aliha o texto à direita
            padding=(20, 10) # Adciiona um preenchimento interno ao rótulo
        )
        self.display.pack(fill='both', expand=True) # Adiciona o display ao frame

        # Frame para os botões
        self.frame_botoes = ttk.Frame(self.janela) # Cria um frame para os botões
        self.frame_botoes.pack(fill='both', expand=True)

        # Configuração dos botões
        self.botoes = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        # Criação dos botões
        for i, linha in enumerate(self.botoes): # Itera sobre a linha
            for j, texto in enumerate(linha): # Itera sobre os botões em cada linha
                estilo = 'warning.TButton' if texto in ['C', '⌫', '^', '/', 'x', '+', '-', '='] else 'secondary.TButton'
                botao = ttk.Button(
                    self.frame_botoes,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto)
                )
                botao.grid(row=i, column=j, padx=1, pady=1, sticky='nsew') # Adiciona o botão ao grid

        # Configura o redimensionamento das linhas e colunas
        for i in range(5):
            self.frame_botoes.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.frame_botoes.grid_columnconfigure(i, weight=1)

        # Frame para a imagem SENAI
        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill='both', expand=True, pady=10)

        # Carregando e exibindo a imagem SENAI
        imagem_path = resource_path("Senai.png")
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((300, 100), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)

        label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")
        label_imagem.image = imagem_tk
        label_imagem.pack()

        # Frame para o seletor de temas
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        # Label "Escolher Tema:"
        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        # Seletor de temas (ComboBox)
        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        self.selector_tema = ttk.Combobox(self.frame_tema, values=self.temas, state='readonly')
        self.selector_tema.set('darkly') # Define como padrão
        self.selector_tema.pack(side='top', fill='x')
        self.selector_tema.bind('<<ComboboxSelected>>', self.mudar_tema)

        # Inicia a janela principal
        self.janela.mainloop() # Inicia o loop principal de interface gráfica

    def mudar_tema(self, evento):
        """Muda o tema da aplicação"""
        novo_tema = self.selector_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        """Interpreta o botão pressionado e ataliza o display"""
        texto_atual = self.display.cget("text") # Obtem o texto atual do display

        if (valor == 'C'):
            # Limpa display
            self.display.configure(text='')
        elif (valor == '⌫'):
            # Apaga o útilmo carectere do display
            self.display.configure(text=texto_atual[:-1])
        elif (valor == '='):
            # Calcula o resultado da expressão
            self.calcular()
        elif (valor == '()'):
            # Adiciona parênteses ao display dependedo do contexto
            if not texto_atual or texto_atual[-1] in '+-/^x':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1] in '0123456789)':
                self.display.configure(text=texto_atual + ')')
        else:
            # Adiciona o valor do botão pressionado ao display
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        """ Realiza o cálculo da expressão no display """
        expressao = self.display.cget("text") # Obtém a espressão do display
        expressao = expressao.replace('x', '*').replace('^', '**')

        try:
            # Avalia a expressão e exibe o resultado
            resultado = eval(expressao)
            self.display.configure(text=str(resultado))
        except:
            # Exibe uma mensagem de erro caso a avaliação falhe
            self.display.configure(text="Erro")

# Inicia a aplicação
if __name__ == "__main__":
    Calculadora()
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from functools import partial
import os 
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para dev e para o PyInstaller"""
    try:
        # PyInstaller cria um diretorio temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Caso não esteja usando PyInstaller usa o caminho atual do diretório
        base_path = os.path.abspath(".")

    # Retorna o caminho completo para o recurso
    return os.path.join(base_path, relative_path)

class Calculadora:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ttk.Window(themename="darkly") # Cria a janela principal usando ttkbootstrap
        self.janela.geometry('400x750') # Define o tamanho da janela
        self.janela.title('Calculadora SENAI') # Define o título

        # Definição de cores e fonte
        self.cor_fundo = 'black' # cor de fundo da interface
        self.cor_botao = 'secondary' # cor dos botões numériocos e de ponto
        self.cor_texto = 'white' # cor do texto
        self.cor_operacao = 'warning' # Cor do botões de operadores
        self.fonte_padrao = ('Roboto', 18) # fonte padrão dos botões
        self.fonte_display = ('Roboto', 36) # fonte do display

        # Cnofiguração do ícone da janela
        icon_path = resource_path("calc.ico") # Obtem o caminho do icone
        self.janela.iconbitmap(icon_path) # Define o icone da janela

        # Frame para o display
        self.frame_display = ttk.Frame(self.janela) # Cria um frame para o display
        self.frame_display.pack(fill='both', expand=True) # Adiciona o frame ao layout da janela

        # Display para os cálculos
        self.display = ttk.Label(
            self.frame_display,
            text='',
            font=self.fonte_display,
            anchor='e', # Aliha o texto à direita
            padding=(20, 10) # Adciiona um preenchimento interno ao rótulo
        )
        self.display.pack(fill='both', expand=True) # Adiciona o display ao frame

        # Frame para os botões
        self.frame_botoes = ttk.Frame(self.janela) # Cria um frame para os botões
        self.frame_botoes.pack(fill='both', expand=True)

        # Configuração dos botões
        self.botoes = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        # Criação dos botões
        for i, linha in enumerate(self.botoes): # Itera sobre a linha
            for j, texto in enumerate(linha): # Itera sobre os botões em cada linha
                estilo = 'warning.TButton' if texto in ['C', '⌫', '^', '/', 'x', '+', '-', '='] else 'secondary.TButton'
                botao = ttk.Button(
                    self.frame_botoes,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto)
                )
                botao.grid(row=i, column=j, padx=1, pady=1, sticky='nsew') # Adiciona o botão ao grid

        # Configura o redimensionamento das linhas e colunas
        for i in range(5):
            self.frame_botoes.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.frame_botoes.grid_columnconfigure(i, weight=1)

        # Frame para a imagem SENAI
        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill='both', expand=True, pady=10)

        # Carregando e exibindo a imagem SENAI
        imagem_path = resource_path("Senai.png")
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((300, 100), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)

        label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")
        label_imagem.image = imagem_tk
        label_imagem.pack()

        # Frame para o seletor de temas
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        # Label "Escolher Tema:"
        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        # Seletor de temas (ComboBox)
        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        self.selector_tema = ttk.Combobox(self.frame_tema, values=self.temas, state='readonly')
        self.selector_tema.set('darkly') # Define como padrão
        self.selector_tema.pack(side='top', fill='x')
        self.selector_tema.bind('<<ComboboxSelected>>', self.mudar_tema)

        # Inicia a janela principal
        self.janela.mainloop() # Inicia o loop principal de interface gráfica

    def mudar_tema(self, evento):
        """Muda o tema da aplicação"""
        novo_tema = self.selector_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        """Interpreta o botão pressionado e ataliza o display"""
        texto_atual = self.display.cget("text") # Obtem o texto atual do display

        if (valor == 'C'):
            # Limpa display
            self.display.configure(text='')
        elif (valor == '⌫'):
            # Apaga o útilmo carectere do display
            self.display.configure(text=texto_atual[:-1])
        elif (valor == '='):
            # Calcula o resultado da expressão
            self.calcular()
        elif (valor == '()'):
            # Adiciona parênteses ao display dependedo do contexto
            if not texto_atual or texto_atual[-1] in '+-/^x':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1] in '0123456789)':
                self.display.configure(text=texto_atual + ')')
        else:
            # Adiciona o valor do botão pressionado ao display
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        """ Realiza o cálculo da expressão no display """
        expressao = self.display.cget("text") # Obtém a espressão do display
        expressao = expressao.replace('x', '*').replace('^', '**')

        try:
            # Avalia a expressão e exibe o resultado
            resultado = eval(expressao)
            self.display.configure(text=str(resultado))
        except:
            # Exibe uma mensagem de erro caso a avaliação falhe
            self.display.configure(text="Erro")

# Inicia a aplicação
if __name__ == "__main__":
    Calculadora()