#!/usr/bin/env python3
import os
import time
import re
from datetime import datetime

# ====== CORES ======
PINK = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ====== BANNER ======
BANNER = f"""
{PINK}{BOLD}
██╗███╗░░██╗██████╗░██╗░█████╗░
██║████╗░██║██╔══██╗██║██╔══██╗
██║██╔██╗██║██║░░██║██║███████║
██║██║╚████║██║░░██║██║██╔══██║
██║██║░╚███║██████╔╝██║██║░░██║
╚═╝╚═╝░░╚══╝╚═════╝░╚═╝╚═╝░░╚═╝

███╗░░░███╗░█████╗░██████╗░██████╗░██╗░░░██╗███████╗
████╗░████║██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝██╔════╝
██╔████╔██║███████║██████╔╝██████╔╝░╚████╔╝░█████╗░
██║╚██╔╝██║██╔══██║██╔══██╗██╔══██╗░░╚██╔╝░░██╔══╝░
██║░╚═╝░██║██║░░██║██║░░██║██║░░██║░░░██║░░░███████╗
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
{RESET}
"""

# ====== MENU ======
MENU = f"""
{PINK}╭┄┄┄┄┄┄┄
├┄❲1❳ Denúncia
├┄❲2❳ Spam
├┄❲3❳ Denúncia Dupla
├┄❲4❳ Spam Dupla
├┄❲5❳ Sair
╰┄┄┄┄┄┄┄{RESET}
"""

# ====== FUNÇÕES ======
def clear():
    os.system("clear")

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
            print(f"{PINK}Número inválido encontrado: \"{p}\"{RESET}")
            return None
        normalized.append(n)
    if not normalized:
        print(f"{PINK}Nenhum número válido fornecido.{RESET}")
        return None
    return normalized

def progress_bar_fixed(total, delay, action, number):
    bar_length = 50
    print(f"{PINK}{action} -> {number}{RESET}")  # Texto fixo acima da barra
    for i in range(total + 1):
        percent = i / total
        filled_length = int(bar_length * percent)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r{PINK}[{bar}] {int(percent*100)}%{RESET}", end='', flush=True)
        time.sleep(delay)
    print()  # linha final depois que barra enche

def execute_action(action_name, multiple_numbers=False):
    clear()
    print(BANNER)

    if multiple_numbers:
        numbers_input = input(f"{PINK}Digite o(s) número(s) separados por vírgula:{RESET} ")
        numbers = parse_numbers_field(numbers_input)
        if not numbers:
            input(f"{PINK}Pressione Enter para voltar ao menu.{RESET}")
            return
    else:
        number = input(f"{PINK}Digite o número:{RESET} ")
        n = normalize_number(number)
        if not n:
            print(f"{PINK}Número inválido!{RESET}")
            input("Enter para voltar...")
            return
        numbers = [n]

    try:
        qty = int(input(f"{PINK}Quantidade por número:{RESET} "))
    except:
        print(f"{PINK}Quantidade inválida!{RESET}")
        input("Enter para voltar...")
        return

    try:
        delay_input = input(f"{PINK}Delay entre envios (s, opcional, padrão=1):{RESET} ")
        delay = float(delay_input) if delay_input else 1
    except:
        print(f"{PINK}Delay inválido! Usando 1s.{RESET}")
        delay = 1

    clear()
    print(BANNER)
    start_time = datetime.now()

    for number in numbers:
        progress_bar_fixed(qty, delay, f"Executando {action_name}", number)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # ===== RESUMO DENTRO DA CAIXINHA =====
    print(f"""
{PINK}╭┄┄┄┄┄┄┄
├┄❲ RESUMO ❳
├┄Ação: {action_name}
├┄Número(s): {', '.join(numbers)}
├┄Quantidade por número: {qty}
├┄Delay: {delay}s
├┄Itens processados: {len(numbers)*qty}
├┄Início: {start_time}
├┄Término: {end_time}
├┄Duração total (s): {duration:.2f}
╰┄┄┄┄┄┄┄{RESET}
""")
    input(f"{PINK}Pressione Enter para voltar ao menu.{RESET}")

# ====== LOOP PRINCIPAL ======
while True:
    clear()
    print(BANNER)
    print(MENU)
    choice = input(f"{PINK}Escolha uma opção (1-5): {RESET}")
    if choice == "1":
        execute_action("Denúncia")
    elif choice == "2":
        execute_action("Spam")
    elif choice == "3":
        execute_action("Denúncia Dupla", multiple_numbers=True)
    elif choice == "4":
        execute_action("Spam Dupla", multiple_numbers=True)
    elif choice == "5":
        print(f"{PINK}Saindo...{RESET}")
        break
    else:
        print(f"{PINK}Opção inválida!{RESET}")
        time.sleep(1)
