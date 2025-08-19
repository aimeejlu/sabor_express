# Usando biblioteca Tkinter (Padrão Python para interfaces)
import tkinter as tk

# Submódulo do Tkinter com widgets mais modernos e estilizados
from tkinter import ttk

# Biblioteca para trabalhar com imagens
from PIL import Image, ImageTk

# Variável para cor de fundo padrão
COR_FUNDO = "#c9c9c9"

# Dicionário para mapear nomes de cores em português para inglês/hex
cor_mapa = {
    "Vermelho": "#dc3545",
    "Azul": "#007bff",
    "Verde": "#28a745",
    "Amarelo": "#ffc107",
    "Preto": "black",
    "Branco": "white"
}

def atualizar_resultado():
    # Obter o texto da caixa de entrada
    nome = caixa_texto.get()

    # Obter a opção selecionada nos botões de rádio
    preferencia = var_radio.get()

    # Verificar se a caixa de seleção de saudação
    # informal esta marcada
    if var_check_saudacao.get():
        saudacao = "Olá"
    else:
        saudacao = "Bem-vindo"
    
    # Verificar se a caixa de seleção de saudação
    # personalizada esta marcada
    if var_check_personalizada.get():
        saudacao = f"{saudacao}, caro(a)"

    # Obter a cor favorita selecionada
    cor_favorita = combo_cor.get() 
    
    # Montar mensagem final
    mensagem = f"{saudacao} {nome}! Você prefere {preferencia}."
    if cor_favorita:
        mensagem += f" Sua cor favorita é {cor_favorita}."
    
    # Atualiza o texto e a cor do rótulo conforme a escolha do usuário (Cor)
    label_resultado.config(text=mensagem, foreground=cor_mapa.get(cor_favorita, '#343a40'))

def limpar_campos():
    # Limpa todas as escolhas
    caixa_texto.delete(0, tk.END)
    var_radio.set("Café")
    var_check_saudacao.set(False)
    var_check_personalizada.set(False)
    combo_cor.set("Escolha (sua cor)")
    # Ao limpar, o texto volta para a cor padrão
    label_resultado.config(text="", foreground='#343a40')

# Criar a janela principal
janela = tk.Tk()
janela.title("Interface avançada")
janela.geometry("400x500")
# Mudando cor de fundo da tela usando a variável
janela.config(bg=COR_FUNDO)

# Adicionando o ícone à janela
try:
    # A imagem 'senai.png' deve estar na mesma pasta do script.
    icone_senai = Image.open("senai.png")
    icone_senai_tk = ImageTk.PhotoImage(icone_senai)
    janela.iconphoto(True, icone_senai_tk)
except FileNotFoundError:
    print("Aviso: Arquivo 'senai.png' não encontrado. O ícone padrão será usado.")
except ImportError:
    print("Aviso: A biblioteca Pillow não está instalada. O ícone padrão será usado.")

# Criar uma caixa de entrada (Entry)
label_nome = tk.Label(janela, text="Digite seu nome:", bg=COR_FUNDO, fg="blue", font=("Arial", 14, "bold"))
label_nome.pack(pady=5)
caixa_texto = tk.Entry(janela, width=40)
caixa_texto.pack(pady=5)

# Criar botões de rádio
label_preferencia = tk.Label(janela, text=" Escolha sua preferência:", bg=COR_FUNDO)
label_preferencia.pack(pady=5)

var_radio = tk.StringVar(value="Café")
radio_cafe = tk.Radiobutton(janela, text="Café", variable=var_radio, value="Café", bg=COR_FUNDO)
radio_cha = tk.Radiobutton(janela, text="Chá", variable=var_radio, value="Chá", bg=COR_FUNDO)
radio_suco = tk.Radiobutton(janela, text="Suco", variable=var_radio, value="Suco", bg=COR_FUNDO)
radio_agua = tk.Radiobutton(janela, text="Água", variable=var_radio, value="Água", bg=COR_FUNDO)

# .pack (Método do Tkinter que
# deixa as opções visíveis)
radio_cafe.pack()
radio_cha.pack()
radio_suco.pack()
radio_agua.pack()

# Criar caixas de seleção múltipla (Checkbox)
var_check_saudacao = tk.BooleanVar()
check_saudacao = tk.Checkbutton(janela, text="Usar saudação informal", variable=var_check_saudacao, bg=COR_FUNDO)
check_saudacao.pack(pady=5)

var_check_personalizada = tk.BooleanVar()
check_personalizada = tk.Checkbutton(janela, text="Usar saudação personalizada", variable=var_check_personalizada, bg=COR_FUNDO)
check_personalizada.pack(pady=5)

# ComboBox (Caixa de seleção com opções)
label_cor = tk.Label(janela, text="Escolha sua cor favorita:", bg=COR_FUNDO)
label_cor.pack(pady=5)

combo_cor = ttk.Combobox(janela, values=["Vermelho","Azul","Verde","Amarelo","Preto","Branco"])
combo_cor.set("Escolha (sua cor)")
combo_cor.pack(pady=5)

# Criar botões (Frase e Limpar)
botao_atualizar = tk.Button(janela, text="Atualizar", command=atualizar_resultado, bg="#28a745")
botao_atualizar.pack(pady=10)

botao_limpar = tk.Button(janela, text="Limpar", command=limpar_campos, bg="#dc3545")
botao_limpar.pack(pady=5)

# Exibição do resultado final (Rótulo "Label")
label_resultado = tk.Label(janela, text="", wraplength=300, bg=COR_FUNDO, font=("Arial", 15, "bold"))
label_resultado.pack(pady=10)

# Executar a janela principal
janela.mainloop()