import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


index = faiss.read_index("mental_index.faiss")


with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


current_node = None
followup_index = 0

print("\n Mental Wellness Chatbot")
print("Type 'exit' to stop\n")



def is_new_question(text):

    text = text.lower()

    keywords = [
        "why",
        "how",
        "i feel",
        "i am",
        "i'm",
        "i cant",
        "i can't",
        "i dont",
        "i don't",
        "i have",
        "i keep",
    ]

    for k in keywords:
        if k in text:
            return True

    return False



while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    
    if current_node is None or is_new_question(user_input):

        query_vector = model.encode([user_input])
        query_vector = np.array(query_vector).astype("float32")

        distances, indices = index.search(query_vector, 1)

        best_match = metadata[indices[0][0]]

        current_node = best_match
        followup_index = 0

        print("\nBot:", best_match.get("response", ""))

        followups = best_match.get("followups", [])

        if followups:
            print("\nBot:", followups[0]["question"])

        continue

   
    followups = current_node.get("followups", [])

    if followup_index < len(followups):

        answer = followups[followup_index]["answer"]

        print("\nBot:", answer)

        followup_index += 1

        if followup_index < len(followups):

            next_question = followups[followup_index]["question"]

            print("\nBot:", next_question)

        else:

            print("\nBot: Thanks for sharing. Would you like to talk about something else?")

            current_node = None
            followup_index = 0

    else:

        current_node = None
        followup_index = 0