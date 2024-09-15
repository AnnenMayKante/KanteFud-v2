import os
import zlib
import random
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes, padding
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QFileDialog
import webbrowser

# Dinamik olarak anahtar üret
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# RSA ile AES anahtarını şifrele
def rsa_encrypt_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# RSA ile şifrelenmiş anahtarı çöz
def rsa_decrypt_key(encrypted_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key

# AES ile şifreleme
def aes_encrypt(plaintext, key, iv):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted

# AES ile şifre çözme
def aes_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode()

# GUI uygulaması
class AnnenMayKantereitApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AnnenMayKantereit v1.0")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon('AnnenMayKante.png'))
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        self.setStyleSheet("background-color: #000000;")

        self.logo = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('AnnenMayKante.png')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.logo)

        font = QtGui.QFont("Arial", 12)
        self.setFont(font)

        self.file_button = QPushButton("Select Python File", self)
        self.file_button.setStyleSheet("background-color: #c4151c; color: white; padding: 10px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)
        main_layout.addWidget(self.file_button)

        self.result_label = QLabel("", self)
        self.result_label.setStyleSheet("color: #333333; font-size: 12px; padding: 10px;")
        main_layout.addWidget(self.result_label)

        self.message_label = QLabel("Created by AnnenMayKantereit", self)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 12px; color: #555555;")
        main_layout.addWidget(self.message_label)

        main_layout.addStretch()

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.py)")
        if file_name:
            self.encrypt(file_name)

    def encrypt(self, file_name):
        with open(file_name, "r") as f:
            original_code = f.read()

        import_lines = []
        for line in original_code.split('\n'):
            if line.strip().startswith('import') or line.strip().startswith('from'):
                import_lines.append(line)

        key = os.urandom(32)  # AES anahtarı
        iv = os.urandom(16)  # Başlangıç vektörü

        private_key, public_key = generate_rsa_key_pair()  # RSA anahtar çiftini üret
        encrypted_key = rsa_encrypt_key(key, public_key)  # AES anahtarını RSA ile şifrele

        compressed_code = zlib.compress(original_code.encode())
        encrypted_code = aes_encrypt(compressed_code.decode('latin1'), key, iv)

        decode_function = '''
import zlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes

def rsa_decrypt_key(encrypted_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key

def aes_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode()

private_key = ... # RSA özel anahtarı
encrypted_key = {encrypted_key}

key = rsa_decrypt_key(encrypted_key, private_key)
iv = {iv}

compressed_code = aes_decrypt(encrypted_code, key, iv)
original_code = zlib.decompress(compressed_code.encode('latin1')).decode()
exec(original_code)
'''.format(encrypted_key=repr(encrypted_key), iv=repr(iv))

        with open("obfuscated_code.py", "w") as f:
            f.write(decode_function)

        self.result_label.setText("Code encrypted with RSA-AES and saved as 'obfuscated_code.py'.")

    def open_documentation(self):
        webbrowser.open("https://learn.microsoft.com/en-us/dotnet/framework/tools/signtool-exe")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = AnnenMayKantereitApp()
    window.show()
    app.exec_()
