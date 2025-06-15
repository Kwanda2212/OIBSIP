import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import secrets
import pyperclip
import re
from typing import List, Dict

class PasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Password Generator")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Password history
        self.password_history = []
        
        # Character sets
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'numbers': string.digits,
            'symbols': "!@#$%^&*()_+-=[]{}|;:,.<>?",
            'similar': "il1Lo0O",
            'ambiguous': "{}[]()/\\'\"`~,;.<>"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Password Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password length
        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.StringVar(value="12")
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.length_entry = ttk.Entry(length_frame, textvariable=self.length_var, width=10)
        self.length_entry.pack(side=tk.LEFT)
        
        self.length_scale = ttk.Scale(length_frame, from_=4, to=128, orient=tk.HORIZONTAL,
                                     variable=self.length_var, command=self.update_length_entry)
        self.length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Character type options
        char_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="10")
        char_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        char_frame.columnconfigure(1, weight=1)
        
        self.char_vars = {}
        char_options = [
            ('lowercase', 'Lowercase letters (a-z)', True),
            ('uppercase', 'Uppercase letters (A-Z)', True),
            ('numbers', 'Numbers (0-9)', True),
            ('symbols', 'Symbols (!@#$%^&*)', True)
        ]
        
        for i, (key, label, default) in enumerate(char_options):
            self.char_vars[key] = tk.BooleanVar(value=default)
            ttk.Checkbutton(char_frame, text=label, variable=self.char_vars[key]).grid(
                row=i, column=0, sticky=tk.W, pady=2)
        
        # Security rules
        security_frame = ttk.LabelFrame(main_frame, text="Security Rules", padding="10")
        security_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.security_vars = {}
        security_options = [
            ('min_uppercase', 'Minimum uppercase letters:', 1),
            ('min_lowercase', 'Minimum lowercase letters:', 1),
            ('min_numbers', 'Minimum numbers:', 1),
            ('min_symbols', 'Minimum symbols:', 1),
            ('exclude_similar', 'Exclude similar characters (il1Lo0O)', True),
            ('exclude_ambiguous', 'Exclude ambiguous characters ({}[]/\\)', False),
            ('no_repeating', 'No repeating characters', False)
        ]
        
        for i, option in enumerate(security_options):
            if len(option) == 3 and isinstance(option[2], bool):
                key, label, default = option
                self.security_vars[key] = tk.BooleanVar(value=default)
                ttk.Checkbutton(security_frame, text=label, 
                               variable=self.security_vars[key]).grid(
                    row=i, column=0, columnspan=2, sticky=tk.W, pady=2)
            else:
                key, label, default = option
                ttk.Label(security_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
                self.security_vars[key] = tk.StringVar(value=str(default))
                ttk.Entry(security_frame, textvariable=self.security_vars[key], 
                         width=5).grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Custom exclusions
        exclusion_frame = ttk.LabelFrame(main_frame, text="Custom Character Exclusions", padding="10")
        exclusion_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        exclusion_frame.columnconfigure(1, weight=1)
        
        ttk.Label(exclusion_frame, text="Exclude characters:").grid(row=0, column=0, sticky=tk.W)
        self.exclude_var = tk.StringVar()
        ttk.Entry(exclusion_frame, textvariable=self.exclude_var).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Generation options
        gen_frame = ttk.Frame(main_frame)
        gen_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Label(gen_frame, text="Number of passwords:").pack(side=tk.LEFT)
        self.count_var = tk.StringVar(value="1")
        ttk.Entry(gen_frame, textvariable=self.count_var, width=5).pack(side=tk.LEFT, padx=(10, 20))
        
        # Generate button
        self.generate_btn = ttk.Button(gen_frame, text="Generate Password(s)", 
                                      command=self.generate_passwords,
                                      style='Accent.TButton')
        self.generate_btn.pack(side=tk.LEFT)
        
        # Password display
        display_frame = ttk.LabelFrame(main_frame, text="Generated Passwords", padding="10")
        display_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)
        
        # Password text area
        self.password_text = scrolledtext.ScrolledText(display_frame, height=8, width=60)
        self.password_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Buttons frame
        btn_frame = ttk.Frame(display_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear_passwords).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Save to File", 
                  command=self.save_to_file).pack(side=tk.LEFT)
        
        # Password strength indicator
        strength_frame = ttk.Frame(main_frame)
        strength_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        strength_frame.columnconfigure(1, weight=1)
        
        ttk.Label(strength_frame, text="Password Strength:").grid(row=0, column=0, sticky=tk.W)
        self.strength_var = tk.StringVar(value="Generate a password to see strength")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var)
        self.strength_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Progress bar for strength
        self.strength_progress = ttk.Progressbar(strength_frame, length=200, mode='determinate')
        self.strength_progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Bind events
        self.length_entry.bind('<KeyRelease>', self.update_length_scale)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(6, weight=1)
        
    def update_length_entry(self, value):
        """Update length entry when scale changes"""
        self.length_var.set(str(int(float(value))))
        
    def update_length_scale(self, event):
        """Update scale when entry changes"""
        try:
            value = int(self.length_var.get())
            if 4 <= value <= 128:
                self.length_scale.set(value)
        except ValueError:
            pass
    
    def validate_inputs(self) -> tuple[bool, str]:
        """Validate user inputs"""
        try:
            length = int(self.length_var.get())
            if length < 4 or length > 128:
                return False, "Password length must be between 4 and 128 characters"
        except ValueError:
            return False, "Invalid password length"
        
        # Check if at least one character type is selected
        if not any(var.get() for var in self.char_vars.values()):
            return False, "At least one character type must be selected"
        
        # Validate minimum requirements
        total_minimum = 0
        for key in ['min_uppercase', 'min_lowercase', 'min_numbers', 'min_symbols']:
            try:
                min_val = int(self.security_vars[key].get())
                if min_val < 0:
                    return False, f"Minimum values cannot be negative"
                total_minimum += min_val
            except ValueError:
                return False, f"Invalid minimum value for {key}"
        
        if total_minimum > length:
            return False, "Sum of minimum requirements exceeds password length"
        
        try:
            count = int(self.count_var.get())
            if count < 1 or count > 100:
                return False, "Number of passwords must be between 1 and 100"
        except ValueError:
            return False, "Invalid number of passwords"
        
        return True, ""
    
    def build_character_set(self) -> str:
        """Build the character set based on user selections"""
        charset = ""
        
        # Add selected character types
        for char_type, include in self.char_vars.items():
            if include.get():
                charset += self.char_sets[char_type]
        
        # Remove excluded characters
        if self.security_vars.get('exclude_similar', tk.BooleanVar()).get():
            charset = ''.join(c for c in charset if c not in self.char_sets['similar'])
        
        if self.security_vars.get('exclude_ambiguous', tk.BooleanVar()).get():
            charset = ''.join(c for c in charset if c not in self.char_sets['ambiguous'])
        
        # Remove custom exclusions
        custom_exclude = self.exclude_var.get()
        if custom_exclude:
            charset = ''.join(c for c in charset if c not in custom_exclude)
        
        # Remove duplicates while preserving order
        seen = set()
        charset = ''.join(c for c in charset if not (c in seen or seen.add(c)))
        
        return charset
    
    def generate_single_password(self, length: int, charset: str) -> str:
        """Generate a single password meeting all requirements"""
        max_attempts = 1000
        
        for _ in range(max_attempts):
            password = ''.join(secrets.choice(charset) for _ in range(length))
            
            if self.meets_requirements(password):
                return password
        
        # If we can't meet requirements with random generation, 
        # build password strategically
        return self.build_compliant_password(length, charset)
    
    def meets_requirements(self, password: str) -> bool:
        """Check if password meets all security requirements"""
        # Check minimum character type requirements
        requirements = {
            'min_uppercase': sum(1 for c in password if c.isupper()),
            'min_lowercase': sum(1 for c in password if c.islower()),
            'min_numbers': sum(1 for c in password if c.isdigit()),
            'min_symbols': sum(1 for c in password if c in self.char_sets['symbols'])
        }
        
        for req_type, actual_count in requirements.items():
            try:
                required_count = int(self.security_vars[req_type].get())
                if actual_count < required_count:
                    return False
            except (ValueError, KeyError):
                pass
        
        # Check no repeating characters
        if self.security_vars.get('no_repeating', tk.BooleanVar()).get():
            if len(set(password)) != len(password):
                return False
        
        return True
    
    def build_compliant_password(self, length: int, charset: str) -> str:
        """Build a password that meets all requirements"""
        password = []
        remaining_length = length
        
        # Add minimum required characters
        char_pools = {
            'min_uppercase': [c for c in charset if c.isupper()],
            'min_lowercase': [c for c in charset if c.islower()],
            'min_numbers': [c for c in charset if c.isdigit()],
            'min_symbols': [c for c in charset if c in self.char_sets['symbols']]
        }
        
        for req_type, pool in char_pools.items():
            if not pool:
                continue
            try:
                required_count = int(self.security_vars[req_type].get())
                for _ in range(min(required_count, remaining_length)):
                    if self.security_vars.get('no_repeating', tk.BooleanVar()).get():
                        available = [c for c in pool if c not in password]
                        if available:
                            password.append(secrets.choice(available))
                            remaining_length -= 1
                    else:
                        password.append(secrets.choice(pool))
                        remaining_length -= 1
            except (ValueError, KeyError):
                pass
        
        # Fill remaining positions
        available_chars = list(charset)
        if self.security_vars.get('no_repeating', tk.BooleanVar()).get():
            available_chars = [c for c in available_chars if c not in password]
        
        while remaining_length > 0 and available_chars:
            char = secrets.choice(available_chars)
            password.append(char)
            remaining_length -= 1
            
            if self.security_vars.get('no_repeating', tk.BooleanVar()).get():
                available_chars.remove(char)
        
        # Shuffle the password
        password_list = list(password)
        random.shuffle(password_list)
        
        return ''.join(password_list)
    
    def calculate_strength(self, password: str) -> tuple[int, str]:
        """Calculate password strength score and description"""
        score = 0
        factors = []
        
        # Length scoring
        length = len(password)
        if length >= 12:
            score += 25
            factors.append("Good length")
        elif length >= 8:
            score += 15
            factors.append("Adequate length")
        else:
            factors.append("Too short")
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.char_sets['symbols'] for c in password)
        
        variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
        score += variety_count * 15
        
        if variety_count >= 3:
            factors.append("Good character variety")
        
        # Entropy calculation
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += len(self.char_sets['symbols'])
        
        if charset_size > 0:
            import math
            entropy = length * math.log2(charset_size)
            if entropy >= 60:
                score += 20
                factors.append("High entropy")
            elif entropy >= 40:
                score += 10
                factors.append("Medium entropy")
        
        # Pattern detection (basic)
        if not re.search(r'(.)\1{2,}', password):  # No 3+ repeating chars
            score += 10
            factors.append("No obvious patterns")
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Medium"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return min(score, 100), f"{strength} ({', '.join(factors)})"
    
    def generate_passwords(self):
        """Generate passwords based on user settings"""
        # Validate inputs
        valid, error_msg = self.validate_inputs()
        if not valid:
            messagebox.showerror("Invalid Input", error_msg)
            return
        
        try:
            length = int(self.length_var.get())
            count = int(self.count_var.get())
            
            # Build character set
            charset = self.build_character_set()
            if not charset:
                messagebox.showerror("Error", "No characters available for password generation")
                return
            
            # Generate passwords
            passwords = []
            for _ in range(count):
                password = self.generate_single_password(length, charset)
                passwords.append(password)
            
            # Display passwords
            self.password_text.delete(1.0, tk.END)
            for i, password in enumerate(passwords, 1):
                if count > 1:
                    self.password_text.insert(tk.END, f"Password {i}: {password}\n")
                else:
                    self.password_text.insert(tk.END, password)
            
            # Update strength indicator for first password
            if passwords:
                score, description = self.calculate_strength(passwords[0])
                self.strength_var.set(description)
                self.strength_progress['value'] = score
                
                # Update progress bar color based on strength
                if score >= 80:
                    self.style.configure("Strength.Horizontal.TProgressbar", 
                                       troughcolor='lightgray', background='green')
                elif score >= 60:
                    self.style.configure("Strength.Horizontal.TProgressbar", 
                                       troughcolor='lightgray', background='orange')
                else:
                    self.style.configure("Strength.Horizontal.TProgressbar", 
                                       troughcolor='lightgray', background='red')
                
                self.strength_progress.configure(style="Strength.Horizontal.TProgressbar")
            
            # Add to history
            self.password_history.extend(passwords)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy generated passwords to clipboard"""
        password_content = self.password_text.get(1.0, tk.END).strip()
        if password_content:
            try:
                pyperclip.copy(password_content)
                messagebox.showinfo("Success", "Passwords copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No passwords to copy")
    
    def clear_passwords(self):
        """Clear the password display"""
        self.password_text.delete(1.0, tk.END)
        self.strength_var.set("Generate a password to see strength")
        self.strength_progress['value'] = 0
    
    def save_to_file(self):
        """Save passwords to a file"""
        password_content = self.password_text.get(1.0, tk.END).strip()
        if not password_content:
            messagebox.showwarning("Warning", "No passwords to save")
            return
        
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(password_content)
                messagebox.showinfo("Success", f"Passwords saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("Warning: pyperclip not installed. Clipboard functionality will be limited.")
        print("Install with: pip install pyperclip")
        
        # Create a mock pyperclip for basic functionality
        class MockPyperclip:
            @staticmethod
            def copy(text):
                print(f"Would copy to clipboard: {text}")
        
        pyperclip = MockPyperclip()
    
    app = PasswordGenerator()
    app.run()