
import re
import streamlit as st

from modules.document_loader import extract_text
from modules.text_processor import split_documents
from modules.embeddings import generate_embeddings
from modules.vector_database import (
    create_vector_database,
    search_vectors
)
from modules.ai_agent import get_ai_response
from modules.summarizer import generate_summary


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="AI Document Intelligence Agent",
    page_icon="📚",
    layout="wide"
)


# =====================================
# HELPER FUNCTION: BUILD DOCUMENT CONTEXT
# =====================================

def build_document_context(chunks, max_chars=18000):

    context_parts = []
    used_chars = 0

    for chunk in chunks:

        content = chunk.get("content", "").strip()

        if not content:
            continue

        entry = (
            f"Source: {chunk.get('source', 'Unknown')}\n"
            f"Page: {chunk.get('page', 'N/A')}\n"
            f"Content: {content}"
        )

        remaining = max_chars - used_chars

        if remaining <= 0:
            break

        if len(entry) > remaining:
            entry = entry[:remaining]

        context_parts.append(entry)
        used_chars += len(entry) + 2

    return "\n\n".join(context_parts)


# =====================================
# HELPER FUNCTION: FORMAT CHECKLIST
# =====================================

def format_checklist_output(checklist):

    # Convert inline bullet symbols into separate checklist items
    checklist = checklist.replace("•", "\n- [ ] ")

    formatted_lines = []

    for line in checklist.splitlines():

        line = line.strip()

        if not line:
            continue

        # Preserve headings
        if line.startswith("#"):
            formatted_lines.append("")
            formatted_lines.append(line)

        # Preserve already formatted checkboxes
        elif line.startswith("- [ ]") or line.startswith("- [x]"):
            formatted_lines.append(line)

        # Convert ordinary bullet points into checkboxes
        elif line.startswith("- ") or line.startswith("* "):
            formatted_lines.append("- [ ] " + line[2:].strip())

        # Convert numbered tasks into checkboxes
        elif re.match(r"^\d+[\.\)]\s+", line):
            item = re.sub(r"^\d+[\.\)]\s+", "", line)
            formatted_lines.append("- [ ] " + item)

        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)


# =====================================
# SESSION STATE
# =====================================

if "all_chunks" not in st.session_state:
    st.session_state.all_chunks = []

if "vector_index" not in st.session_state:
    st.session_state.vector_index = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# =====================================
# MAIN TITLE
# =====================================

st.title("📚 AI-Powered Document Intelligence Agent")

st.write(
    "Your intelligent assistant for understanding, "
    "analyzing and comparing multiple documents."
)

st.success("Welcome! Your AI Document Agent is ready.")


# =====================================
# SIDEBAR NAVIGATION
# =====================================

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Choose an option",
    [
        "Home",
        "Upload Documents",
        "Document Summary",
        "Ask Your Documents",
        "Compare Documents",
        "Generate Checklist"
    ]
)


# =====================================
# HOME PAGE
# =====================================

if menu == "Home":

    st.header("🏠 Dashboard")

    st.write(
        "Upload your documents and interact with your AI assistant."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Processed Documents",
        len(st.session_state.processed_files)
    )

    col2.metric(
        "AI Model",
        "Llama 3.2"
    )

    col3.metric(
        "Total Chunks",
        len(st.session_state.all_chunks)
    )

    st.subheader("Available Features")

    st.write("📂 Multiple Document Upload")
    st.write("📖 Document Text Extraction")
    st.write("✂️ Text Chunking")
    st.write("🔢 Text Embeddings")
    st.write("🗄️ FAISS Vector Database")
    st.write("🤖 AI Question Answering")
    st.write("📝 Document Summarization")
    st.write("📊 Document Comparison")
    st.write("✅ Checklist Generation")


# =====================================
# UPLOAD DOCUMENTS
# =====================================

