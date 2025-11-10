#!/usr/bin/env python3
# india_marrye_menu.py
# Painel "Índia marrye" — Execute: python india_marrye_menu.py
# Use em ambiente controlado. O proprietário não se responsabiliza por uso de má fé.

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

PANEL_NAME = "Índia marrye"
VERSION = "1.0"

# --- Validação/normalização de números ---
def normalize_number(raw):
    raw = raw.strip()
    plus = raw.startswith('+')
    digits = re.sub(r'\D', '', raw)
    if not digits:
        return None
    if plus or digits.startswith('55'):
        if not digits.startswith('55'):
            digits = '55' + digits
        return '+' + digits
    return digits

def parse_numbers_field(field_text):
    parts = [p.strip() for p in field_text.split(',') if p.strip() != ""]
    normalized = []
    for p in parts:
        n = normalize_number(p)
        if n is None:
            return None, f"Número inválido encontrado: \"{p}\""
        normalized.append(n)
    if not normalized:
        return None, "Nenhum número válido fornecido."
    return normalized, None

# --- Aplicativo ---
class IndiaMarryeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(PANEL_NAME)
        self.configure(bg='#ffe6f0')
        self.geometry('720x560')
        self.resizable(False, False)
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Return>', self.on_enter_key)

    def _build_ui(self):
        # Cabeçalho grande como banner
        header = tk.Frame(self, bg='#ffb6d5', height=100)
        header.pack(fill='x', padx=12, pady=(12,6))
        header.pack_propagate(False)
        title = tk.Label(header, text=PANEL_NAME, font=('Helvetica', 28, 'bold'),
                         bg='#ffb6d5', fg='#ffffff')
        title.pack(expand=True)

        # Conteúdo principal
        content = tk.Frame(self, bg='#ffe6f0')
        content.pack(fill='both', expand=True, padx=12, pady=6)

        # Coluna esquerda (formulário)
        left = tk.Frame(content, bg='#ffe6f0', width=340)
        left.pack(side='left', fill='y', padx=(0,8))
        left.pack_propagate(False)

        form_box = tk.Frame(left, bg='#ffdbe8', bd=2, relief='ridge')
        form_box.place(relx=0.5, rely=0.02, anchor='n', width=320, height=420)

        # Campos do formulário
        tk.Label(form_box, text="NÚMERO(s):", bg='#ffdbe8', anchor='w').place(x=12, y=12, width=296, height=22)
        self.entry_numbers = tk.Entry(form_box)
        self.entry_numbers.place(x=12, y=36, width=296, height=32)
        self.entry_numbers.insert(0, "+55 64 9604-9771")

        tk.Label(form_box, text="AÇÃO:", bg='#ffdbe8', anchor='w').place(x=12, y=80, width=296, height=22)
        self.action_var = tk.StringVar(value="Denúncia")
        ttk.Combobox(form_box, textvariable=self.action_var, state='readonly',
                     values=["Denúncia", "Spam", "Denúncia dupla", "Spam dupla"]).place(x=12, y=104, width=296, height=30)

        tk.Label(form_box, text="QUANTIDADE (por número):", bg='#ffdbe8', anchor='w').place(x=12, y=150, width=296, height=22)
        self.spin_qty = tk.Spinbox(form_box, from_=1, to=1000)
        self.spin_qty.place(x=12, y=174, width=296, height=30)

        tk.Label(form_box, text="DELAY entre envios (segundos):", bg='#ffdbe8', anchor='w').place(x=12, y=214, width=296, height=22)
        self.entry_delay = tk.Entry(form_box)
        self.entry_delay.place(x=12, y=238, width=296, height=30)
        self.entry_delay.insert(0, "1")

        # Botão executar
        self.btn_start = tk.Button(form_box, text="Executar", bg='#ff88b8', command=self.on_start)
        self.btn_start.place(x=12, y=286, width=296, height=40)

        # Barra de progresso
        tk.Label(form_box, text="Progresso:", bg='#ffdbe8', anchor='w').place(x=12, y=340, width=296, height=16)
        self.progress = ttk.Progressbar(form_box, orient='horizontal', mode='determinate')
        self.progress.place(x=12, y=360, width=296, height=14)

        # Coluna direita (log)
        right = tk.Frame(content, bg='#ffe6f0', width=340)
        right.pack(side='left', fill='y', padx=(8,0))
        right.pack_propagate(False)

        log_box = tk.Frame(right, bg='#ffdbe8', bd=2, relief='ridge')
        log_box.place(relx=0.5, rely=0.02, anchor='n', width=320, height=520)

        tk.Label(log_box, text=f"{PANEL_NAME} — Registro", bg='#ffdbe8', anchor='w').place(x=12, y=8, width=296, height=22)

        self.txt_log = tk.Text(log_box, wrap='word', state='normal')
        self.txt_log.place(x=12, y=36, width=296, height=420)
        self.clear_log_header()

        # Rodapé
        tk.Label(self, text="Use em ambiente controlado. O proprietário não se responsabiliza por uso de má fé.",
                 bg='#ffe6f0', anchor='w').pack(fill='x', padx=12, pady=(0,12))

    def clear_log_header(self):
        self.txt_log.configure(state='normal')
        self.txt_log.delete('1.0', 'end')
        self.txt_log.insert('end', f"{PANEL_NAME}\n")
        self.txt_log.insert('end', "="*50 + "\n\n")
        self.txt_log.configure(state='disabled')

    def log(self, message):
        self.txt_log.configure(state='normal')
        self.txt_log.insert('end', f"{datetime.now().strftime('%H:%M:%S')} — {message}\n")
        self.txt_log.see('end')
        self.txt_log.configure(state='disabled')

    def on_start(self):
        self.clear_log_header()  # SOS: limpa tela antes de cada execução

        raw_numbers = self.entry_numbers.get()
        numbers, err = parse_numbers_field(raw_numbers)
        if err:
            messagebox.showerror("Erro", err)
            return
        try:
            qty = int(self.spin_qty.get())
            if qty <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return
        try:
            delay = float(self.entry_delay.get())
            if delay < 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Erro", "Delay inválido.")
            return

        action = self.action_var.get()
        self.tasks = [(n, i+1) for n in numbers for i in range(qty)]
        self.total_tasks = len(self.tasks)
        if self.total_tasks == 0:
            messagebox.showerror("Erro", "Nenhuma tarefa a executar.")
            return

        self.progress['maximum'] = self.total_tasks
        self.progress['value'] = 0
        self.btn_start.config(state='disabled')
        self.entry_numbers.config(state='disabled')
        self.spin_qty.config(state='disabled')
        self.entry_delay.config(state='disabled')
        self.log(f"Iniciando execução — Ação: {action}; Alvos: {', '.join(numbers)}; Quantidade por alvo: {qty}; Delay: {delay}s")
        self.run_info = {
            'action': action,
            'numbers': numbers,
            'qty_per_number': qty,
            'delay': delay,
            'start_time': datetime.now(),
        }
        self.current_index = 0
        self.after(100, lambda: self._process_next(delay))

    def _process_next(self, delay):
        if self.current_index >= self.total_tasks:
            self._finish_run()
            return
        target, instance = self.tasks[self.current_index]
        self.log(f"{self.run_info['action']} -> {target} (item {instance} de {self.run_info['qty_per_number']})")
        self.current_index += 1
        self.progress['value'] = self.current_index
        self.after(int(delay*1000), lambda: self._process_next(delay))

    def _finish_run(self):
        info = self.run_info
        end_time = datetime.now()
        duration = (end_time - info['start_time']).total_seconds()
        summary_lines = [
            "=== RESUMO DA EXECUÇÃO ===",
            f"Painel: {PANEL_NAME}",
            f"Ação: {info['action']}",
            f"Número(s): {', '.join(info['numbers'])}",
            f"Quantidade por número: {info['qty_per_number']}",
            f"Delay entre envios: {info['delay']}s",
            f"Itens processados: {self.total_tasks}",
            f"Início: {info['start_time'].strftime('%Y-%m-%d %H:%M:%S')}",
            f"Término: {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Duração total (s): {duration:.2f}",
            "===================================="
        ]
        for l in summary_lines:
            self.log(l)
        messagebox.showinfo("Concluído", "Execução concluída. Pressione Enter para voltar à tela inicial.")
        self.finished = True
        self.btn_start.config(state='normal')
        self.log("Pressione Enter para limpar e voltar à tela inicial.")

    def on_enter_key(self, event):
        if getattr(self, 'finished', False):
            self._reset_to_home()

    def _reset_to_home(self):
        self.finished = False
        self.entry_numbers.config(state='normal')
        self.spin_qty.config(state='normal')
        self.entry_delay.config(state='normal')
        self.progress['value'] = 0
        self.clear_log_header()
        self.log("Painel pronto para nova execução.")

    def on_close(self):
        if messagebox.askokcancel("Sair", "Deseja fechar o painel?"):
            self.destroy()

if __name__ == "__main__":
    app = IndiaMarryeApp()
    app.mainloop()
