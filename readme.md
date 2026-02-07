# LLM-Assisted COREP Reporting Prototype

## Overview

This is a small prototype exploring how **large language models (LLMs)** can assist with **PRA COREP regulatory reporting**.

COREP reporting requires analysts to interpret dense regulatory text and map it to specific reporting rows. This project demonstrates a **simple, end-to-end workflow** where a natural-language question and reporting scenario are used to retrieve relevant regulatory rules and generate structured COREP-style output.

The focus is on **regulatory interpretation and traceability**, not full automation or production use.

---

## Scope

This prototype supports a **very limited subset** of COREP:

- Template: **C 01.00 – Own Funds**
- Capital tier: **Common Equity Tier 1 (CET1)**
- Supported rows:
  - 010 – Ordinary shares  
  - 020 – Share premium  
  - 030 – Retained earnings  
  - 060 – Total CET1

Only basic examples are covered.

---

## How It Works

1. **Ingest Rules**: Load regulatory text from `data/rules.txt` into ChromaDB using LLM embeddings
2. **Retrieve**: Query the vector store to find relevant rules based on a question
3. **Generate**: Pass rules to a local LLM (Ollama) along with a reporting scenario
4. **Output**: Get structured JSON aligned to the COREP schema with regulatory justifications

### Workflow

```
User Question + Scenario
    ↓
retrieve_rules.py (ChromaDB similarity search)
    ↓
Relevant Regulatory Rules
    ↓
generate_corep.py (Ollama LLM inference)
    ↓
Structured JSON Output with Justifications
```

---

## Project Structure

```
.
├── readme.md                 # This file
├── problem_statement.txt     # Project requirements
├── .env                      # Environment variables (Ollama URL, model names)
├── data/
│   └── rules.txt            # Regulatory rules (CRR extracts)
├── src/
│   ├── corep_schema.py      # COREP C01.00 schema definition
│   ├── ingest_rules.py      # Load and ingest rules into ChromaDB
│   ├── retrieve_rules.py    # Query ChromaDB for relevant rules
│   └── generate_corep.py    # Generate COREP JSON via LLM
├── chroma_db/              # ChromaDB vector store (generated)
├── venv/                   # Python virtual environment
└── .gitignore             # Git ignore patterns
```

---

## Tech Stack

- **Python 3.x**
- **Ollama** (local LLM inference)
- **LangChain** (LLM orchestration and embeddings)
- **ChromaDB** (vector database for semantic search)

All models run locally with no external API calls.

---

## Setup

1. Install Python dependencies:
   ```bash
   pip install langchain langchain-ollama langchain-chroma chromadb
   ```

2. Install and start Ollama:
   - Download from [ollama.ai](https://ollama.ai)
   - Pull required models:
     ```bash
     ollama pull gemma2:4b
     ollama pull embedding-gemma
     ```

3. Ingest regulatory rules into ChromaDB:
   ```bash
   python src/ingest_rules.py
   ```

4. Generate COREP output:
   ```bash
   python src/generate_corep.py
   ```

---

## Example Output

```json
{
  "template": "C01.00",
  "fields": {
    "CET1_RetainedEarnings": {
      "value": 1200000,
      "row": "030",
      "justification": "CRR Article 26(1)(c)"
    }
  }
}
```

---

## Requirements

- **Ollama** running locally on `http://localhost:11434`
- Models: `gemma2:4b` (generation), `embedding-gemma` (embeddings)
- Python 3.8+
