# 🚀 Claim Processing Pipeline (FastAPI + LangGraph)
## 🎥 Demo

A quick walkthrough of the full pipeline (PDF → classification → structured output):

👉 https://www.loom.com/share/31eb711cc7464bcc8ce8ddb64d62d85b

---

An AI-powered backend system that processes health insurance claim PDFs and extracts structured data using **LangGraph-based multi-agent workflows**.

---

## 🧠 Problem

Health insurance claims involve multiple document types such as:

* Claim forms
* Discharge summaries
* Itemized bills
* Prescriptions
* Reports

Manual processing is:

* Slow
* Error-prone
* Not scalable

👉 This project automates the entire pipeline using **LLMs + agent orchestration**

---

## ⚙️ Solution Overview

The system:

1. Accepts a claim PDF
2. Extracts text using OCR
3. Classifies each page into document types
4. Routes pages to specialized AI agents
5. Aggregates structured output

---

## 🔄 LangGraph Workflow

```text
START → Segregator Agent
        ↓
   ┌───────────────┐
   │   LangGraph   │
   └───────────────┘
        ↓
   ↓        ↓        ↓
 ID Agent  Discharge  Billing
   ↓        ↓        ↓
        Aggregator
            ↓
           END
```

---

## 🧩 Components

### 🔹 1. Segregator Agent (LLM-powered)

* Classifies each page into 9 document types:

  * claim_forms
  * cheque_or_bank_details
  * identity_document
  * itemized_bill
  * discharge_summary
  * prescription
  * investigation_report
  * cash_receipt
  * other

* Ensures:

  * Every page is classified
  * No page is dropped (fallback logic)

---

### 🔹 2. Extraction Agents

Each agent processes **only relevant pages** routed by the segregator.

#### ✅ ID Agent

Extracts:

* Patient name
* Date of birth
* Policy number

> Identity data may appear across multiple documents, so the agent aggregates context for better accuracy.

---

#### ✅ Discharge Summary Agent

Extracts:

* Diagnosis
* Admission date
* Discharge date
* Physician details

---

#### ✅ Itemized Bill Agent

Extracts:

* Individual billing items
* Quantity, rate, amount
* Total bill amount

---

### 🔹 3. Aggregator Node

* Combines outputs from all agents
* Returns final structured JSON

---

## 🧪 API Endpoint

### `POST /api/process`

### Input:

* `claim_id` (string)
* `file` (PDF)

### Output:

```json
{
  "claim_id": "123",
  "classification": { "...": "..." },
  "extracted_data": {
    "id": { "...": "..." },
    "discharge_summary": { "...": "..." },
    "itemized_bill": { "...": "..." }
  }
}
```

---

## 🛠️ Tech Stack

* **FastAPI** – API layer
* **LangGraph** – workflow orchestration
* **OpenAI (gpt-4o-mini)** – LLM processing
* **Tesseract OCR** – text extraction

---

## 📂 Project Structure

```text
├── app/
│   ├── main.py
│   └── routes.py
│
├── services/
│   ├── pdf_loader.py
│   ├── ocr_service.py
│   └── llm_segregator.py
│
├── graph/
│   └── workflow.py
│
└── README.md
```

---

## ⚡ Setup & Run

```bash
git clone <repo>
cd claim-pipeline
pip install -r requirements.txt
```

---

## 🚀 Setup Instructions

### 1. Set API Key

```bash
setx OPENAI_API_KEY "your_api_key"
```

### 2. Run Server

```bash
uvicorn app.main:app --reload
```

### 3. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🎯 Key Design Decisions

* Used **LangGraph** for explicit multi-agent orchestration
* Avoided **per-page LLM calls** → reduced cost & latency
* Added **fallback logic** → ensures no page is missed
* Designed agents **modularly** → easy to scale

---

## 🚀 Future Improvements

* Hybrid classification (**rule-based + LLM**)
* Async processing for large PDFs
* Store outputs in **PostgreSQL**
* Add vector database for semantic retrieval

---

## 👨‍💻 Author

**Rohan**
Backend Developer | AI Systems
