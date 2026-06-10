import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.pushDecrypt.clicked.connect(self.call_api_decrypt)
       
    def validate_key(self, text_length):
        key = self.ui.textKey.toPlainText()
        
        if not key.isdigit():
            QMessageBox.warning(self, "Khoa khong hop le", "Khoa phai la so nguyen.")
            return False
        
        key = int(key)
        
        if key <= 1:
            QMessageBox.warning(self, "Khoa khong hop le", "Khoa phai lon hon 1.")
            return False
            
        if key >= text_length:
            QMessageBox.warning(self, "Khoa khong hop le", "Khoa phai nho hon do dai chuoi van ban.")
            return False

        return True

    def call_api_encrypt(self):
        plaintext = self.ui.textPlainText.toPlainText()
        
        if not self.validate_key(len(plaintext)):
            return
            
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plaintext,
            "key": self.ui.textKey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textCipherText.setText(data["encrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Error while calling API")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Connection Error")
            msg.setText(f"Could not connect to server: {str(e)}")
            msg.exec_()

    def call_api_decrypt(self):
        ciphertext = self.ui.textCipherText.toPlainText()
        
        if not self.validate_key(len(ciphertext)):
            return
            
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": ciphertext,
            "key": self.ui.textKey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textPlainText.setText(data["decrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Error while calling API")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Connection Error")
            msg.setText(f"Could not connect to server: {str(e)}")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
