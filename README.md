**RAGnar**
is an interactive chatbot application that combines the power of **OpenAI's GPT-4**, **FAISS** for efficient document retrieval, and **SentenceTransformers** for embedding generation. This project is named in memory of **Ragnar**, a playful and brave German Shepherd who touched many hearts.

![image](https://github.com/user-attachments/assets/20756793-7d41-4e68-b6b4-bf7b646d01b7)

**REX (Response EXplainablity)** 
is a built-in interface which allows for reasoning transparency and the ability to view which files were chosen by the retrieval model. This interface is named in memory of **Rex**, a protective and strong-hearted German Shepherd who is missed by many.

![image](https://github.com/user-attachments/assets/f78d845d-e975-4eb3-9f38-af3405c2164f)

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


![image](https://github.com/user-attachments/assets/4a7695c3-cac8-4cf6-9f04-32c7864d26fa)


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

    Replace `"YOUR_OPENAI_API_KEY"` in the `ragnar_chatbot.py` file with your actual OpenAI API key.

4. **Run the Application:**

    ```bash
    python ragnar_chatbot.py
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
   python ragnar_chatbot.py
   ```

2. **Select Semantic Search Mode:**

   Click on the **"Semantic Search"** button in the side panel.

![image](https://github.com/user-attachments/assets/c40e7c18-d464-4213-a1e2-836c330cf3ee)


3. **Load Knowledge Base:**

   - Click **"Select Knowledge Base"** to select a **folder** containing your **PDF**, **DOCX**, or **CSV** files.
   - The chatbot will process and index these documents for retrieval.

![image](https://github.com/user-attachments/assets/c9944aff-3a1a-43b7-9dfc-428479f679e2)


4. **Interact with the Chatbot:**

   - Enter your queries in the text input box and click **"Send"**.
   - The chatbot will retrieve relevant information from your knowledge base and generate contextual responses.

![image](https://github.com/user-attachments/assets/972ef6c8-2232-4a83-a085-df76e0a725d0)


### Text-to-SQL Mode

1. **Select Text-to-SQL Mode:**

   Click on the **"Text-to-SQL"** button in the side panel.

![image](https://github.com/user-attachments/assets/59d36bda-46a7-4348-9621-360bd0233575)


2. **Load Database Schema:**

   - Click **"Select Database"** to choose your SQLite database file (`.db` or `.sqlite`).
   - The application will load the database schema for reference.

![image](https://github.com/user-attachments/assets/7eacf36b-6da3-443f-89f0-5507be336fcf)


3. **Ask Natural Language Queries:**

   - Enter your question in natural language and click **"Send"**.
   - The chatbot can create SQL queries for you, but can also describe the data and build code to leverage it as well.

![image](https://github.com/user-attachments/assets/f287984b-ff89-4cf4-b265-36e93fa6c9e3)


4. **REX - Response EXplainablity**

   - After querying using semantic search or Text-to-SQL capabilities, User's can click the 'REX' button to access context relevant for reasoning and references.

![image](https://github.com/user-attachments/assets/8f948fd3-18cf-4255-b8ef-534903a87af5)


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
