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

def progress_bar(total, delay, action, number):
    for i in range(1, total+1):
        percent = int((i/total)*100)
        bar = f"{PINK}[{'#' * (percent//2)}{'-'*(50 - percent//2)}] {percent}%{RESET}"
        print(f"{PINK}{action} -> {number} ({i}/{total}) {bar}{RESET}", end='\r')
        time.sleep(delay)
    print()

def execute_action(action_name):
    clear()
    print(BANNER)
    numbers_input = input(f"{PINK}Digite o(s) número(s) separados por vírgula:{RESET} ")
    numbers = parse_numbers_field(numbers_input)
    if not numbers:
        input(f"{PINK}Pressione Enter para voltar ao menu.{RESET}")
        return

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
    print(f"{PINK}Executando {action_name}...{RESET}")
    start_time = datetime.now()

    for number in numbers:
        progress_bar(qty, delay, action_name, number)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n{PINK}=== RESUMO ==={RESET}")
    print(f"{PINK}Ação: {action_name}{RESET}")
    print(f"{PINK}Número(s): {', '.join(numbers)}{RESET}")
    print(f"{PINK}Quantidade por número: {qty}{RESET}")
    print(f"{PINK}Delay: {delay}s{RESET}")
    print(f"{PINK}Itens processados: {len(numbers)*qty}{RESET}")
    print(f"{PINK}Início: {start_time}{RESET}")
    print(f"{PINK}Término: {end_time}{RESET}")
    print(f"{PINK}Duração total (s): {duration:.2f}{RESET}")
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
        execute_action("Denúncia Dupla")
    elif choice == "4":
        execute_action("Spam Dupla")
    elif choice == "5":
        print(f"{PINK}Saindo...{RESET}")
        break
    else:
        print(f"{PINK}Opção inválida!{RESET}")
        time.sleep(1)

# ====== FINAL DO SCRIPT ======
print(f"{PINK}Obrigado por usar o painel Índia Marrye!{RESET}")
