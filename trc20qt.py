import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt6.QtGui import QIntValidator
from tronpy import Tron
from tronpy.keys import PrivateKey

class WalletGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Private key input
        private_key_layout = QHBoxLayout()
        private_key_label = QLabel("Private Key (optional):")
        self.private_key_input = QLineEdit()
        private_key_layout.addWidget(private_key_label)
        private_key_layout.addWidget(self.private_key_input)
        layout.addLayout(private_key_layout)

        # Number of wallets input
        num_wallets_layout = QHBoxLayout()
        num_wallets_label = QLabel("Number of Wallets:")
        self.num_wallets_input = QLineEdit()
        self.num_wallets_input.setValidator(QIntValidator(1, 100))  # Limit input to integers between 1 and 100
        num_wallets_layout.addWidget(num_wallets_label)
        num_wallets_layout.addWidget(self.num_wallets_input)
        layout.addLayout(num_wallets_layout)

        # Generate button
        generate_button = QPushButton("Generate Wallets")
        generate_button.clicked.connect(self.generate_wallets)
        layout.addWidget(generate_button)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        self.setLayout(layout)
        self.setWindowTitle('USDT TRC20 Wallet Generator')
        self.setGeometry(300, 300, 500, 400)

    def generate_wallets(self):
        try:
            private_key = self.private_key_input.text().strip()
            num_wallets_text = self.num_wallets_input.text().strip()

            if not num_wallets_text:
                raise ValueError("Please enter the number of wallets to generate.")

            num_wallets = int(num_wallets_text)
            if num_wallets <= 0 or num_wallets > 100:
                raise ValueError("Number of wallets must be between 1 and 100.")

            tron = Tron()
            usdt_contract = tron.get_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")  # USDT TRC20 contract address

            results = []
            if private_key:
                try:
                    priv_key = PrivateKey(bytes.fromhex(private_key))
                    address = priv_key.public_key.to_base58check_address()
                    wallet_info = f"Address: {address}\nPrivate Key: {priv_key.hex()}\n\n"
                    results.append(wallet_info)
                except ValueError:
                    raise ValueError("Invalid private key format. Please provide a valid hexadecimal private key.")
            
            for _ in range(num_wallets - len(results)):
                priv_key = PrivateKey.random()
                address = priv_key.public_key.to_base58check_address()
                wallet_info = f"Address: {address}\nPrivate Key: {priv_key.hex()}\n\n"
                results.append(wallet_info)

            self.results_display.setText("".join(results))
            QMessageBox.information(self, "Success", f"Successfully generated {num_wallets} wallet(s).")

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WalletGenerator()
    ex.show()
    sys.exit(app.exec())