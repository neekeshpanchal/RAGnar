# RAGnar

**RAGnar** is an interactive chatbot application that leverages **GPT-4o-mini** and **FAISS** for PDF-based knowledge retrieval, **SentenceTransformers** for embedding generation, and a user-friendly interface built using **PyQt5**. This project is named in memory of **Ragnar**, a playful and brave German shepherd who loved to bark and eat meat sticks.

![Ragnar Image](https://github.com/user-attachments/assets/58c2fe7f-3e6c-4b4f-ae99-da1114d172b8)

## Features

- **Conversational AI with GPT-4o-mini**: Engage with an intelligent chatbot powered by OpenAI's GPT-4 model.
- **Knowledge Base Integration**: Select a directory of PDF files to augment chatbot responses with relevant context from documents.
- **FAISS-Enabled Retrieval**: Efficient document retrieval with FAISS (Facebook AI Similarity Search) for quick and accurate knowledge base querying.
- **Embeddings with SentenceTransformers**: Uses SentenceTransformers to generate embeddings for document chunks, enhancing the relevance of retrieved information.
- **PyQt5 GUI**: Intuitive and responsive GUI for user interaction, including a collapsible side panel to select and manage knowledge bases.
- **Collapsible Side Panel**: Seamlessly integrates a knowledge base selection panel to allow real-time switching of document sources.
- **Searchable Chat History**: Future enhancement will allow users to search through previous conversations.
- **Save and Load Conversations**: Save your current chatbot session and load it back to continue where you left off.
- **Auto-Completion**: Get auto-suggestions based on previous inputs, enhancing user experience and speeding up conversation flow.

![image](https://github.com/user-attachments/assets/00280859-9ddf-4223-ae76-f4cc1a09b554)


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

3. **Run the Application:**
    ```bash
    python ragna_chatbot.py
    ```

## Prerequisites

- **Python 3.7+**
- **PyQt5**
- **OpenAI API Key**: Set up your OpenAI API key for GPT-4 integration.
- **FAISS**: Ensure FAISS is installed for efficient document similarity searches.
- **SentenceTransformers**: Required for generating document embeddings.

## Usage

1. Launch the chatbot GUI using the `python ragna_chatbot.py` command.
2. Select a knowledge base directory by clicking the "Select Knowledge Base" button in the collapsible side panel. 
   - Ensure the directory contains PDF files that you want the chatbot to pull from.
3. Enter your message in the text input box and hit "Send."
4. **RAGnar** will retrieve relevant information from the knowledge base and generate a contextual response using GPT-4.
5. Optionally, save your conversation and reload it in a future session.

## Future Enhancements

- **Searchable Chat History**: Easily search through past interactions with the chatbot.
- **Enhanced Knowledge Management**: Add multiple knowledge bases and switch between them seamlessly.
- **Auto-Completion of Inputs**: Contextual suggestions as you type to improve user interaction speed.


REST IN PEACE RAGNAR 🐾
