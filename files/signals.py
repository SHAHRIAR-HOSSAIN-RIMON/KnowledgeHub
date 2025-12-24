from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FileAsset

@receiver(post_save, sender=FileAsset)
def update_file_search(sender, instance, **kwargs):
    FileAsset.objects.filter(id=instance.id).update(
        search_vector=SearchVector("filename")
    )
