# Usando biblioteca Thinker (padrão do Python para interfaces)
import tkinter as tk

# Submodulo do tkinter com Widgets mais modernos e estilizados
from tkinter import tik

def atualizar_resultado():
    # Obter o texto da caixa de entrada
    nome = caixa_de_texto.get()

    # Obter opção selecionada nos botões de rádio
    preferencia = var_radio.get()

    # Verificar se a caixa de seleção de saudação personalizada está marcada
    if ver_check_saudacao.get():
        saudacao = "Olá"
    else:
        saudacao = "Bem-vindo"

    if var_check_personalizado.get():
        saudacao = f"{saudacao}, caro(a)"

    # Obter cor favortia selecionada
    cor_favorita = comobo_cor.get()

    # Montar mensagem final
    mensagem = f"{saudacao} {nome}! Você prefere {preferencia}."
    if cor_favorita:
        mensagem += f" Sua cor favorita é {cor_favorita}."

    # Atualizar o texto do rótulo da mensagem
    label_resultado.config(text=mensagem)