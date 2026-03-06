import os

provider = os.getenv("LLM_PROVIDER", "ollama")

if provider == "ollama":
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="mistral",
        base_url="http://host.docker.internal:11434"
    )

else:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=0
    )