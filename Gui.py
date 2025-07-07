import tkinter as tk
from tkinter import ttk
from password_strength import PasswordStrengthChecker

# Color scheme
BG_COLOR = "#2D2D30"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#4EC9B0"
ENTRY_BG = "#FFFFFF"  # Changed to light background
ENTRY_FG = "#000000"  # Changed to black text
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
        
        # Set window icon
        try:
            self.root.iconbitmap("shield_icon.ico")
        except:
            pass

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=('Segoe UI', 10))
        self.style.configure("TButton", font=('Segoe UI', 10, 'bold'))
        self.style.configure("TCheckbutton", background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.map("TButton", background=[('active', '#3A9DDB')])

        self.checker = PasswordStrengthChecker()

        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, 
                          text="🔒 Password Strength Analyzer", 
                          font=('Segoe UI', 14, 'bold'),
                          foreground=ACCENT_COLOR)
        header.pack(pady=(0, 15))

        # Password entry
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entry_frame, text="Enter Password:", font=('Segoe UI', 10)).pack(anchor='w')
        
        self.pw_var = tk.StringVar()
        # Create entry with custom colors
        self.entry = tk.Entry(entry_frame, textvariable=self.pw_var, show='•', 
                              font=('Segoe UI', 11), width=30,
                              bg=ENTRY_BG, fg=ENTRY_FG,  # Set background and foreground
                              relief='flat', highlightthickness=1,
                              highlightbackground="#555555", highlightcolor=ACCENT_COLOR)
        self.entry.pack(fill=tk.X, pady=5, ipady=5)
        self.entry.bind('<KeyRelease>', self.update)
        self.entry.focus_set()

        # Show password toggle
        self.show_var = tk.IntVar(value=0)
        show_check = ttk.Checkbutton(entry_frame, text="Reveal Password", 
                                    variable=self.show_var, command=self.toggle_show)
        show_check.pack(pady=(5, 15))

        # Strength display
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(strength_frame, text="Security Level:", font=('Segoe UI', 10)).pack(anchor='w')
        
        self.strength_var = tk.StringVar(value="")
        strength_label = ttk.Label(strength_frame, textvariable=self.strength_var,
                                  font=('Segoe UI', 12, 'bold'))
        strength_label.pack(anchor='w', pady=(5, 10))

        # Strength meter
        self.meter = ttk.Progressbar(main_frame, orient='horizontal', 
                                    length=300, mode='determinate')
        self.meter.pack(fill=tk.X, pady=5)

        # Recommendations
        ttk.Label(main_frame, text="Security Recommendations:", 
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(15, 5))
        
        feedback_frame = ttk.Frame(main_frame, relief=tk.SUNKEN)
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        feedback_frame.configure(style='TFrame')
        
        self.feedback_text = tk.Text(feedback_frame, height=5, width=40, 
                                   font=('Segoe UI', 10), wrap=tk.WORD,
                                   bg=FEEDBACK_BG, fg=TEXT_COLOR,
                                   padx=10, pady=10, borderwidth=0)
        self.feedback_text.pack(fill=tk.BOTH, expand=True)
        self.feedback_text.config(state='disabled')

    def update(self, event=None):
        password = self.pw_var.get()
        result = self.checker.check(password)
        
        # Update strength display
        strength = result['strength']
        score = result['score']
        self.strength_var.set(f"{strength}")
        self.strength_label = ttk.Label()
        self.strength_label.configure(foreground=STRENGTH_COLORS.get(strength, TEXT_COLOR))
        
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
            self.feedback_text.insert(tk.END, f"• {f}\n")
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