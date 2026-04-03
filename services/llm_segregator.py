from openai import OpenAI
import json

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

CATEGORIES = [
    "claim_forms",
    "cheque_or_bank_details",
    "identity_document",
    "itemized_bill",
    "discharge_summary",
    "prescription",
    "investigation_report",
    "cash_receipt",
    "other"
]






def llm_segregator(pages: list) -> dict:
    classification = {key: [] for key in CATEGORIES}

    # 🔥 Build input (LIMIT to 10 pages to avoid overload)
    input_text = ""
    for page in pages[:10]:
        input_text += f"\nPage {page['page_number']}:\n{page['text'][:800]}\n"

    prompt = f"""
You are a medical document classification system.

Classify EACH page into ONE category:

- claim_forms
- cheque_or_bank_details
- identity_document
- itemized_bill
- discharge_summary
- prescription
- investigation_report
- cash_receipt
- other

Rules:
- Every page MUST be classified
- Return ONLY JSON
- Do NOT skip any page

Return format:
{{
  "claim_forms": [],
  "cheque_or_bank_details": [],
  "identity_document": [],
  "itemized_bill": [],
  "discharge_summary": [],
  "prescription": [],
  "investigation_report": [],
  "cash_receipt": [],
  "other": []
}}
Return ONLY page numbers as integers (e.g., 0,1,2). Do NOT return "Page 0".
Text:
{input_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # 🔥 CLEAN markdown JSON if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        result = json.loads(content)
    except:
        return classification

    # 🔥 Direct assignment (correct logic)
    for category in CATEGORIES:
        if category in result:
            classification[category] = result[category]

    # 🔥 Ensure no page is missed
    all_pages = {page["page_number"] for page in pages}
    classified_pages = set()

    for pages_list in classification.values():
        classified_pages.update(pages_list)

    missing_pages = all_pages - classified_pages

    if missing_pages:
        classification["other"].extend(list(missing_pages))

    return classification