elif menu == "Upload Documents":

    st.header("📂 Upload Your Documents")

    files = st.file_uploader(
        "Choose PDF, DOCX, TXT or PPTX files",
        type=[
    "pdf",
    "docx",
    "txt",
    "pptx",
    "png",
    "jpg",
    "jpeg",
    "tif",
    "tiff",
    "bmp",
    "webp"
],
        accept_multiple_files=True
    )

    if files:

        if st.button("Process Documents", type="primary"):

            all_chunks = []
            processed_files = []

            for file in files:

                st.divider()
                st.subheader(f"📄 {file.name}")

                try:

                    # STEP 1: EXTRACT TEXT

                    extracted_data = extract_text(file)

                    if not extracted_data:

                        st.warning(
                            f"No readable text found in {file.name}"
                        )
                        continue

                    st.success("Text extracted successfully!")

                    total_words = sum(
                        len(item["content"].split())
                        for item in extracted_data
                    )

                    st.write("Total words:", total_words)

                    # STEP 2: TEXT CHUNKING

                    chunks = split_documents(extracted_data)

                    if not chunks:

                        st.warning(
                            f"No text chunks generated for {file.name}"
                        )
                        continue

                    all_chunks.extend(chunks)
                    processed_files.append(file.name)

                    st.success("Text chunking completed!")

                    st.write("Total chunks:", len(chunks))

                    with st.expander("View Text Chunks"):

                        for chunk in chunks:

                            st.markdown(
                                f"**Chunk {chunk['chunk_id']}**"
                            )

                            st.write("Source:", chunk["source"])
                            st.write("Page:", chunk["page"])
                            st.write(chunk["content"])

                            st.divider()

                except Exception as e:

                    st.error(
                        f"Unable to process {file.name}: {e}"
                    )

            # STEP 3: GENERATE EMBEDDINGS

            if all_chunks:

                try:

                    with st.spinner(
                        "Generating embeddings... Please wait."
                    ):

                        embeddings = generate_embeddings(all_chunks)

                    st.success("Embeddings generated successfully!")

                    # STEP 4: CREATE FAISS DATABASE

                    with st.spinner(
                        "Creating FAISS vector database..."
                    ):

                        vector_index = create_vector_database(
                            all_chunks,
                            embeddings
                        )

                    # STEP 5: SAVE DATA

                    st.session_state.all_chunks = all_chunks

                    st.session_state.vector_index = vector_index

                    st.session_state.processed_files = processed_files

                    st.success(
                        "Documents processed successfully!"
                    )

                    st.subheader("📊 Processing Report")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Processed Documents",
                        len(processed_files)
                    )

                    col2.metric(
                        "Total Chunks",
                        len(all_chunks)
                    )

                    col3.metric(
                        "Total Embeddings",
                        len(embeddings)
                    )

                    st.metric(
                        "FAISS Vectors",
                        vector_index.ntotal
                    )

                except Exception as e:

                    st.error(
                        f"Embedding or FAISS error: {e}"
                    )

            else:

                st.warning("No document chunks were generated.")


# =====================================
# DOCUMENT SUMMARY
# =====================================

elif menu == "Document Summary":

    st.header("📝 Generate Document Summary")

    if not st.session_state.all_chunks:

        st.warning(
            "Please upload and process documents first."
        )

    else:

        st.write(
            "Generate short summaries, detailed explanations "
            "and important points from your documents."
        )

        selected_docs = st.multiselect(
            "Select documents",
            options=st.session_state.processed_files,
            default=st.session_state.processed_files,
            key="summary_documents"
        )

        summary_option = st.selectbox(
            "Choose Summary Type",
            [
                "Short Summary",
                "Detailed Summary",
                "Important Points"
            ]
        )

        summary_types = {
            "Short Summary": "short",
            "Detailed Summary": "detailed",
            "Important Points": "points"
        }

        if st.button("Generate Summary"):

            if not selected_docs:

                st.warning(
                    "Please select at least one document."
                )

            else:

                selected_chunks = [
                    chunk
                    for chunk in st.session_state.all_chunks
                    if chunk.get("source") in selected_docs
                ]

                try:

                    with st.spinner(
                        "Llama 3.2 is generating your summary..."
                    ):

                        summary = generate_summary(
                            selected_chunks,
                            summary_types[summary_option]
                        )

                    st.subheader("📄 Generated Summary")

                    st.markdown(summary)

                    st.success(
                        "Summary generated successfully!"
                    )

                    st.caption(
                        "Summary generated using your uploaded documents."
                    )

                except Exception as e:

                    st.error(
                        f"Summary generation error: {e}"
                    )


