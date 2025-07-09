import tkinter as tk
from tkinter import ttk
from password_strength import PasswordStrengthChecker

# Color scheme
BG_COLOR = "#23272E"  # Slightly deeper background
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#4EC9B0"
ENTRY_BG = "#F3F3F3"  # Softer entry background
ENTRY_FG = "#23272E"  # Darker text for entry
FEEDBACK_BG = "#252526"
STRENGTH_COLORS = {
    "Very Weak": "#FF5555",
    "Weak": "#FFAA33",
    "Medium": "#FFCC00",
    "Strong": "#99CC66",
    "Very Strong": "#4EC9B0"
}

class PasswordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Password Strength Analyzer")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("shield_icon.ico")
        except:
            pass
        self.style = ttk.Style()
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=('Segoe UI', 10))
        self.style.configure("TButton", font=('Segoe UI', 10, 'bold'))
        self.style.configure("TCheckbutton", background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.map("TButton", background=[('active', '#3A9DDB')])
        self.checker = PasswordStrengthChecker()
        main_frame = ttk.Frame(self.root, padding=24, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Header
        header = ttk.Label(main_frame, 
                          text="🔒 Password Strength Analyzer", 
                          font=('Segoe UI', 18, 'bold'),
                          foreground=ACCENT_COLOR,
                          background=BG_COLOR)
        header.pack(pady=(0, 18))
        # Password entry
        entry_frame = ttk.Frame(main_frame, style="TFrame")
        entry_frame.pack(fill=tk.X, pady=8)
        ttk.Label(entry_frame, text="Enter Password:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        self.pw_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.pw_var, show='•', 
                              font=('Segoe UI', 12), width=32,
                              bg=ENTRY_BG, fg=ENTRY_FG,  # Set background and foreground
                              relief='flat', highlightthickness=2,
                              highlightbackground="#4EC9B0", highlightcolor=ACCENT_COLOR,
                              insertbackground=ACCENT_COLOR)
        self.entry.pack(fill=tk.X, pady=7, ipady=7)
        self.entry.bind('<KeyRelease>', self.update)
        self.entry.focus_set()
        # Show password toggle
        self.show_var = tk.IntVar(value=0)
        show_check = ttk.Checkbutton(entry_frame, text="Reveal Password", 
                                    variable=self.show_var, command=self.toggle_show)
        show_check.pack(pady=(5, 18))
        # Strength display
        strength_frame = ttk.Frame(main_frame, style="TFrame")
        strength_frame.pack(fill=tk.X, pady=(10, 7))
        ttk.Label(strength_frame, text="Security Level:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        self.strength_var = tk.StringVar(value="")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var,
                                  font=('Segoe UI', 13, 'bold'))
        self.strength_label.pack(anchor='w', pady=(6, 2))
        # Crack time label
        self.crack_time_var = tk.StringVar(value="")
        self.crack_time_label = ttk.Label(strength_frame, textvariable=self.crack_time_var,
                                  font=('Segoe UI', 10, 'italic'), foreground=ACCENT_COLOR, background=BG_COLOR)
        self.crack_time_label.pack(anchor='w', pady=(0, 10))
        # Strength meter
        self.meter = ttk.Progressbar(main_frame, orient='horizontal', 
                                    length=320, mode='determinate')
        self.meter.pack(fill=tk.X, pady=7)
        # Recommendations
        ttk.Label(main_frame, text="Security Recommendations:", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(18, 7))
        feedback_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, style="TFrame")
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        self.feedback_text = tk.Text(feedback_frame, height=5, width=44, 
                                   font=('Segoe UI', 11), wrap=tk.WORD,
                                   bg=FEEDBACK_BG, fg=TEXT_COLOR,
                                   padx=12, pady=12, borderwidth=0)
        self.feedback_text.pack(fill=tk.BOTH, expand=True)
        self.feedback_text.config(state='disabled')
    def update(self, event=None):
        password = self.pw_var.get()
        result = self.checker.check(password)
        # Update strength display
        strength = result['strength']
        score = result['score']
        self.strength_var.set(f"{strength}")
        self.strength_label.configure(foreground=STRENGTH_COLORS.get(strength, TEXT_COLOR))
        # Update crack time
        crack_time = result.get('crack_time', None)
        if crack_time:
            self.crack_time_var.set(f"Estimated time to crack: {crack_time}")
        else:
            self.crack_time_var.set("")
        # Update progress meter
        meter_value = (score / 5) * 100
        self.meter['value'] = meter_value
        self.meter['style'] = 'TProgressbar'
        # Custom progress bar color
        if score < 2:
            self.meter.configure(style="red.Horizontal.TProgressbar")
        elif score < 4:
            self.meter.configure(style="yellow.Horizontal.TProgressbar")
        else:
            self.meter.configure(style="green.Horizontal.TProgressbar")
        # Update feedback
        self.feedback_text.config(state='normal')
        self.feedback_text.delete('1.0', tk.END)
        for f in result['feedback']:
            icon = "✅" if "good" in f.lower() or "strong" in f.lower() else "⚠️"
            self.feedback_text.insert(tk.END, f"{icon} {f}\n")
        self.feedback_text.config(state='disabled')
    def toggle_show(self):
        if self.show_var.get():
            self.entry.config(show='')
        else:
            self.entry.config(show='•')
def main():
    root = tk.Tk()
    # Configure custom progress bar styles
    style = ttk.Style()
    style.configure("red.Horizontal.TProgressbar", 
                   background='#FF5555', troughcolor=BG_COLOR)
    style.configure("yellow.Horizontal.TProgressbar", 
                   background='#FFCC00', troughcolor=BG_COLOR)
    style.configure("green.Horizontal.TProgressbar", 
                   background='#4EC9B0', troughcolor=BG_COLOR)
    PasswordGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()