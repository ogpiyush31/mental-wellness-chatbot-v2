import mysql.connector
import bcrypt
import os

# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

cursor = db.cursor()


# REGISTER USER
def register_user():

    username = input("Enter username: ")
    password = input("Enter password: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    query = "INSERT INTO users (username, password) VALUES (%s,%s)"

    cursor.execute(query, (username, hashed_password))
    db.commit()

    print("User registered successfully!")


# LOGIN USER
def login_user():

    username = input("Username: ")
    password = input("Password: ")

    query = "SELECT id, password FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:

        stored_password = result[1]

        # convert to bytes if returned as string
        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        if bcrypt.checkpw(password.encode(), stored_password):

            print("Login successful")

            return result[0]

    print("Invalid username or password")

    return None


# SAVE CHAT SUMMARY
def save_summary(user_id, summary):

    query = """
    INSERT INTO chat_summaries (user_id, summary)
    VALUES (%s,%s)
    """

    cursor.execute(query, (user_id, summary))

    db.commit()


# GENERATE SUMMARY USING LLM
def generate_summary(llm, conversation_history):

    text = "\n".join(conversation_history)

    prompt = f"""
Summarize this mental wellness conversation in 3 sentences:

{text}
"""

    response = llm.invoke(prompt)

    return response.content