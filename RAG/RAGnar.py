# Author: Neekesh Panchal, Computer Science and Neuroscience Graduate, September 2024

import sys
import os
import openai
import PyPDF2
import faiss
import markdown2
import sqlite3
import pandas as pd
import docx
import re  # For regex operations
from sentence_transformers import SentenceTransformer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QFileDialog, QMessageBox, QScrollArea, QSizePolicy, QSplitter, QTextBrowser,
    QFrame, QGraphicsDropShadowEffect, QToolButton
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QEasingCurve, QRect, QCoreApplication, QPropertyAnimation
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon

# Load OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key

# Model to use
MODEL = "gpt-4"  # You can use a different model if available

# Load the sentence transformer model for semantic search
retriever_model = SentenceTransformer('all-MiniLM-L6-v2')

# Document Retriever Class
class DocumentRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.index = self.create_index()

    def create_index(self):
        # Create a FAISS index for fast document retrieval
        document_embeddings = retriever_model.encode(self.documents)
        index = faiss.IndexFlatL2(document_embeddings.shape[1])
        index.add(document_embeddings)
        return index

    def retrieve(self, query, k=3):
        # Retrieve the top-k documents most relevant to the query
        query_embedding = retriever_model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        retrieved_documents = [self.documents[i] for i in indices[0]]
        return retrieved_documents

# Functions to extract text from different file types
def extract_text_from_pdfs(folder_path):
    pdf_texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                pdf_texts.append(text)
    return pdf_texts

def extract_text_from_docx(folder_path):
    docx_texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.docx'):
            docx_path = os.path.join(folder_path, file_name)
            doc = docx.Document(docx_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            docx_texts.append(text)
    return docx_texts

def extract_text_from_csv(folder_path):
    csv_texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(csv_path)
            text = df.to_string()
            csv_texts.append(text)
    return csv_texts

class ApiWorker(QThread):
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, user_text, mode, retriever=None, db_schema=None):
        super().__init__()
        self.user_text = user_text
        self.mode = mode
        self.retriever = retriever
        self.db_schema = db_schema

    def run(self):
        try:
            if self.mode == '!semantic':
                context = ""
                if self.retriever:
                    retrieved_docs = self.retriever.retrieve(self.user_text)
                    context = " ".join(retrieved_docs)

                messages = [
                    {"role": "system", "content": "You are a helpful assistant that provides answers based on the retrieved context."},
                    {"role": "system", "content": f"Context: {context}"},
                    {"role": "user", "content": self.user_text}
                ]

                response = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7
                )

                assistant_response = response.choices[0].message.content.strip()
                self.result_signal.emit(assistant_response)

            elif self.mode == '!text2sql':
                schema_description = self.db_schema if self.db_schema else ""
                messages = [
                    {"role": "system", "content": "You are an assistant that helps convert natural language queries into SQL based on the provided database schema. When appropriate, output the SQL query in a code block labeled as sql. Do not include any explanations in the code block. If the user asks a general question or something not related to SQL, you can answer normally."},
                    {"role": "system", "content": f"Database Schema:\n{schema_description}"},
                    {"role": "user", "content": self.user_text}
                ]

                response = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )

                assistant_response = response.choices[0].message.content.strip()
                self.result_signal.emit(assistant_response)
            else:
                self.error_signal.emit("Invalid mode selected.")
        except Exception as e:
            self.error_signal.emit(str(e))

class ChatMessage(QWidget):
    def __init__(self, name, message, is_user):
        super().__init__()
        self.name = name
        self.message = message
        self.is_user = is_user
        self.init_ui()
        self.animate_entry()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        # Avatar setup
        avatar_label = QLabel()
        avatar_label.setFixedSize(40, 40)
        if self.is_user:
            avatar_pixmap = QIcon("user_avatar.png").pixmap(40, 40)  # Replace with actual avatar image path
        else:
            avatar_pixmap = QIcon("bot_avatar.png").pixmap(40, 40)  # Replace with actual avatar image path
        avatar_label.setPixmap(avatar_pixmap)
        avatar_label.setScaledContents(True)

        # Message bubble
        bubble_layout = QVBoxLayout()
        bubble_layout.setSpacing(5)

        # Name label
        name_label = QLabel(self.name)
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        name_label.setStyleSheet("color: #FFFFFF;")

        # Timestamp
        from datetime import datetime
        timestamp_label = QLabel(datetime.now().strftime("%H:%M"))
        timestamp_label.setFont(QFont("Arial", 8))
        timestamp_label.setStyleSheet("color: #AAAAAA;")

        # Message content
        message_browser = QTextBrowser()
        message_browser.setFont(QFont("Arial", 12))
        message_browser.setOpenExternalLinks(True)
        message_browser.setReadOnly(True)
        message_browser.setFrameStyle(QFrame.NoFrame)
        message_browser.setStyleSheet("background: transparent;")
        message_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        html_message = markdown2.markdown(self.message)
        message_browser.setHtml(html_message)

        # Adjust the height to fit content
        message_browser.document().setTextWidth(400)
        document_height = message_browser.document().size().height()
        message_browser.setFixedHeight(int(document_height + 20))

        # Bubble frame
        bubble_frame = QFrame()
        bubble_frame_layout = QVBoxLayout(bubble_frame)
        bubble_frame_layout.addWidget(name_label)
        bubble_frame_layout.addWidget(message_browser)
        bubble_frame_layout.addWidget(timestamp_label, alignment=Qt.AlignRight)
        bubble_frame.setLayout(bubble_frame_layout)
        bubble_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        bubble_frame.setContentsMargins(0, 0, 0, 0)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 80))
        bubble_frame.setGraphicsEffect(shadow)

        # Styling
        if self.is_user:
            bubble_frame.setStyleSheet("""
                background-color: #1E88E5;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 10px;
            """)
            layout.addStretch()
            layout.addWidget(bubble_frame)
            layout.addWidget(avatar_label)
        else:
            bubble_frame.setStyleSheet("""
                background-color: #424242;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 10px;
            """)
            layout.addWidget(avatar_label)
            layout.addWidget(bubble_frame)
            layout.addStretch()

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def animate_entry(self):
        # Fade-in animation
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b'windowOpacity')
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()

class RagnarChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation = []
        self.retriever = None
        self.db_schema = None
        self.mode = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("RAGnar 0.1 - Chatbot Interface")
        self.resize(900, 700)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Side panel
        self.side_panel = QFrame()
        self.side_panel.setFixedWidth(250)
        self.side_panel.setStyleSheet("background-color: #2C2C2C;")
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setSpacing(20)
        side_layout.setContentsMargins(20, 20, 20, 20)

        # Logo or title
        title_label = QLabel("RAGnar 0.1")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        side_layout.addWidget(title_label)

        # Mode selection
        self.mode_label = QLabel("Select Mode:")
        self.mode_label.setStyleSheet("color: #FFFFFF;")
        side_layout.addWidget(self.mode_label)

        button_style = """
            QPushButton {
                background-color: #3E3E3E;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """

        # Semantic search button
        self.semantic_button = QPushButton(QIcon("semantic_icon.png"), " Semantic Search")  # Replace with actual icon path
        self.semantic_button.setStyleSheet(button_style)
        self.semantic_button.clicked.connect(self.select_semantic_mode)
        side_layout.addWidget(self.semantic_button)

        # Text-to-SQL button
        self.text2sql_button = QPushButton(QIcon("sql_icon.png"), " Text-to-SQL")  # Replace with actual icon path
        self.text2sql_button.setStyleSheet(button_style)
        self.text2sql_button.clicked.connect(self.select_text2sql_mode)
        side_layout.addWidget(self.text2sql_button)

        # Knowledge base selection
        self.dir_button = QPushButton("Select Knowledge Base")
        self.dir_button.setStyleSheet(button_style)
        self.dir_button.clicked.connect(self.select_knowledge_base)
        self.dir_label = QLabel("No directory selected.")
        self.dir_label.setStyleSheet("color: #FFFFFF;")
        side_layout.addWidget(self.dir_button)
        side_layout.addWidget(self.dir_label)

        # Database selection
        self.db_button = QPushButton("Select Database")
        self.db_button.setStyleSheet(button_style)
        self.db_button.clicked.connect(self.select_database)
        self.db_label = QLabel("No database selected.")
        self.db_label.setStyleSheet("color: #FFFFFF;")
        side_layout.addWidget(self.db_button)
        side_layout.addWidget(self.db_label)

        side_layout.addStretch()

        # Chat area
        chat_frame = QFrame()
        chat_layout = QVBoxLayout(chat_frame)
        chat_frame.setStyleSheet("background-color: #F5F5F5;")

        # Scroll area for messages
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)
        self.chat_area.setSpacing(10)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        chat_layout.addWidget(self.scroll_area)

        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #FFFFFF;")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(50)
        self.user_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        input_layout.addWidget(self.user_input)
        self.send_button = QPushButton(QIcon("send_icon.png"), "")  # Replace with actual icon path
        self.send_button.setFixedSize(50, 50)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        chat_layout.addWidget(input_frame)

        # Add frames to main layout
        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(chat_frame)

        self.setLayout(main_layout)
        self.display_message("RAGnar 0.1", "Hello! Please select a mode by clicking Semantic Search or Text-to-SQL.", is_user=False)

        # Initial UI state
        self.update_ui_state()

    def update_ui_state(self):
        # Update the UI based on the selected mode
        if self.mode == '!semantic':
            self.db_button.hide()
            self.db_label.hide()
            self.dir_button.show()
            self.dir_label.show()
        elif self.mode == '!text2sql':
            self.dir_button.hide()
            self.dir_label.hide()
            self.db_button.show()
            self.db_label.show()
        else:
            self.dir_button.hide()
            self.dir_label.hide()
            self.db_button.hide()
            self.db_label.hide()

    def select_semantic_mode(self):
        self.mode = '!semantic'
        self.display_message("System", "Semantic Search mode selected.", is_user=False)
        self.update_ui_state()

    def select_text2sql_mode(self):
        self.mode = '!text2sql'
        self.display_message("System", "Text-to-SQL mode selected.", is_user=False)
        self.update_ui_state()

    def select_knowledge_base(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Knowledge Base Folder")
        if folder_path:
            self.dir_label.setText(f"Knowledge Base: {folder_path}")
            pdf_texts = extract_text_from_pdfs(folder_path)
            docx_texts = extract_text_from_docx(folder_path)
            csv_texts = extract_text_from_csv(folder_path)
            all_texts = pdf_texts + docx_texts + csv_texts
            if all_texts:
                self.retriever = DocumentRetriever(all_texts)
                self.display_message("System", "Knowledge base loaded successfully.", is_user=False)
            else:
                self.display_message("System", "No valid documents found in the selected folder.", is_user=False)
        else:
            self.dir_label.setText("No directory selected.")

    def select_database(self):
        db_path, _ = QFileDialog.getOpenFileName(self, "Select Database File", "", "SQLite Database Files (*.db *.sqlite)")
        if db_path:
            self.db_label.setText(f"Database: {db_path}")
            self.db_path = db_path
            self.load_db_schema(db_path)
        else:
            self.db_label.setText("No database selected.")

    def load_db_schema(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            schema = ""
            for table in tables:
                table_name = table[0]
                schema += f"Table: {table_name}\n"
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                for column in columns:
                    schema += f" - {column[1]} ({column[2]})\n"
            self.db_schema = schema
            conn.close()
            self.display_message("System", "Database schema loaded successfully.", is_user=False)
        except Exception as e:
            self.display_message("Error", f"Failed to load database schema: {e}", is_user=False)

    def display_message(self, name, message, is_user):
        # Display a message in the chat area
        chat_message = ChatMessage(name, message, is_user)
        self.chat_area.addWidget(chat_message)
        QCoreApplication.processEvents()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def send_message(self):
        user_text = self.user_input.toPlainText().strip()
        if not user_text:
            QMessageBox.warning(self, "Input Error", "Please type a message.")
            return
        if not self.mode:
            QMessageBox.warning(self, "Mode Selection", "Please select a mode first.")
            return
        if self.mode == '!semantic' and not self.retriever:
            QMessageBox.warning(self, "Knowledge Base Not Loaded", "Please select and load a knowledge base first.")
            return
        if self.mode == '!text2sql' and not hasattr(self, 'db_schema'):
            QMessageBox.warning(self, "Database Not Loaded", "Please select and load a database first.")
            return
        self.display_message("You", user_text, is_user=True)
        self.user_input.clear()
        self.user_input.setDisabled(True)
        self.send_button.setDisabled(True)
        self.worker = ApiWorker(user_text, self.mode, self.retriever, self.db_schema)
        self.worker.result_signal.connect(self.handle_result)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.start()

    def handle_result(self, assistant_response):
        self.display_message("RAGnar 0.1", assistant_response, is_user=False)
        self.user_input.setDisabled(False)
        self.send_button.setDisabled(False)

        if self.mode == '!text2sql' and hasattr(self, 'db_path'):
            try:
                # Extract SQL code from the assistant's response
                code_blocks = re.findall(r'```sql\s*(.*?)```', assistant_response, re.DOTALL | re.IGNORECASE)
                if code_blocks:
                    sql_query = code_blocks[0].strip()

                    # Connect to the SQLite database and execute the SQL query
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(sql_query)
                    columns = [description[0] for description in cursor.description]  # Get column names
                    results = cursor.fetchall()
                    conn.close()

                    # Check if results are found
                    if results:
                        # Format the results in an HTML table
                        result_str = "<table border='1' cellpadding='5' cellspacing='0'>"
                        result_str += "<tr>" + "".join([f"<th>{col}</th>" for col in columns]) + "</tr>"  # Header row
                        for row in results:
                            result_str += "<tr>" + "".join([f"<td>{val}</td>" for val in row]) + "</tr>"  # Data rows
                        result_str += "</table>"

                        # Display the formatted table in the chat
                        self.display_message("Results", result_str, is_user=False)
                    else:
                        self.display_message("Results", "No results found.", is_user=False)

                else:
                    # No SQL code found in the assistant's response
                    pass  # Do nothing extra

            except Exception as e:
                self.display_message("Error", f"Failed to execute SQL query: {e}", is_user=False)

    def handle_error(self, error_message):
        self.display_message("Error", error_message, is_user=False)
        self.user_input.setDisabled(False)
        self.send_button.setDisabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = RagnarChatbotApp()
    chatbot.show()
    sys.exit(app.exec_())
