
import ollama


def generate_summary(chunks, summary_type="short"):

    if not chunks:
        raise ValueError("No document chunks available.")

    document_parts = []
    max_chars = 8000
    current_length = 0

    for chunk in chunks:

        content = chunk.get("content", "").strip()

        if not content:
            continue

        entry = (
            f"Source: {chunk.get('source', 'Unknown')}\n"
            f"Page: {chunk.get('page', 'N/A')}\n"
            f"Content: {content}"
        )

        remaining = max_chars - current_length

        if remaining <= 0:
            break

        document_parts.append(entry[:remaining])
        current_length += len(entry[:remaining])

    document_text = "\n\n".join(document_parts)

    if not document_text.strip():
        raise ValueError("No readable document text available.")

    summary_instructions = {

        "short": """
Create a short summary in simple English.
Explain the main idea and important information
in approximately 5-7 bullet points.
""",

        "detailed": """
Create a detailed summary using clear headings.
Explain the main topics, important concepts,
and supporting information in simple English.
""",

        "points": """
Extract the most important points from the document.
Present them as a clear and organized bullet list.
"""
    }

    instruction = summary_instructions.get(
        summary_type,
        summary_instructions["short"]
    )

    prompt = f"""
You are an intelligent Document Summarization Assistant.

Summarize the uploaded document using only
the information provided below.

Do not invent facts or add outside information.

Summary instructions:
{instruction}

Document content:
{document_text}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI document summarization assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_gpu": 0,
            "num_ctx": 2048,
            "num_batch": 128,
            "temperature": 0.2
        }
    )

    return response["message"]["content"]
