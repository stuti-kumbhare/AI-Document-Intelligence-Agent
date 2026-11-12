
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(extracted_data):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []

    for item in extracted_data:

        text = item["content"]

        chunks = splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "chunk_id": len(all_chunks) + 1,
                "source": item["source"],
                "page": item["page"],
                "content": chunk
            })

    return all_chunks
