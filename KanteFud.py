import sys
import base64
import zlib
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
from urllib.parse import quote

def random_string(length):
    characters = string.ascii_letters + string.digits
    first_char = random.choice(string.ascii_letters)
    remaining_chars = ''.join(random.choice(characters) for _ in range(length - 1))
    return first_char + remaining_chars

class AnnenMayKantereitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnnenMayKantereit v1.5")
        self.geometry("800x600")
        self.configure(bg="#000000")  # Siyah arka plan

        self.logo = tk.PhotoImage(file="AnnenMayKante.png")
        self.logo_label = tk.Label(self, image=self.logo, bg="#000000")  # Arka plan rengiyle uyumlu
        self.logo_label.pack(pady=10)

        self.file_button = tk.Button(self, text="Python Dosyası Seç", command=self.select_file,
                                      bg="#c4151c", fg="#FFFFFF", font=("Arial", 12, "bold"),
                                      relief=tk.RAISED, bd=2)
        self.file_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.message_label = tk.Label(self, text="Created by AnnenMayKantereit", bg="#000000", fg="#FFFFFF", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Python Dosyası Seç", filetypes=(("Python Dosyaları", "*.py"),))
        if file_path:
            self.encrypt(file_path)

    def encrypt(self, file_path):
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                original_code = f.read()

            import_lines = []
            for line in original_code.split('\n'):
                if line.strip().startswith('import') or line.strip().startswith('from'):
                    import_lines.append(line)

            compressed_code = zlib.compress(original_code.encode())
            encoded_code = base64.b64encode(compressed_code).decode()

            decode_function = '''
import base64
import zlib

{imports}
encoded_code = "{encoded_code}"
compressed_code = base64.b64decode(encoded_code)
original_code = zlib.decompress(compressed_code).decode()
exec(original_code)
'''.format(imports='\n'.join(import_lines), encoded_code=encoded_code)

            obfuscated_code = decode_function.replace('encoded_code', random_string(10)).replace('compressed_code', random_string(10)).replace('original_code', random_string(10))

            with open("obfuscated_code.py", "w", encoding='utf-8') as f:
                f.write(obfuscated_code)

            self.result_label.config(text="Kod obfuscate edildi ve 'obfuscated_code.py' olarak kaydedildi.")
        except UnicodeDecodeError as e:
            self.result_label.config(text=f"Hata: {str(e)}")
        except Exception as e:
            self.result_label.config(text=f"Bir hata oluştu: {str(e)}")

    def open_documentation(self):
        documentation_url = "https://example.com/SignTool_Documentation"
        webbrowser.open(documentation_url)

if __name__ == '__main__':
    app = AnnenMayKantereitApp()
    app.mainloop()
