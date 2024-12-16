import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

# Carregando o modelo BERT e o tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def get_bert_embedding(text):
    """Obtém o embedding BERT para o texto fornecido."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    return embeddings


def bert_similarity(s1, s2):
    """Calcula a similaridade entre dois textos usando embeddings do BERT."""
    emb1 = get_bert_embedding(s1)
    emb2 = get_bert_embedding(s2)
    similarity = 1 - cosine(emb1, emb2)
    return similarity * 100


class BERTSimilarityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verificador de Similaridade BERT")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Título
        title = QLabel("Verificador de Similaridade BERT")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Campo para inserir a marca principal
        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Digite o nome da sua marca")
        layout.addWidget(QLabel("Sua Marca:"))
        layout.addWidget(self.marca_input)

        # Campo para inserir as marcas colidentes
        self.colidencias_input = QTextEdit()
        self.colidencias_input.setPlaceholderText(
            "Digite as marcas supostamente colidentes, uma por linha"
        )
        layout.addWidget(QLabel("Marcas Colidentes:"))
        layout.addWidget(self.colidencias_input)

        # Botão para iniciar o cálculo
        self.process_button = QPushButton("Calcular Similaridade")
        self.process_button.clicked.connect(self.calculate_similarity)
        layout.addWidget(self.process_button)

        # Resultado
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # Definir layout principal
        self.setLayout(layout)

    def calculate_similarity(self):
        # Obter entradas
        marca = self.marca_input.text().strip()
        colidencias_text = self.colidencias_input.toPlainText().strip()

        if not marca or not colidencias_text:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos antes de continuar.")
            return

        colidencias = colidencias_text.split("\n")
        results = []

        # Calcular similaridade para cada marca colidente
        for colidencia in colidencias:
            similarity = bert_similarity(marca, colidencia.strip())
            results.append(f"{colidencia.strip()}: {similarity:.2f}%")

        # Exibir resultados
        self.result_label.setText("Resultados exibidos no console.")
        QMessageBox.information(self, "Resultado", "\n".join(results))
        print("\n".join(results))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BERTSimilarityApp()
    window.show()
    sys.exit(app.exec())
