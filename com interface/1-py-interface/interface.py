import tkinter as tk

def mostrar_mensagem():
    # Obter o texto da caixa de texto
    texto = caixa_texto.get()
    # Atualizar o texto do rótulo com o texto da caixa
    label_resultado.config(text=texto)

# Criar a janela principal
janela = tk.Tk()
janela.title("Exemplo de interface")
janela.geometry("400x150")

# Mudando cor de fundo da tela
janela.config(bg="red")

# Criar uma caixa de entrada (Entry)
caixa_texto = tk.Entry(janela, width=60)
caixa_texto.pack(pady=10)

# Criar botão
botao =tk.Button(janela, text="Mostrar Texto", command=mostrar_mensagem, bg="blue", fg="white")
botao.pack(pady=5)

# Criar um rótulo para mostrar resultado
label_resultado = tk.Label(janela, text="", bg="red", fg="white")
label_resultado.pack(pady=10)

# Executar a tela principal
janela.mainloop()