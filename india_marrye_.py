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
██╔████╔██║███████║██████╔╝██████╔╝░╚████╔╝░█████╗░░
██║╚██╔╝██║██╔══██║██╔══██╗██╔══██╗░░╚██╔╝░░██╔══╝░░
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
    try:
        for i in range(total + 1):
            clear()
            print(BANNER)
            hora_atual = datetime.now().strftime("%H:%M:%S")
            print(f"{PINK}╭┄┄┄┄┄┄┄\n├┄ Hora: {hora_atual}\n╰┄┄┄┄┄┄┄{RESET}")
            print(f"{PINK}Executando: {action} → {number}{RESET}\n")

            percent = int((i / total) * 100)
            filled = int(percent / 2)
            bar = f"[{'#' * filled}{'-' * (50 - filled)}] {percent}%"
            print(f"{PINK}{bar}{RESET}\n")
            print(f"{PINK}╭┄┄┄┄┄┄┄\n├┄ Painel Índia Marrye\n╰┄┄┄┄┄┄┄{RESET}")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{PINK}\nEncerrando execução com segurança...{RESET}")
        time.sleep(1)
        exit(0)

def execute_action(action_name, multiple_allowed=False):
    clear()
    print(BANNER)
    numbers_input = input(f"{PINK}Digite o(s) número(s){' (separe por vírgula)' if multiple_allowed else ''}:{RESET} ")

    if multiple_allowed:
        numbers = parse_numbers_field(numbers_input)
    else:
        n = normalize_number(numbers_input)
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

    start_time = datetime.now()
    for number in numbers:
        progress_bar_fixed(qty, delay, action_name, number)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()
    print(f"\n{PINK}╭┄┄┄┄┄┄┄")
    print(f"├┄ Ação: {action_name}")
    print(f"├┄ Número(s): {', '.join(numbers)}")
    print(f"├┄ Quantidade: {qty}")
    print(f"├┄ Delay: {delay}s")
    print(f"├┄ Duração total: {duration:.2f}s")
    print(f"╰┄┄┄┄┄┄┄{RESET}")
    input(f"{PINK}Pressione Enter para voltar ao menu.{RESET}")

# ====== LOOP PRINCIPAL ======
while True:
    try:
        clear()
        print(BANNER)
        print(MENU)
        choice = input(f"{PINK}Escolha uma opção (1-5): {RESET}")
        if choice == "1":
            execute_action("Denúncia")
        elif choice == "2":
            execute_action("Spam")
        elif choice == "3":
            execute_action("Denúncia Dupla", multiple_allowed=True)
        elif choice == "4":
            execute_action("Spam Dupla", multiple_allowed=True)
        elif choice == "5":
            print(f"{PINK}Saindo...{RESET}")
            break
        else:
            print(f"{PINK}Opção inválida!{RESET}")
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{PINK}\nEncerrando painel Índia Marrye...{RESET}")
        time.sleep(1)
        break
