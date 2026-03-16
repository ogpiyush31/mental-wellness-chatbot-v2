🧠 AI Mental Wellness Chatbot
RAG + Groq LLM + MariaDB

An AI-powered Mental Wellness Chatbot that provides supportive conversations, detects distress signals, and stores conversation summaries for each user.

The system combines Retrieval-Augmented Generation (RAG) with LLM responses to deliver contextual and empathetic support.

🚀 Features

✨ User Authentication

Register & Login system

Secure password hashing using bcrypt

🧠 AI Chatbot

Retrieval-Augmented Generation (RAG)

Sentence Transformers embeddings

Groq LLM integration

⚠ Distress Detection

Detects crisis keywords

Escalates conversation to human support

💾 Database Integration

Stores users

Stores conversation summaries

MariaDB relational database

🔐 Security

.env environment variable configuration

Password hashing

API keys hidden from repository

🏗 System Architecture
User
  │
  ├── Register / Login
  │
  ├── Chat with AI
  │      │
  │      ├── Distress Detection
  │      ├── RAG Retrieval
  │      └── Groq LLM Response
  │
  └── Conversation Summary
          │
          └── Stored in MariaDB
📂 Project Structure
mental-wellness-chatbot
│
├── chatbot.py              # Main chatbot logic
├── auth_db.py              # Authentication & DB operations
├── build_faiss.py          # Vector index builder
├── mental_awareness_60_trees_kb.json
├── mental_index.faiss
├── metadata.pkl
├── .env
├── .gitignore
└── README.md
🛠 Tech Stack
Category	Technology
Language	Python
LLM	Groq (Llama 3)
Embeddings	Sentence Transformers
Database	MariaDB
Security	bcrypt
Vector Search	FAISS
⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/ogpiyush31/mental-wellness-chatbot-v2.git
cd mental-wellness-chatbot-v2
2️⃣ Install Dependencies
pip install sentence-transformers
pip install langchain-groq
pip install mysql-connector-python
pip install bcrypt
pip install python-dotenv
🔑 Environment Variables

Create a .env file:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=mental_health_db
DB_PORT=3307

GROQ_API_KEY=your_groq_api_key
🗄 Database Setup
CREATE DATABASE mental_health_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
▶ Run the Chatbot
python chatbot.py
💬 Example Conversation
🧠 Mental Wellness Chatbot

1. Register
2. Login

Choose option: 2

Username: user@gmail.com
Password: ******

Login successful

You: I feel stressed about work
Bot: It sounds like work pressure is affecting you. What part of your job feels most stressful?
📊 Database Example
Users Table
id	username
1	user@gmail.com
Chat Summaries
id	user_id	summary
1	1	User discussed stress related to work.
🔮 Future Improvements

Web interface with React

Backend API using FastAPI

Real-time chat UI

Conversation history per user

Emotion detection using NLP
