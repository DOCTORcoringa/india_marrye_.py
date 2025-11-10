#!/usr/bin/env python3
# india_marrye_termux.py
# CLI para Termux — Painel "Índia marrye"
# NÃO envia mensagens externas — apenas simula/processa localmente.

import os
import re
import time
import sys
from datetime import datetime

PANEL_NAME = "Índia marrye"
VERSION = "1.0"

# Cores ANSI (Termux suporta)
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_MAGENTA = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    w = 60
    top = "=" * w
    name = f"{PANEL_NAME}".upper()
    # centralizar nome em destaque (sem arte)
    print(C_MAGENTA + top + C_RESET)
    print(C_MAGENTA + C_BOLD + f"{name:^{w}}" + C_RESET)
    print(C_MAGENTA + top + C_RESET)
    print(f"{C_DIM}Versão: {VERSION} | Use em ambiente controlado. O proprietário não se responsabiliza por uso de má fé.{C_RESET}")
    print()

# Normaliza números aceitando +, espaços, hífen etc.
def normalize_number(raw):
    raw = raw.strip()
    if raw == "":
        return None
    plus = raw.startswith('+')
    digits = re.sub(r'\D', '', raw)  # remove tudo não dígito
    if digits == "":
        return None
    # se começou com + ou já tem 55 no início, garante +55...
    if plus or digits.startswith('55'):
        if not digits.startswith('55'):
            digits = '55' + digits
        return '+' + digits
    # caso nacional sem DDI, retorna como dígitos (por ex 64xxxxx)
    return digits

def parse_numbers_field(field_text):
    # aceita separadores: vírgula (principal), também aceita ; e nova linha
    parts = re.split(r'[,\n;]+', field_text)
    parts = [p.strip() for p in parts if p.strip() != ""]
    normalized = []
    for p in parts:
        n = normalize_number(p)
        if n is None:
            return None, f"Número inválido encontrado: \"{p}\""
        normalized.append(n)
    if not normalized:
        return None, "Nenhum número válido fornecido."
    return normalized, None

def prompt_numbers():
    txt = input("Digite os números (separados por vírgula): ").strip()
    nums, err = parse_numbers_field(txt)
    if err:
        print(C_RED + "Erro: " + err + C_RESET)
        return prompt_numbers()
    return nums

def prompt_action():
    actions = ["Denúncia", "Spam", "Denúncia dupla", "Spam dupla"]
    print("AÇÕES:")
    for i,a in enumerate(actions, start=1):
        print(f"  {C_CYAN}[{i}] {a}{C_RESET}")
    choice = input("Escolha a ação (número): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(actions)):
        print(C_RED + "Opção inválida." + C_RESET)
        return prompt_action()
    return actions[int(choice)-1]

def prompt_qty():
    s = input("Quantidade por número (ex: 2): ").strip()
    if not s.isdigit() or int(s) <= 0:
        print(C_RED + "Quantidade inválida." + C_RESET)
        return prompt_qty()
    return int(s)

def prompt_delay():
    s = input("Delay entre envios em segundos (ex: 1 ou 0.5): ").strip()
    try:
        d = float(s)
        if d < 0:
            raise ValueError
        return d
    except:
        print(C_RED + "Delay inválido." + C_RESET)
        return prompt_delay()

def show_progress_bar(current, total, width=30):
    pct = current/total if total>0 else 1
    filled = int(width * pct)
    bar = "[" + "#"*filled + "-"*(width-filled) + "]"
    print(f"{bar} {current}/{total} ({pct*100:.1f}%)", end='\r')

def run_execution(action, numbers, qty, delay):
    # SOS: limpa antes de exibir execução
    banner()
    start = datetime.now()
    total = len(numbers) * qty
    print(C_GREEN + f"Iniciando — Ação: {action} | Alvos: {', '.join(numbers)} | Qtd por alvo: {qty} | Delay: {delay}s" + C_RESET)
    print("Início:", start.strftime('%Y-%m-%d %H:%M:%S'))
    print()
    processed = 0
    try:
        for n in numbers:
            for i in range(1, qty+1):
                processed += 1
                ts = datetime.now().strftime('%H:%M:%S')
                # Exibe linha de processamento
                print(f"{C_YELLOW}{ts} — {action} -> {n} (item {i} de {qty}){C_RESET}")
                # Atualiza barra de progresso na mesma linha
                show_progress_bar(processed, total)
                # Sleep pelo delay pedido
                time.sleep(delay)
        # limpar a linha de progresso residual
        print()
    except KeyboardInterrupt:
        print()
        print(C_RED + "Execução interrompida pelo usuário (CTRL+C)." + C_RESET)
    end = datetime.now()
    duration = (end - start).total_seconds()
    # Resumo
    print()
    print(C_MAGENTA + "="*60 + C_RESET)
    print(C_BOLD + "RESUMO DA EXECUÇÃO" + C_RESET)
    print(f"Painel: {PANEL_NAME}")
    print(f"Ação: {action}")
    print(f"Número(s): {', '.join(numbers)}")
    print(f"Quantidade por número: {qty}")
    print(f"Delay entre envios: {delay}s")
    print(f"Itens processados: {processed}")
    print(f"Início: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Término: {end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duração total (s): {duration:.2f}")
    print(C_MAGENTA + "="*60 + C_RESET)
    input("Pressione Enter para voltar ao menu...")

def main_menu():
    while True:
        banner()
        print("Menu:")
        print(f"  {C_CYAN}[1]{C_RESET} Executar ação")
        print(f"  {C_CYAN}[2]{C_RESET} Sair")
        choice = input("Escolha: ").strip()
        if choice == '1':
            numbers = prompt_numbers()
            action = prompt_action()
            qty = prompt_qty()
            delay = prompt_delay()
            run_execution(action, numbers, qty, delay)
        elif choice == '2':
            print(C_GREEN + "Saindo... até mais." + C_RESET)
            sys.exit(0)
        else:
            print(C_RED + "Opção inválida." + C_RESET)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n" + C_RED + "Encerrado pelo usuário." + C_RESET)
        sys.exit(0)
