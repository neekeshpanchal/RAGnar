import sys
import os
import openai
import PyPDF2
import faiss
import markdown2
from sentence_transformers import SentenceTransformer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QFileDialog, QMessageBox, QScrollArea, QSizePolicy, QSplitter, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPalette, QColor

# OpenAI API setup
openai.api_key = "<insert your open-ai api key>"
MODEL = "gpt-4o-mini"  

# Load retriever model
retriever_model = SentenceTransformer('all-MiniLM-L6-v2')

# Document Retriever Class
class DocumentRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.index = self.create_index()

    def create_index(self):
        # Create a FAISS index for fast retrieval
        document_embeddings = retriever_model.encode(self.documents)
        index = faiss.IndexFlatL2(document_embeddings.shape[1])
        index.add(document_embeddings)
        return index

    def retrieve(self, query, k=3):
        # Generate query embedding and retrieve the closest documents
        query_embedding = retriever_model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        retrieved_documents = [self.documents[i] for i in indices[0]]
        return retrieved_documents

# Function to extract text from PDFs in a folder
def extract_text_from_pdfs(folder_path):
    pdf_texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
                pdf_texts.append(text)
    return pdf_texts

class ApiWorker(QThread):
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, user_text, retriever=None):
        super().__init__()
        self.user_text = user_text
        self.retriever = retriever
        
    def run(self):
        try:
            context = ""
            if self.retriever:
                retrieved_docs = self.retriever.retrieve(self.user_text)
                context = " ".join(retrieved_docs)
            
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are my friend's late dog, Ragnar."},
                    {"role": "system", "content": f"Context: {context}"},
                    {"role": "user", "content": self.user_text}
                ]
            )
            assistant_response = response.choices[0].message["content"]
            self.result_signal.emit(assistant_response)
        except Exception as e:
            self.error_signal.emit(str(e))

class ChatMessage(QWidget):
    def __init__(self, name, message, is_user):
        super().__init__()
        self.name = name
        self.message = message
        self.is_user = is_user
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        name_label = QLabel(f"({self.name}):")
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        message_label = QLabel()
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Arial", 12))
        html_message = markdown2.markdown(self.message)
        message_label.setText(html_message)
        message_label.setTextFormat(Qt.RichText)
        message_label.setOpenExternalLinks(True)

        if self.is_user:
            name_label.setStyleSheet("color: #fd5200;")
            message_label.setStyleSheet("background-color: #fd5200; color: #fbfbfb; padding: 10px; border-radius: 10px;")
            layout.setAlignment(Qt.AlignRight)
        else:
            name_label.setStyleSheet("color: #619b8a;")
            message_label.setStyleSheet("background-color: #619b8a; color: #fbfbfb; padding: 10px; border-radius: 10px;")
            layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(name_label)
        layout.addWidget(message_label)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

class RagnarChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation = []
        self.retriever = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("RAGNAR - Chatbot Interface")
        self.resize(800, 700)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#012a36"))
        self.setPalette(palette)
        
        main_layout = QVBoxLayout(self)
        
        # Splitter for collapsible panel and chat
        splitter = QSplitter(Qt.Horizontal)
        
        # Chat area
        chat_layout = QVBoxLayout()
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)
        self.chat_area.setSpacing(10)
        
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("background-color: #fbfbfb; border: none;")
        chat_layout.addWidget(self.scroll_area)
        
        # Input area
        input_layout = QHBoxLayout()
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(50)
        input_layout.addWidget(self.user_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        chat_layout.addLayout(input_layout)
        
        chat_widget = QWidget()
        chat_widget.setLayout(chat_layout)
        splitter.addWidget(chat_widget)

        # Collapsible side panel for selecting a knowledge base
        self.side_panel = QWidget()
        side_layout = QVBoxLayout(self.side_panel)
        self.dir_button = QPushButton("Select Knowledge Base")
        self.dir_button.clicked.connect(self.select_knowledge_base)
        self.dir_label = QLabel("No directory selected.")
        side_layout.addWidget(self.dir_button)
        side_layout.addWidget(self.dir_label)
        splitter.addWidget(self.side_panel)

        main_layout.addWidget(splitter)
        splitter.setSizes([600, 200])

        self.setLayout(main_layout)
        self.display_message("Ragnar", "Hello!", is_user=False)
        
    def select_knowledge_base(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Knowledge Base Folder")
        if folder_path:
            self.dir_label.setText(f"Knowledge Base: {folder_path}")
            pdf_texts = extract_text_from_pdfs(folder_path)
            self.retriever = DocumentRetriever(pdf_texts)
        else:
            self.dir_label.setText("No directory selected.")
        
    def display_message(self, name, message, is_user):
        chat_message = ChatMessage(name, message, is_user)
        self.chat_area.addWidget(chat_message)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        
    def send_message(self):
        user_text = self.user_input.toPlainText().strip()
        if not user_text:
            QMessageBox.warning(self, "Input Error", "Please type a message.")
            return
        self.display_message("You", user_text, is_user=True)
        self.user_input.clear()
        self.user_input.setDisabled(True)
        self.send_button.setDisabled(True)
        self.worker = ApiWorker(user_text, self.retriever)
        self.worker.result_signal.connect(self.handle_result)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.start()
        
    def handle_result(self, assistant_response):
        self.display_message("Ragnar", assistant_response, is_user=False)
        self.user_input.setDisabled(False)
        self.send_button.setDisabled(False)
        
    def handle_error(self, error_message):
        self.display_message("Error", error_message, is_user=False)
        self.user_input.setDisabled(False)
        self.send_button.setDisabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = RagnarChatbotApp()
    chatbot.show()
    sys.exit(app.exec_())
