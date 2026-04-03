from fastapi import APIRouter, UploadFile, File, Form
from services.pdf_loader import extract_pages_from_pdf
from services.llm_segregator import llm_segregator
from graph.workflow import build_graph

router = APIRouter()

# 🔥 initialize graph once
graph = build_graph()


@router.post("/api/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()

    # Step 1: Extract pages
    pages = extract_pages_from_pdf(file_bytes)

    # Step 2: Segregation (LLM)
    classification = llm_segregator(pages)

    # Step 3: Run LangGraph pipeline
    result = graph.invoke({
        "claim_id": claim_id,
        "pages": pages,
        "classification": classification
    })

    return {
        "claim_id": claim_id,
        "classification": classification,
        "extracted_data": result
    }