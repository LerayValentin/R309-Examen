
"""
https://github.com/LerayValentin/R309-Examen
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit
from PyQt6.QtCore import QCoreApplication
import socket
import threading
etat_serveur = False
client_connected = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        label_serveur = QLabel("Serveur :")
        label_port = QLabel("Port :")
        label_nbr = QLabel("Nombre de clients maximum :")
        self.input_serveur = QLineEdit()
        self.input_serveur.setText('0.0.0.0')
        self.input_port = QLineEdit()
        self.input_port.setText('4200')
        self.input_nbr = QLineEdit()
        self.input_nbr.setText('5')
        self.bouton = QPushButton("Démarrage du serveur")
        self.affichage = QTextEdit()
        self.quit = QPushButton("Quitter")

        grid.addWidget(label_serveur, 0, 0)
        grid.addWidget(label_port, 1, 0)
        grid.addWidget(label_nbr, 2, 0)
        grid.addWidget(self.input_serveur, 0, 1)
        grid.addWidget(self.input_port, 1, 1)
        grid.addWidget(self.input_nbr, 2, 1)
        grid.addWidget(self.bouton, 3, 0, 1, 2)
        grid.addWidget(self.affichage, 4, 0, 1, 2)
        grid.addWidget(self.quit, 5, 0, 1, 2)

        self.bouton.clicked.connect(self.__demarrage)
        self.quit.clicked.connect(self.__quitter)

        self.setWindowTitle("Le serveur de tchat")
        self.resize(375,500)


    def __quitter(self):
        QCoreApplication.exit(0)

    def __demarrage(self):
        global etat_serveur
        global serveur
        if etat_serveur :
            self.bouton.setText('Démarrage du serveur')
            etat_serveur = False
        else:
            self.bouton.setText('Arrêt du serveur')
            etat_serveur = True
        serveur = socket.socket()
        nbr = int(self.input_nbr.text())
        port = int(self.input_port.text())
        serveur.bind((self.input_serveur.text(), port))
        serveur.listen(nbr)
        self.affichage.setText('en attente de connexion...\n')
        thread_accept = threading.Thread(target=self.__accept)
        
    def __accept(self):
        global etat_serveur, client_connected, conn, serveur, addr
        while etat_serveur:
            try:
                conn, addr = serveur.accept()
                client_connected = True
            except OSError:
                pass
            else:
                __gerer_client(conn, addr)
        
    def __gerer_client(conn, addr):
        global etat_serveur, client_connected
        while client_connected:
            try:
                message = conn.recv(1024).decode()
                self.affichage.setText(f'Message reçu : {message}')
                if message == 'deco-server':
                    client_connected = False
            except ConnectionResetError:
                print(f"connexion perdue avec {addr}")
                break

        conn.close()
        print(f"Connexion fermee avec {addr}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