# =====================================
# ASK YOUR DOCUMENTS
# =====================================

elif menu == "Ask Your Documents":

    st.header("💬 Ask Your Documents")

    st.write(
        "Ask questions about your uploaded documents "
        "and get AI-generated answers."
    )

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask AI"):

        if not question.strip():

            st.warning("Please enter a question.")

        elif st.session_state.vector_index is None:

            st.warning(
                "Please upload and process documents first."
            )

        else:

            try:

                # STEP 1: QUESTION EMBEDDING

                with st.spinner("Understanding your question..."):

                    query_embedding = generate_embeddings([
                        {
                            "content": question
                        }
                    ])

                # STEP 2: VECTOR SEARCH

                with st.spinner("Searching relevant documents..."):

                    distances, indices = search_vectors(
                        st.session_state.vector_index,
                        query_embedding[0],
                        top_k=3
                    )

                context_parts = []
                source_details = []

                for score, index in zip(distances, indices):

                    index = int(index)

                    if index < 0:
                        continue

                    if index >= len(st.session_state.all_chunks):
                        continue

                    chunk = st.session_state.all_chunks[index]

                    context_parts.append(
                        f"""
Source: {chunk['source']}
Page: {chunk['page']}
Content: {chunk['content']}
"""
                    )

                    source_details.append({
                        "source": chunk["source"],
                        "page": chunk["page"],
                        "score": float(score),
                        "content": chunk["content"]
                    })

                # STEP 3: CHECK SEARCH RESULTS

                if not context_parts:

                    st.info(
                        "No relevant document sections were found."
                    )

                else:

                    context = "\n\n".join(context_parts)

                    # STEP 4: GENERATE AI ANSWER

                    with st.spinner(
                        "Llama 3.2 is generating your answer..."
                    ):

                        answer = get_ai_response(
                            question,
                            context
                        )

                    st.subheader("🤖 AI Generated Answer")

                    st.markdown(answer)

                    # STEP 5: SHOW SOURCES

                    st.subheader("📚 Source References")

                    for source in source_details:

                        with st.expander(
                            f"{source['source']} - Page {source['page']}"
                        ):

                            st.write(
                                "Similarity score:",
                                round(source["score"], 3)
                            )

                            st.write(source["content"])

            except Exception as e:

                st.error(
                    f"AI Question Answering Error: {e}"
                )


# =====================================
# COMPARE DOCUMENTS
# =====================================

