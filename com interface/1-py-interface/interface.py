import tkinter as tk

def mostrar_mensagem():
    # Obter o texto da caixa de texto
    texto = caixa_texto.get()
    # Atualizar o texto do rótulo com o texto da caixa
    label_resultado.config(text=texto)

# Criar a janela principal
janela = tk.Tk()
janela.title("Interface avançada")
janela.geometry("400x500")


# Criar uma caixa de entrada (Entry)
label_nome = tk.Label(janela, text="Digite seu nome:")
label_nome.pack(pady=5)
caixa_texto = tk.Entry(janela, width=40)
caixa_texto.pack(pady=5)

# Criar botões de rádio


# Executar a tela principal
janela.mainloop()