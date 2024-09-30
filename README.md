# RAGnar

**RAGnar** is an interactive chatbot application that combines the power of **OpenAI's GPT-4**, **FAISS** for efficient document retrieval, and **SentenceTransformers** for embedding generation. Built with a user-friendly interface using **PyQt5**, RAGnar allows you to engage in meaningful conversations, perform semantic searches across your documents, and convert natural language queries into SQL commands. This project is named in memory of **Ragnar**, a playful and brave German Shepherd who touched many hearts.

![Ragnar Image](https://github.com/user-attachments/assets/58c2fe7f-3e6c-4b4f-ae99-da1114d172b8)

---

**Author**: Neekesh Panchal, Computer Science and Neuroscience Graduate, September 2024

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Semantic Search Mode](#semantic-search-mode)
  - [Text-to-SQL Mode](#text-to-sql-mode)
- [Future Enhancements](#future-enhancements)
- [Acknowledgements](#acknowledgements)

## Features

- **Conversational AI with GPT-4**: Engage with an intelligent chatbot powered by OpenAI's GPT-4 model, capable of understanding and responding to a wide range of queries.
- **Knowledge Base Integration**: Select a directory containing **PDF**, **DOCX**, and **CSV** files to enhance chatbot responses with relevant context from your documents.
- **FAISS-Enabled Retrieval**: Utilize FAISS (Facebook AI Similarity Search) for efficient and accurate document retrieval within your knowledge base.
- **Embeddings with SentenceTransformers**: Generate embeddings for document chunks using SentenceTransformers, improving the relevance of retrieved information.
- **Text-to-SQL Conversion**: Convert natural language queries into SQL commands and execute them against a selected SQLite database, displaying results within the chat interface.
- **PyQt5 GUI**: Enjoy an intuitive and responsive graphical user interface for seamless interaction with the chatbot.
- **Mode Selection**: Easily switch between **Semantic Search** and **Text-to-SQL** modes to suit your needs.
- **Dynamic Knowledge Base and Database Loading**: Load and manage your knowledge bases and databases in real-time without restarting the application.
- **Collapsible Side Panel**: Access mode selection and resource loading options through a sleek, collapsible side panel.

![Chatbot Interface](https://github.com/user-attachments/assets/00280859-9ddf-4223-ae76-f4cc1a09b554)

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/RAGnar.git
    cd RAGnar
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up OpenAI API Key:**

    Replace `"YOUR_OPENAI_API_KEY"` in the `ragna_chatbot.py` file with your actual OpenAI API key.

4. **Run the Application:**

    ```bash
    python ragna_chatbot.py
    ```

## Prerequisites

- **Python 3.7+**
- **PyQt5**
- **OpenAI API Key**: Required for GPT-4 integration.
- **FAISS**: Install FAISS for efficient document similarity searches.
- **SentenceTransformers**: Used for generating document embeddings.
- **PyPDF2**, **python-docx**, **pandas**: For extracting text from PDF, DOCX, and CSV files.
- **SQLite**: For executing SQL queries in Text-to-SQL mode.

## Usage

### Semantic Search Mode

1. **Launch the Application:**

   ```bash
   python ragna_chatbot.py
   ```

2. **Select Semantic Search Mode:**

   Click on the **"Semantic Search"** button in the side panel.

3. **Load Knowledge Base:**

   - Click **"Select Knowledge Base"** to choose a directory containing your **PDF**, **DOCX**, or **CSV** files.
   - The chatbot will process and index these documents for retrieval.

4. **Interact with the Chatbot:**

   - Enter your queries in the text input box and click **"Send"**.
   - The chatbot will retrieve relevant information from your knowledge base and generate contextual responses.

### Text-to-SQL Mode

1. **Select Text-to-SQL Mode:**

   Click on the **"Text-to-SQL"** button in the side panel.

2. **Load Database Schema:**

   - Click **"Select Database"** to choose your SQLite database file (`.db` or `.sqlite`).
   - The application will load the database schema for reference.

3. **Ask Natural Language Queries:**

   - Enter your question in natural language and click **"Send"**.
   - The chatbot will convert your query into an SQL command, execute it against the loaded database, and display the results.

4. **General Questions:**

   - You can also ask general questions not related to SQL. The chatbot will respond accordingly without attempting to execute any SQL commands.

## Future Enhancements

- **Searchable Chat History**: Implement functionality to search through past interactions with the chatbot.
- **Enhanced Knowledge Management**: Allow the addition of multiple knowledge bases and the ability to switch between them seamlessly.
- **Auto-Completion of Inputs**: Provide contextual suggestions as you type to improve user interaction speed.
- **Conversation Saving and Loading**: Enable users to save their chat sessions and reload them in future interactions.

## Acknowledgements

- **OpenAI**: For providing the GPT-4 model that powers the conversational capabilities.
- **FAISS**: For efficient similarity search and clustering of dense vectors.
- **SentenceTransformers**: For easy-to-use BERT-based sentence and text embeddings.
- **PyQt5**: For the GUI framework that makes the application user-friendly.

---

**Rest in Peace, Ragnar 🐾**

This project is dedicated to the memory of Ragnar, whose spirit of curiosity and companionship inspired its creation.
