import sys
from password_strength import PasswordStrengthChecker
import getpass

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

def print_ascii_logo():
    logo = r"""
   ____                 _                         _   _             _             _             
  |  _ \ __ _ _ __ ___ | |__   ___  _ __ ___   __| | | |_ ___   ___| |_ __ _ _ __| |_ ___  _ __ 
  | |_) / _` | '_ ` _ \| '_ \ / _ \| '_ ` _ \ / _` | | __/ _ \ / __| __/ _` | '__| __/ _ \| '__|
  |  __/ (_| | | | | | | |_) | (_) | | | | | | (_| | | || (_) | (__| || (_| | |  | || (_) | |   
  |_|   \__,_|_| |_| |_|_.__/ \___/|_| |_| |_|\__,_|  \__\___/ \___|\__\__,_|_|   \__\___/|_|   
"""
    if COLOR_ENABLED:
        print(Fore.CYAN + logo + Style.RESET_ALL)
    else:
        print(logo)

def print_strength_bar(score):
    bar_length = 20
    filled = int(score * bar_length / 5)
    bar = '█' * filled + '-' * (bar_length - filled)
    if COLOR_ENABLED:
        colors = [Fore.RED, Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.GREEN]
        color = colors[min(score, 4)]
        print(f"  Strength Meter: {color}{bar}{Style.RESET_ALL} ({score}/5)")
    else:
        print(f"  Strength Meter: {bar} ({score}/5)")

def main():
    print()
    print_ascii_logo()
    if COLOR_ENABLED:
        print(f"{Style.BRIGHT}{Fore.CYAN}=== 🔒 Password Strength Analyzer ==={Style.RESET_ALL}")
    else:
        print(f"=== 🔒 Password Strength Analyzer ===")
    print()
    print("Enter your password below for security evaluation\n")
    password = getpass.getpass(f"> Password: ")
    checker = PasswordStrengthChecker()
    result = checker.check(password)
    # Print results with color coding
    strength = result['strength']
    score = result['score']
    if COLOR_ENABLED:
        strength_colors = {
            "Very Weak": Fore.RED,
            "Weak": Fore.RED,
            "Medium": Fore.YELLOW,
            "Strong": Fore.GREEN,
            "Very Strong": Fore.GREEN + Style.BRIGHT
        }
        color = strength_colors.get(strength, Fore.WHITE)
        print(f"\n🔐 {color}Strength: {strength}{Style.RESET_ALL}")
    else:
        print(f"\n🔐 Strength: {strength}")

    print_strength_bar(score)

    # Show crack time
    crack_time = result.get('crack_time', None)
    if crack_time:
        if COLOR_ENABLED:
            print(f"\n⏳ {Fore.CYAN}Estimated time to crack: {crack_time}{Style.RESET_ALL}")
        else:
            print(f"\n⏳ Estimated time to crack: {crack_time}")

    print("\n📝 Security Recommendations:")
    for f in result['feedback']:
        icon = "✅" if "good" in f.lower() or "strong" in f.lower() else "⚠️"
        if COLOR_ENABLED:
            feedback_color = Fore.GREEN if icon == "✅" else Fore.YELLOW
            print(f"  {feedback_color}{icon} {f}{Style.RESET_ALL}")
        else:
            print(f"  {icon} {f}")
    print("\n" + "="*50)
    if COLOR_ENABLED:
        print(f"{Style.DIM}{Fore.CYAN}Tip: Combine letters, numbers & special characters{Style.RESET_ALL}")
    else:
        print("Tip: Combine letters, numbers & special characters")

if __name__ == "__main__":
    main()