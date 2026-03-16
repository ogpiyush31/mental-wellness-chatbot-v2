AI Mental Wellness Chatbot

An AI-powered Mental Wellness Chatbot built using RAG (Retrieval Augmented Generation), Sentence Transformers, Groq LLM, and MariaDB.
The chatbot provides supportive mental health conversations, detects distress signals, and escalates to a human agent when necessary.

Features

User Registration & Login system

Secure password hashing using bcrypt

RAG-based responses using Sentence Transformers

Groq LLM integration for intelligent responses

Distress detection system

Automatic chat summary generation

MariaDB database storage

Secure configuration using .env environment variables

Agent escalation when bot confidence is low

Tech Stack

Backend

Python

Sentence Transformers

LangChain

Groq API

Database

MariaDB

Machine Learning

Embedding Model: all-MiniLM-L6-v2

RAG Retrieval using vector similarity

Security

bcrypt password hashing

Environment variable configuration

Project Architecture
User
  │
  ├── Register / Login
  │
  ├── Chat with AI
  │       │
  │       ├── Distress Detection
  │       ├── RAG Retrieval
  │       └── Groq LLM Response
  │
  └── Conversation Summary
          │
          └── Stored in MariaDB
Project Structure
mental-wellness-chatbot
│
├── chatbot.py              # Main chatbot logic
├── auth_db.py              # Authentication & database operations
├── build_faiss.py          # FAISS index creation
├── mental_awareness_60_trees_kb.json
├── mental_index.faiss
├── metadata.pkl
├── .env                    # API keys & DB credentials
├── .gitignore
└── README.md
Setup Instructions
1 Install dependencies
pip install -r requirements.txt

or manually:

pip install sentence-transformers
pip install langchain-groq
pip install mysql-connector-python
pip install bcrypt
pip install python-dotenv
2 Configure Environment Variables

Create a .env file:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=mental_health_db
DB_PORT=3307

GROQ_API_KEY=your_groq_api_key
3 Setup Database

Create database and tables:

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
4 Run the Chatbot
python chatbot.py
Example Usage
🧠 Mental Wellness Chatbot

1. Register
2. Login

Choose option: 2

Username: user@gmail.com
Password: ********

Login successful

You: I feel stressed about work
Bot: It sounds like work pressure is affecting you. What part of your job feels most stressful?
Database Example
Users Table
id	username
1	user@gmail.com
Chat Summary Table
id	user_id	summary
1	1	User discussed work stress and anxiety.
Future Improvements

Web interface using React

FastAPI backend API

Real-time chat UI

Chat history per session

Emotion detection from voice/text


GitHub
https://github.com/ogpiyush31
