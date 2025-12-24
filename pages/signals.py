from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Page

@receiver(post_save, sender=Page)
def update_page_search(sender, instance, **kwargs):
    Page.objects.filter(id=instance.id).update(
        search_vector=(
            SearchVector("title", weight="A") +
            SearchVector("content", weight="B")
        )
    )