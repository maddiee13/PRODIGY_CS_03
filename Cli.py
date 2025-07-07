import sys
from password_strength import PasswordStrengthChecker
import getpass

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

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
    print(f"\n{Style.BRIGHT}=== 🔒 Password Strength Analyzer ===")
    print("Enter your password below for security evaluation\n")
    
    password = getpass.getpass("> Password: ")
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
    
    print("\n📝 Security Recommendations:")
    for f in result['feedback']:
        print(f"  • {f}")
    
    print("\n" + "="*50)
    print(f"{Style.DIM}Tip: Combine letters, numbers & special characters{Style.RESET_ALL}")

if __name__ == "__main__":
    main()