from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Item, File
from .clean import clear_dirs


@receiver(pre_delete, sender=Item)
@receiver(pre_delete, sender=File)
def remove_directory(sender, instance, **kwargs):
	if instance.__class__.__name__ == 'File':
		instance = instance.item

	slug = instance.slug
	clear_dirs(slug)




