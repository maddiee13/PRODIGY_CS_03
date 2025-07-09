# Password Strength Analyzer (CLI & GUI)

A modern tool to assess your password's strength and security, featuring both a beautiful cross-platform GUI and a user-friendly CLI. The tool provides detailed feedback, a strength score, and estimates how long it would take for your password to be cracked by an attacker.

## Features

- **Password Strength Analysis:** Checks for length, uppercase, lowercase, digits, and special characters.
- **Security Feedback:** Gives actionable feedback and a clear strength score.
- **Crack Time Estimation:** Estimates how long it would take to crack your password using modern attack methods.
- **Visual Strength Meter:** See your password's security level at a glance.
- **CLI & GUI:** Use in the terminal or with a modern Tkinter-based graphical interface.
- **Cross-platform:** Works on Windows, Mac, and Linux.

## Requirements

- Python 3.7 or higher
- [colorama](https://pypi.org/project/colorama/) (for colored CLI output)
- Tkinter (usually included with Python, for GUI)

### Optional
- [ttkthemes](https://pypi.org/project/ttkthemes/) (for enhanced GUI appearance)

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### CLI

Run the CLI tool in your terminal:

```bash
python Cli.py
```

- Enter your password when prompted. The tool will display the strength, estimated crack time, and security recommendations.

### GUI

Run the GUI tool:

```bash
python Gui.py
```

- Enter your password in the input field. The GUI will show the strength, estimated crack time, and recommendations in real time.

## Output Example (CLI)

```
🔒 Password Strength Analyzer

> Password: ********

🔐 Strength: Strong
██████████---------- (3/5)
⏳ Estimated time to crack: 2 days, 4 hours
📝 Security Recommendations:
  ⚠️ Add special characters (!@#$%^&*)
  ✅ Good password length (14+ characters)

Tip: Combine letters, numbers & special characters
```

## License

MIT License
