from langchain.tools import tool
from app.rag.retriver import retriver_documents

@tool
def search_knowledge_base(query: str) -> str:
    """Search the support knowledge base for general policy and how-to answers
    (returns, refunds, shipping, warranty, account help). Use for general
    questions, NOT for looking up a specific customer's order."""
    responses = retriver_documents(query=query)

    if not responses:
        return "No relevant information found in the knowledge base."

    return "\n\n".join(f"[{r.source}/{r.intent}] {r.response}" for r in responses)