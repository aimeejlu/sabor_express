import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import re

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Controle Financeiro")
        self.geometry("900x500")
        self.minsize(700, 400)
        self.configure(bg="black")

        # Dados das transações: lista de dicionários
        self.transactions = []

        # Saldo inicial
        self.balance = 0.0

        # Contador de ID sequencial
        self.next_id = 1

        # Criar interface
        self.create_widgets()
        self.update_balance_label()
        self.update_transaction_history()

    def create_widgets(self):
        # Container principal
        self.main_frame = ctk.CTkFrame(self, fg_color=None)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Layout horizontal: esquerda (form) e direita (histórico)
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color=None)
        self.left_frame.pack(side="left", fill="y", expand=False)

        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color=None)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(20,0))

        # Título Saldo
        self.balance_label = ctk.CTkLabel(
            self.left_frame,
            text="Saldo: R$ 0,00",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#00B45A",
            anchor="center"
        )
        self.balance_label.pack(pady=(0, 30), fill="x")

        # Tipo transação (Receita / Despesa)
        self.tipo_var = tk.StringVar(value="receita")
        tipo_frame = ctk.CTkFrame(self.left_frame, fg_color=None)
        tipo_frame.pack(pady=(0, 20), fill="x")

        # Centralizar os botões usando grid e adicionar uma coluna "espacadora"
        tipo_frame.grid_columnconfigure(0, weight=1)
        tipo_frame.grid_columnconfigure(1, weight=1)

        self.radio_receita = ctk.CTkRadioButton(
            tipo_frame,
            text="Receita",
            variable=self.tipo_var,
            value="receita",
            text_color="#00B45A",
            font=ctk.CTkFont(size=18, weight="bold"),
            border_color="#00B45A",
            hover_color="#00B45A",
            fg_color="#00B45A",  # Botão verde
            width=30,
            height=30,
            corner_radius=15,
        )
        self.radio_receita.grid(row=0, column=0, padx=20, sticky="ew")

        self.radio_despesa = ctk.CTkRadioButton(
            tipo_frame,
            text="Despesa",
            variable=self.tipo_var,
            value="despesa",
            text_color="#FF3B3B",
            font=ctk.CTkFont(size=18, weight="bold"),
            border_color="#FF3B3B",
            hover_color="#FF3B3B",
            fg_color="#FF3B3B",  # Botão vermelho
            width=30,
            height=30,
            corner_radius=15,
        )
        self.radio_despesa.grid(row=0, column=1, padx=20, sticky="ew")

        # Input Valor
        self.valor_entry = ctk.CTkEntry(
            self.left_frame,
            placeholder_text="Valor",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            width=280,
            height=45,
            corner_radius=30,
        )
        self.valor_entry.pack(pady=(0, 20))

        # Input Descrição
        self.descricao_entry = ctk.CTkEntry(
            self.left_frame,
            placeholder_text="Descrição",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            width=280,
            height=45,
            corner_radius=30,
        )
        self.descricao_entry.pack(pady=(0, 20))

        # Botão Adicionar
        self.btn_adicionar = ctk.CTkButton(
            self.left_frame,
            text="Adicionar",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#00B45A",
            hover_color="#009944",
            width=180,
            height=45,
            corner_radius=30,
            command=self.adicionar_transacao,
        )
        self.btn_adicionar.pack(pady=(0, 30))

        # Input ID da Transação para exclusão
        self.id_entry = ctk.CTkEntry(
            self.left_frame,
            placeholder_text="ID da Transação",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            width=280,
            height=45,
            corner_radius=30,
        )
        self.id_entry.pack(pady=(0, 20))

        # Botão Excluir
        self.btn_excluir = ctk.CTkButton(
            self.left_frame,
            text="Excluir",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#FF3B3B",
            hover_color="#cc2a2a",
            width=180,
            height=45,
            corner_radius=30,
            command=self.excluir_transacao,
        )
        self.btn_excluir.pack()

        # Histórico de Transação (direita)
        self.history_header = ctk.CTkFrame(self.right_frame, fg_color="#6B6B6B", corner_radius=20)
        self.history_header.pack(fill="x")

        self.history_label = ctk.CTkLabel(
            self.history_header,
            text="Histórico de Transação",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white",
            pady=10,
        )
        self.history_label.pack()

        self.history_body = ctk.CTkScrollableFrame(
            self.right_frame,
            fg_color="white",
            corner_radius=20,
            height=350,
            width=500,
        )
        self.history_body.pack(fill="both", expand=True, pady=(0,0))

    def format_valor(self, valor_str):
        """
        Formata o valor para float, aceitando vírgula ou ponto como separador decimal.
        Retorna float ou None se inválido.
        """
        valor_str = valor_str.strip().replace(" ", "")
        # Trocar vírgula por ponto
        valor_str = valor_str.replace(",", ".")
        # Validar se é número válido (positivo)
        if re.fullmatch(r"\d+(\.\d{1,2})?", valor_str):
            return float(valor_str)
        return None

    def adicionar_transacao(self):
        valor_text = self.valor_entry.get()
        descricao = self.descricao_entry.get().strip()
        tipo = self.tipo_var.get()

        valor = self.format_valor(valor_text)
        if valor is None or valor <= 0:
            self.show_feedback("Valor inválido! Use números positivos, ex: 1000, 1000.50 ou 1000,50", error=True)
            return
        if descricao == "":
            self.show_feedback("Descrição não pode ser vazia!", error=True)
            return

        # Ajustar valor para despesa (negativo)
        if tipo == "despesa":
            valor = -valor

        # Criar ID sequencial
        transacao_id = str(self.next_id)
        self.next_id += 1

        # Adicionar transação
        self.transactions.append({
            "id": transacao_id,
            "valor": valor,
            "descricao": descricao,
            "tipo": tipo,
        })

        # Atualizar saldo e histórico
        self.update_balance()
        self.update_transaction_history()

        # Limpar inputs
        self.valor_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)

        self.show_feedback(f"Transação adicionada com ID: {transacao_id}", error=False)

    def excluir_transacao(self):
        id_to_remove = self.id_entry.get().strip()
        if id_to_remove == "":
            self.show_feedback("Informe o ID da transação para excluir!", error=True)
            return

        # Procurar transação pelo ID
        for i, t in enumerate(self.transactions):
            if t["id"] == id_to_remove:
                del self.transactions[i]
                self.update_balance()
                self.update_transaction_history()
                self.id_entry.delete(0, tk.END)
                self.show_feedback(f"Transação {id_to_remove} excluída com sucesso.", error=False)
                return

        self.show_feedback(f"ID {id_to_remove} não encontrado.", error=True)

    def update_balance(self):
        self.balance = sum(t["valor"] for t in self.transactions)
        self.update_balance_label()

    def update_balance_label(self):
        # Formatar saldo com 2 casas decimais e vírgula decimal
        saldo_str = f"R$ {self.balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.balance_label.configure(text=f"Saldo: {saldo_str}")

        # Cor do saldo: verde se >=0, vermelho se negativo
        if self.balance >= 0:
            self.balance_label.configure(text_color="#00B45A")
        else:
            self.balance_label.configure(text_color="#FF3B3B")

    def update_transaction_history(self):
        # Limpar histórico
        for widget in self.history_body.winfo_children():
            widget.destroy()

        if not self.transactions:
            empty_label = ctk.CTkLabel(
                self.history_body,
                text="Nenhuma transação registrada.",
                font=ctk.CTkFont(size=16),
                text_color="#555555",
                pady=20,
            )
            empty_label.pack()
            return

        # Mostrar cada transação
        for t in self.transactions:
            frame = ctk.CTkFrame(self.history_body, fg_color="#f0f0f0", corner_radius=10, height=50)
            frame.pack(fill="x", padx=10, pady=6)

            # ID
            id_label = ctk.CTkLabel(
                frame,
                text=t["id"],
                font=ctk.CTkFont(size=14, weight="bold"),
                width=70,
                anchor="w",
                text_color="#333333",
            )
            id_label.pack(side="left", padx=(10,5))

            # Descrição
            desc_label = ctk.CTkLabel(
                frame,
                text=t["descricao"],
                font=ctk.CTkFont(size=16),
                anchor="w",
                width=250,
                text_color="#222222",
            )
            desc_label.pack(side="left", padx=(0,5))

            # Valor formatado
            valor_abs = abs(t["valor"])
            valor_str = f"R$ {valor_abs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            valor_label = ctk.CTkLabel(
                frame,
                text=valor_str,
                font=ctk.CTkFont(size=18, weight="bold"),
                width=120,
                anchor="e",
                text_color="#00B45A" if t["tipo"] == "receita" else "#FF3B3B",
            )
            valor_label.pack(side="right", padx=(5,10))

    def show_feedback(self, message, error=False):
        # Mensagem visual temporária no topo da janela
        if hasattr(self, "feedback_label"):
            self.feedback_label.destroy()

        color = "#FF3B3B" if error else "#00B45A"
        self.feedback_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color,
            bg_color="black",
            anchor="center",
        )
        self.feedback_label.place(relx=0.5, rely=0.02, anchor="n")

        # Remover após 4 segundos
        self.after(4000, self.feedback_label.destroy)

if __name__ == "__main__":
    try:
        app = FinanceApp()
        app.mainloop()
    except Exception as e:
        print("Erro ao iniciar a aplicação:", e)
        print("Verifique se o módulo 'customtkinter' está instalado corretamente.")