import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Variáveis globais
csv_file_path = "importar_firebase.csv"
collection_name = "pagamento"
log_text = None


# Função para importar dados do CSV para o Firestore e mostrar logs na interface
def import_csv_to_firestore():
    global log_text



    # Limpe o widget de log
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Iniciando a importação...\n")

    try:
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                # Insira cada linha do CSV na coleção do Firestore
                db.collection(collection_name).add(row)
                log_text.insert(tk.END, f"Inserido com sucesso: {row}\n")

        log_text.insert(tk.END, "Importação concluída.\n")
    except Exception as e:
        log_text.insert(tk.END, f"Erro durante a importação: {str(e)}\n")


# Função para selecionar um arquivo CSV
def select_csv_file():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if csv_file_path:
        log_text.insert(tk.END, f"Arquivo CSV selecionado: {csv_file_path}\n")


# Criar a janela da interface gráfica
root = tk.Tk()
root.title("Importar Dados CSV para Firestore")

# Botão para selecionar arquivo CSV


# Botão para iniciar a importação
import_button = tk.Button(root, text="Importar CSV para Firestore", command=import_csv_to_firestore)
import_button.pack()

# Widget para exibir logs
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
log_text.pack()

# Iniciar o loop de eventos da interface gráfica
root.mainloop()
