from langgraph.graph import StateGraph
from typing import TypedDict
from openai import OpenAI
import json

# 🔑 Use your working key here (for assignment simplicity)
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


# ✅ State Schema
class GraphState(TypedDict, total=False):
    claim_id: str
    pages: list
    classification: dict

    id_data: dict
    discharge_data: dict
    billing_data: dict


# --- Nodes ---

def segregator_node(state: GraphState):
    return state


def id_agent_node(state: GraphState):
    pages = state.get("pages", [])
    classification = state.get("classification", {})
    relevant_pages = list(set(
        classification.get("identity_document", []) +
        classification.get("claim_forms", []) +
        classification.get("discharge_summary", [])
    ))
    text = "\n".join(
        page["text"][:1500]
        for page in pages
        if page["page_number"] in relevant_pages
    )

    if not text.strip():
        return {"id_data": {}}

    prompt = f"""
    You are an expert medical document parser.

    Extract patient identity details from the text below.

    IMPORTANT:
    - Information may appear across multiple pages
    - Look carefully across ALL content
    - DO NOT return null if value exists
    - Return ONLY valid JSON

    Extract:
    - patient_name
    - date_of_birth
    - policy_number

    Text:
    {text}
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return {"id_data": json.loads(res.choices[0].message.content)}
    except:
        return {"id_data": {}}


def discharge_agent_node(state: GraphState):
    pages = state.get("pages", [])
    relevant_pages = state.get("classification", {}).get("discharge_summary", [])

    text = "\n".join(
        page["text"][:1500]
        for page in pages
        if page["page_number"] in relevant_pages
    )

    if not text.strip():
        return {"discharge_data": {}}

    prompt = f"""
You are a medical document extraction system.

Extract:
- diagnosis
- admission_date
- discharge_date
- physician_name

Return ONLY JSON.

Text:
{text}
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return {"discharge_data": json.loads(res.choices[0].message.content)}
    except:
        return {"discharge_data": {}}


def bill_agent_node(state: GraphState):
    pages = state.get("pages", [])
    relevant_pages = state.get("classification", {}).get("itemized_bill", [])

    text = "\n".join(
        page["text"][:1500]
        for page in pages
        if page["page_number"] in relevant_pages
    )

    if not text.strip():
        return {"billing_data": {}}

    prompt = f"""
You are a medical billing extraction system.
Return ONLY valid JSON.

Extract:
- items (list of objects with name, qty, rate, amount)
- total_amount

Text:
{text}
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return {"billing_data": json.loads(res.choices[0].message.content)}
    except:
        return {"billing_data": {}}


def aggregator_node(state: GraphState):
    return {
        "id": state.get("id_data"),
        "discharge_summary": state.get("discharge_data"),
        "itemized_bill": state.get("billing_data"),
    }


# --- Build Graph ---

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("segregator", segregator_node)
    builder.add_node("id_agent", id_agent_node)
    builder.add_node("discharge_agent", discharge_agent_node)
    builder.add_node("bill_agent", bill_agent_node)
    builder.add_node("aggregator", aggregator_node)

    builder.set_entry_point("segregator")

    # Parallel execution
    builder.add_edge("segregator", "id_agent")
    builder.add_edge("segregator", "discharge_agent")
    builder.add_edge("segregator", "bill_agent")

    # Merge into aggregator
    builder.add_edge("id_agent", "aggregator")
    builder.add_edge("discharge_agent", "aggregator")
    builder.add_edge("bill_agent", "aggregator")

    return builder.compile()