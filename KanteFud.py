import sys
import base64
import zlib
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os

def random_string(length):
    characters = string.ascii_letters + string.digits
    first_char = random.choice(string.ascii_letters)
    remaining_chars = ''.join(random.choice(characters) for _ in range(length - 1))
    return first_char + remaining_chars

class AnnenMayKantereitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnnenMayKantereit v2")
        self.geometry("800x600")
        self.configure(bg="#000000")

        try:
            self.logo = tk.PhotoImage(file="AnnenMayKante.png")
            self.logo_label = tk.Label(self, image=self.logo, bg="#000000")
            self.logo_label.pack(pady=10)
        except Exception:
            self.logo_label = tk.Label(self, text="[Logo yüklenemedi]", fg="#FF0000", bg="#000000", font=("Arial", 14))
            self.logo_label.pack(pady=10)

        self.file_button = tk.Button(self, text="Python Dosyası Seç", command=self.select_file,
                                     bg="#c4151c", fg="#FFFFFF", font=("Arial", 12, "bold"), relief=tk.RAISED, bd=2)
        self.file_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.message_label = tk.Label(self, text="Created by AnnenMayKantereit", bg="#000000",
                                      fg="#FFFFFF", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Python Dosyası Seç", filetypes=[("Python Dosyaları", "*.py")])
        if file_path:
            self.encrypt(file_path)

    def encrypt(self, file_path):
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                original_code = f.read()

            compressed = zlib.compress(original_code.encode())
            encoded = base64.b64encode(compressed).decode()

            var_encoded = random_string(8)
            var_compressed = random_string(8)
            var_decoded = random_string(8)

            loader_code = f"""
import base64
import zlib

{var_encoded} = "{encoded}"
{var_compressed} = base64.b64decode({var_encoded})
{var_decoded} = zlib.decompress({var_compressed}).decode()
exec({var_decoded})
"""

            original_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file = f"obfuscated_{original_name}_{random_string(5)}.py"

            with open(output_file, "w", encoding='utf-8') as f:
                f.write(loader_code.strip())

            self.result_label.config(text=f"✅ Obfuscation başarılı: {output_file}")
        except Exception as e:
            self.result_label.config(text=f"❌ Hata: {str(e)}")

if __name__ == '__main__':
    app = AnnenMayKantereitApp()
    app.mainloop()
