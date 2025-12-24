from .providers.deepseek import DeepSeekProvider

def get_ai_provider():
    return DeepSeekProvider()

def generate_embedding(text: str):
    provider = get_ai_provider()
    return provider.generate_embedding(text)