elif menu == "Compare Documents":

    st.header("📊 Compare Documents")

    if len(st.session_state.processed_files) < 2:

        st.warning(
            "Please upload and process at least two documents "
            "to use the comparison feature."
        )

    else:

        st.write(
            "Select two documents to identify similarities "
            "and differences."
        )

        document_a = st.selectbox(
            "Select First Document",
            st.session_state.processed_files,
            index=0,
            key="compare_document_a"
        )

        document_b = st.selectbox(
            "Select Second Document",
            st.session_state.processed_files,
            index=1,
            key="compare_document_b"
        )

        if st.button("Compare Documents"):

            if document_a == document_b:

                st.warning(
                    "Please select two different documents."
                )

            else:

                chunks_a = [
                    chunk
                    for chunk in st.session_state.all_chunks
                    if chunk.get("source") == document_a
                ]

                chunks_b = [
                    chunk
                    for chunk in st.session_state.all_chunks
                    if chunk.get("source") == document_b
                ]

                context_a = build_document_context(
                    chunks_a,
                    max_chars=9000
                )

                context_b = build_document_context(
                    chunks_b,
                    max_chars=9000
                )

                comparison_context = (
                    f"DOCUMENT A: {document_a}\n\n"
                    f"{context_a}\n\n"
                    f"DOCUMENT B: {document_b}\n\n"
                    f"{context_b}"
                )

                comparison_question = f"""
Compare the following two uploaded documents.

Organize the comparison using these headings:

1. Overview of Document A
2. Overview of Document B
3. Similarities
4. Key Differences
5. Important Observations

Use a comparison table wherever useful.

Mention only information supported by the documents.
Do not invent facts.

Compare {document_a} and {document_b}.
"""

                try:

                    with st.spinner(
                        "AI is comparing both documents..."
                    ):

                        comparison = get_ai_response(
                            comparison_question,
                            comparison_context
                        )

                    st.subheader("📊 Document Comparison")

                    st.markdown(comparison)

                    st.success(
                        "Document comparison completed!"
                    )

                    st.caption(
                        "Comparison is based on the available extracted text."
                    )

                except Exception as e:

                    st.error(
                        f"Comparison error: {e}"
                    )


# =====================================
# GENERATE CHECKLIST
# =====================================

elif menu == "Generate Checklist":

    st.header("✅ Generate Actionable Checklist")

    if not st.session_state.all_chunks:

        st.warning(
            "Please upload and process documents first."
        )

    else:

        st.write(
            "Generate an actionable checklist from your uploaded documents."
        )

        selected_docs = st.multiselect(
            "Select documents for checklist generation",
            options=st.session_state.processed_files,
            default=st.session_state.processed_files,
            key="checklist_documents"
        )

        checklist_goal = st.text_area(
            "What kind of checklist do you need?",
            placeholder=(
                "Example: Create a checklist of important tasks, "
                "requirements and deadlines."
            )
        )

        if st.button("Generate Checklist"):

            if not selected_docs:

                st.warning(
                    "Please select at least one document."
                )

            else:

                selected_chunks = [
                    chunk
                    for chunk in st.session_state.all_chunks
                    if chunk.get("source") in selected_docs
                ]

                context = build_document_context(
                    selected_chunks,
                    max_chars=18000
                )

                if not context.strip():

                    st.warning(
                        "No readable content found in selected documents."
                    )

                else:

                    if checklist_goal.strip():

                        task = checklist_goal

                    else:

                        task = (
                            "Create a practical actionable checklist "
                            "based on the uploaded documents."
                        )

                    checklist_question = f"""
{task}

Use only the information available in the uploaded documents.

Create a properly organized checklist using these sections:

### Important Tasks
- [ ] Write each task on a separate line.

### Requirements
- [ ] Write each requirement separately.

### Necessary Actions
- [ ] Write each action separately.

### Deadlines and Dates
- [ ] Include only dates explicitly mentioned in the documents.

Instructions:

1. Use simple English.
2. Keep each checkbox short and clear.
3. Do not combine multiple tasks in one checkbox.
4. Do not invent deadlines, dates or requirements.
5. If no deadline is mentioned, write:
   No explicit deadline found.
6. Do not repeat the same task.
7. Return the checklist in Markdown format.
"""

                    try:

                        with st.spinner(
                            "Llama 3.2 is generating your checklist..."
                        ):

                            checklist = get_ai_response(
                                checklist_question,
                                context
                            )

                        st.subheader("✅ Generated Checklist")

                        formatted_checklist = format_checklist_output(
                            checklist
                        )

                        st.markdown(formatted_checklist)

                        st.success(
                            "Checklist generated successfully!"
                        )

                        st.caption(
                            "Checklist generated using your uploaded documents."
                        )

                    except Exception as e:

                        st.error(
                            f"Checklist generation error: {e}"
                        )


# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
    "AI-Powered Document Intelligence Agent | "
    "Python + Streamlit + Ollama + Llama 3.2 + FAISS + RAG"
)
