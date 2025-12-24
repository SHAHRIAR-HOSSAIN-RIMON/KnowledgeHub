from .models import KnowledgeEmbedding
from .services import generate_embedding

def index_page(page):
    KnowledgeEmbedding.objects.update_or_create(
        workspace=page.workspace,
        source_type="page",
        source_id=page.id,
        defaults={
            "content": page.content,
            "embedding": generate_embedding(page.content),
        }
    )
