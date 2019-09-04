import uuid
from urllib.parse import urlparse
from django.db import models
from django.template.defaultfilters import slugify


class Item(models.Model):
	id = models.UUIDField(primary_key=True,
						default=uuid.uuid4,
						editable=False)
	slug = models.SlugField(blank=True, unique=True)
	url = models.URLField()
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		name = urlparse(self.url).netloc \
				+ '_' \
				+ self.email \
				+ str(self.id)
		self.slug = slugify(name)
		super(Item, self).save(*args, **kwargs)

	def __str__(self):
		return self.url
