#!/usr/bin/env python3
# india_marrye_termux.py
# Painel "Índia marrye" para Termux — CLI pura
# Execute: python india_marrye_termux.py

import os
import re
import time
from datetime import datetime

PANEL_NAME = "Índia marrye"

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    print("="*60)
    print(f"{PANEL_NAME:^60}")
    print("="*60)
    print()

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

def get_input_numbers():
    raw = input("Digite o(s) número(s) separados por vírgula: ")
    numbers, err = parse_numbers_field(raw)
    if err:
        print(f"Erro: {err}")
        return get_input_numbers()
    return numbers

def get_input_action():
    actions = ["Denúncia", "Spam", "Denúncia dupla", "Spam dupla"]
    print("\nEscolha a ação:")
    for i, a in enumerate(actions, 1):
        print(f"{i}. {a}")
    choice = input("Digite o número da ação: ")
    try:
        idx = int(choice)
        if 1 <= idx <= len(actions):
            return actions[idx-1]
        else:
            raise ValueError
    except:
        print("Escolha inválida!")
        return get_input_action()

def get_input_qty():
    try:
        qty = int(input("Quantidade por número: "))
        if qty <= 0:
            raise ValueError
        return qty
    except:
        print("Quantidade inválida!")
        return get_input_qty()

def get_input_delay():
    try:
        delay = float(input("Delay entre envios (segundos): "))
        if delay < 0:
            raise ValueError
        return delay
    except:
        print("Delay inválido!")
        return get_input_delay()

def main_loop():
    while True:
        print_banner()
        numbers = get_input_numbers()
        action = get_input_action()
        qty = get_input_qty()
        delay = get_input_delay()

        total_tasks = len(numbers) * qty
        print("\nIniciando execução...")
        start_time = datetime.now()
        task_count = 0

        for n in numbers:
            for i in range(1, qty+1):
                task_count += 1
                print(f"[{task_count}/{total_tasks}] {action} -> {n} (item {i} de {qty})")
                time.sleep(delay)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n=== RESUMO DA EXECUÇÃO ===")
        print(f"Painel: {PANEL_NAME}")
        print(f"Ação: {action}")
        print(f"Número(s): {', '.join(numbers)}")
        print(f"Quantidade por número: {qty}")
        print(f"Delay entre envios: {delay}s")
        print(f"Itens processados: {total_tasks}")
        print(f"Início: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Término: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duração total (s): {duration:.2f}")
        print("============================\n")
        input("Pressione Enter para voltar ao menu...")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nSaindo...")
