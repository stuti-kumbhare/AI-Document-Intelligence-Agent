import ollama


def get_ai_response(question, context):

    prompt = f"""
You are an intelligent AI Document Assistant.

Answer the user's question using only
the information provided in the context.

If the answer is not available in the context,
clearly say that the uploaded documents
do not contain this information.

Give a clear and easy-to-understand answer.

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI Document Assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
