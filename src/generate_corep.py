import json
import requests
from retrieve_rules import retrieve_rules
from corep_schema import COREP_OWN_FUNDS_SCHEMA

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text


def generate_corep(scenario, question):
    rules = retrieve_rules(question)

    rules_text = "\n".join(
        f"- ({r.metadata['row']}) {r.page_content}"
        for r in rules
    )

    prompt = f"""
You are a UK PRA COREP regulatory reporting assistant.

Scenario:
{scenario}

Relevant regulatory rules:
{rules_text}

COREP Template: {COREP_OWN_FUNDS_SCHEMA['template']}

Return STRICT JSON only:

{{
  "template": "C01.00",
  "fields": {{
    "CET1_RetainedEarnings": {{
      "value": <number or null>,
      "row": "030",
      "justification": "<rule reference>"
    }}
  }}
}}

No explanations. No markdown.
"""

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    ).json()

    llm_text = res.get("response") or res.get("message", {}).get("content")
    print("RAW LLM OUTPUT:\n", llm_text)

    return json.loads(clean_json(llm_text))


if __name__ == "__main__":
    scenario = """
    The institution has retained earnings of GBP 1,200,000
    as of the reporting date.
    """

    question = "How should retained earnings be reported in Common Equity Tier 1 capital?"

    output = generate_corep(scenario, question)
    print("\n✅ FINAL COREP OUTPUT\n")
    print(json.dumps(output, indent=2))
