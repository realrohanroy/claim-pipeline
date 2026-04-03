def simple_segregator(pages: list) -> dict:
    result = {
        "claim_forms": [],
        "cheque_or_bank_details": [],
        "identity_document": [],
        "itemized_bill": [],
        "discharge_summary": [],
        "prescription": [],
        "investigation_report": [],
        "cash_receipt": [],
        "other": []
    }

    for page in pages:
        text = page.get("text", "").lower()
        page_number = page.get("page_number")

        if "claim form" in text:
            result["claim_forms"].append(page_number)

        elif (
            "cheque" in text or
            "bank" in text or
            "ifsc" in text or
            "account number" in text
        ):
            result["cheque_or_bank_details"].append(page_number)

        elif (
            "aadhaar" in text or
            "pan" in text or
            "passport" in text or
            "id card" in text or
            "identity" in text
        ):
            result["identity_document"].append(page_number)

        elif (
            "itemized bill" in text or
            "detailed bill" in text or
            "invoice" in text or
            "charges" in text
        ):
            result["itemized_bill"].append(page_number)

        elif "discharge summary" in text:
            result["discharge_summary"].append(page_number)

        elif "prescription" in text or "rx" in text:
            result["prescription"].append(page_number)

        elif (
            "investigation" in text or
            "lab" in text or
            "report" in text or
            "test" in text
        ):
            result["investigation_report"].append(page_number)

        elif "receipt" in text:
            result["cash_receipt"].append(page_number)

        else:
            result["other"].append(page_number)

    return result