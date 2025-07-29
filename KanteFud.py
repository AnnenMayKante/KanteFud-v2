import base64
import zlib
import random
import string
import tkinter as tk
from tkinter import filedialog
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def pad(data):
    pad_len = AES.block_size - len(data.encode()) % AES.block_size
    return data + chr(pad_len) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

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
                                     bg="#c4151c", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.file_button.pack(pady=20)

        self.result_label = tk.Label(self, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Python Dosyası Seç", filetypes=[("Python Dosyaları", "*.py")])
        if file_path:
            self.encrypt(file_path)

    def encrypt(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()

            key = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC)
            iv = cipher.iv
            padded = pad(original_code)
            encrypted = cipher.encrypt(padded.encode())
            b64_encrypted = base64.b64encode(iv + encrypted).decode()

            var_data = random_string(8)
            var_key = random_string(8)
            var_dec = random_string(8)
            var_exec = random_string(8)

            loader_code = f"""
import base64
from Crypto.Cipher import AES

def unpad(data):
    return data[:-data[-1]]

{var_key} = base64.b64decode("{base64.b64encode(key).decode()}")
{var_data} = base64.b64decode("{b64_encrypted}")
cipher = AES.new({var_key}, AES.MODE_CBC, iv={var_data}[:16])
{var_dec} = cipher.decrypt({var_data}[16:])
{var_exec} = unpad({var_dec}).decode()
exec({var_exec})
"""

            output_name = f"obfuscated_{random_string(5)}.py"
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(loader_code.strip())

            self.result_label.config(text=f"✅ AES obfuscation başarılı: {output_name}")

        except Exception as e:
            self.result_label.config(text=f"❌ Hata: {str(e)}")

if __name__ == '__main__':
    app = AnnenMayKantereitApp()
    app.mainloop()
