from langchain_openai import ChatOpenAI

def get_model(model_id: str):
    return ChatOpenAI(
        model=model_id,
        openai_api_key="sk-h4X6yuCGDs0p2Wdx3oJ3Z3Pnc1O9XeDuTqD1V9NqrM3yH",
        openai_api_base="http://localhost:8317/v1",
        temperature=0
    )
