
import mysql.connector
from mysql.connector import Error
from models import Produit, Client


class MySQLDAO:

    def __init__(self, host="localhost", user="root", password=""):
        self.config = {
            "host": host,
            "user": user,
            "password": password
        }

        try:
            # Connexion au serveur
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            # Création de la base
            cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")
            cursor.close()
            self.conn.close()

            # Connexion à la base boutique
            self.conn = mysql.connector.connect(
                **self.config,
                database="boutique"
            )

            self.creer_tables()

        except Error as e:
            print("Erreur de connexion MySQL :", e)
            raise

    def creer_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prix FLOAT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL
            )
        """)

        self.conn.commit()
        cursor.close()

    def ajouter_produit(self, produit):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO produits (nom, prix) VALUES (%s, %s)",
                (produit.nom, produit.prix)
            )
            self.conn.commit()
            cursor.close()
            print("Produit ajouté avec succès.")

        except Error as e:
            print("Erreur MySQL :", e)

    def lister_produits(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM produits")

        for p in cursor.fetchall():
            print(Produit(p[0], p[1], p[2]))

        cursor.close()

    def ajouter_client(self, client):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO clients (nom, email) VALUES (%s, %s)",
                (client.nom, client.email)
            )
            self.conn.commit()
            cursor.close()
            print("Client ajouté avec succès.")

        except Error as e:
            print("Erreur MySQL :", e)

    def lister_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients")

        for c in cursor.fetchall():
            print(Client(c[0], c[1], c[2]))

        cursor.close()

    def rechercher_client(self, email):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM clients WHERE email = %s",
            (email,)
        )

        c = cursor.fetchone()

        if c:
            print(Client(c[0], c[1], c[2]))
        else:
            print("Client introuvable.")

        cursor.close()

    def modifier_prix(self, id_produit, nouveau_prix):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE produits SET prix = %s WHERE id = %s",
                (nouveau_prix, id_produit)
            )
            self.conn.commit()

            if cursor.rowcount:
                print("Prix modifié avec succès.")
            else:
                print("Produit introuvable.")

            cursor.close()

        except Error as e:
            print("Erreur MySQL :", e)

    def fermer(self):
        self.conn.close()
