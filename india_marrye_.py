#!/usr/bin/env python3
import os
import time
import json
import re
from datetime import datetime, timedelta

# ==========================================================
#         INSTALAÇÃO AUTOMÁTICA (UMA VEZ SÓ)
# ==========================================================
os.system("command -v toilet >/dev/null 2>&1 || pkg install toilet -y")
os.system("command -v figlet >/dev/null 2>&1 || pkg install figlet -y")

# ==========================================================
# ====================== CONFIG =============================
# ==========================================================

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "custom_banner_text": None,
            "custom_banner_ascii": None
        }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

def days_since_update():
    last = datetime.strptime(settings["last_update"], "%Y-%m-%d")
    return (datetime.now() - last).days

# ==========================================================
# ====================== CORES ==============================
# ==========================================================

PINK = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ==========================================================
# ====================== BANNER =============================
# ==========================================================

DEFAULT_BANNER = f"""
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

def gerar_ascii_3d(texto):
    comando = f'toilet -f 3d -F metal "{texto}"'
    return os.popen(comando).read()

def get_banner():
    # >>> Se houver banner custom, ele aparece imediatamente, o padrão desaparece
    if settings.get("custom_banner_ascii"):
        return PINK + BOLD + settings["custom_banner_ascii"] + RESET
    return DEFAULT_BANNER

# ==========================================================
# ======================= MENU ==============================
# ==========================================================

MENU = f"""
{PINK}╭┄┄┄┄┄┄┄
├┄❲1❳ Denúncia
├┄❲2❳ Spam
├┄❲3❳ Denúncia Dupla
├┄❲4❳ Spam Dupla
├┄❲5❳ Sair
├┄❲6❳ Atualizar Sistema
├┄❲7❳ Alterar Banner
╰┄┄┄┄┄┄┄{RESET}
"""

# ==========================================================
# ====================== FUNÇÕES ============================
# ==========================================================

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
            print(f"{PINK}Número inválido encontrado: {p}{RESET}")
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
            print(get_banner())
            hora_atual = datetime.now().strftime("%H:%M:%S")
            print(f"{PINK}Hora: {hora_atual}{RESET}\n")
            print(f"{PINK}Executando: {action} → {number}{RESET}\n")

            percent = int((i / total) * 100)
            filled = int(percent / 2)
            bar = f"[{'#' * filled}{'-' * (50 - filled)}] {percent}%"
            print(f"{PINK}{bar}{RESET}\n")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"{PINK}Encerrando...{RESET}")
        exit(0)

# ==========================================================
# ================ SISTEMA DE ATUALIZAÇÃO ===================
# ==========================================================

def atualizar_sistema():
    dias = days_since_update()

    if dias < 30:
        print(f"{PINK}A atualização só estará disponível em {30 - dias} dias.{RESET}")
        input("Enter para voltar...")
        return

    print(f"{PINK}Atualizando para versão 2.0...{RESET}")
    time.sleep(2)

    settings["last_update"] = datetime.now().strftime("%Y-%m-%d")
    save_settings(settings)

    print(f"{PINK}Atualização concluída!{RESET}")
    input("Enter para voltar...")

def verificar_bloqueio():
    return days_since_update() >= 30

# ==========================================================
# ================= ALTERAR BANNER ==========================
# ==========================================================

def alterar_banner():
    clear()
    print(get_banner())
    print(f"{PINK}Digite o novo nome para o banner:{RESET}")
    nome = input("> ").strip()

    if nome == "":
        print(f"{PINK}Nenhum nome inserido. Mantendo o atual.{RESET}")
    else:
        ascii_banner = gerar_ascii_3d(nome)
        settings["custom_banner_text"] = nome
        settings["custom_banner_ascii"] = ascii_banner
        save_settings(settings)
        # >>> Recarrega as configurações imediatamente para sumir o banner padrão
        settings.update(load_settings())
        print(f"{PINK}Banner atualizado! O padrão desapareceu e só existe o novo nome.{RESET}")

    input("Enter para voltar...")

# ==========================================================
# ================= EXECUTAR AÇÃO ===========================
# ==========================================================

def execute_action(action_name, multiple_allowed=False):
    if verificar_bloqueio():
        print(f"{PINK}Seu painel está desatualizado!\nAtualize antes de usar qualquer ação.{RESET}")
        input("Enter para voltar...")
        return

    clear()
    print(get_banner())
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

    delay_input = input(f"{PINK}Delay entre envios (s, padrão=1):{RESET} ")
    try:
        delay = float(delay_input) if delay_input else 1
    except:
        print(f"{PINK}Delay inválido! Usando 1s.{RESET}")
        delay = 1

    start_time = datetime.now()
    for number in numbers:
        progress_bar_fixed(qty, delay, action_name, number)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()
    print(f"{PINK}Ação concluída! Duração total: {duration:.2f}s{RESET}")
    input("Enter para voltar...")

# ==========================================================
# ==================== LOOP PRINCIPAL =======================
# ==========================================================

while True:
    try:
        clear()
        print(get_banner())
        print(MENU)

        choice = input(f"{PINK}Escolha uma opção (1-7): {RESET}")

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
        elif choice == "6":
            atualizar_sistema()
        elif choice == "7":
            alterar_banner()
        else:
            print(f"{PINK}Opção inválida!{RESET}")
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"{PINK}Encerrando painel Índia Marrye...{RESET}")
        break
