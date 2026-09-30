from langchain_openai import ChatOpenAI

from jolly_flow import cliproxy

def get_model(model_id: str):
    return ChatOpenAI(
        model=model_id,
        openai_api_key=cliproxy.api_key(),
        openai_api_base=cliproxy.base_url(),
        temperature=0
    )
