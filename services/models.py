import uuid
from urllib.parse import urlparse
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings


class Item(models.Model):
	GOOD = 'G'
	ERROR = 'E'
	CRAWLING = 'C'
	CURRENT_STATUS = (
		(GOOD, '✓ good'),
		(ERROR, '× error'),
		(CRAWLING, '~ running'))

	id = models.UUIDField(primary_key=True,
						default=uuid.uuid4,
						editable=False)
	slug = models.SlugField(max_length=255,
							blank=True,
							unique=True)
	url = models.URLField()
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1,
							default=GOOD,
							choices=CURRENT_STATUS)

	def save(self, *args, **kwargs):
		netloc = urlparse(self.url).netloc
		domain = netloc.strip('www.')\
					.rsplit('.', 1)[0]
		name = domain + '_' + self.email + str(self.id)
		self.slug = slugify(name)
		super(Item, self).save(*args, **kwargs)

	def __str__(self):
		return self.url

	class Meta:
		ordering = ('created',)


class File(models.Model):

	TYPE_CHOICES = (
		('js', 'js'),
		('css', 'css'),
		('html', 'html'),
		('static', 'static'),
	)
	
	item = models.ForeignKey(
						'Item',
						on_delete=models.CASCADE,
						related_name='files')
	path = models.CharField(
						unique=True,
						blank=True,
						max_length=200)
	url = models.URLField()
	category = models.CharField(
						max_length=10,
						choices=TYPE_CHOICES,
						default='html',
						blank=True)
	root = models.BooleanField(default=False)
	content = models.TextField(blank=True)
	crawled = models.BooleanField(default=False)

	def __str__(self):
		return self.path
		
	def root_path(self):
		if self.category == 'html':
			path = settings.TEMP_PATH
		else:
			path = settings.STATIC_PATH
		return '/'.join((path, self.path))

	# def save(self, *args, **kwargs):
	# 	file = File.objects.filter(path = self.path)
	# 	if file.exists():
	# 		if self.content:
	# 			file.content = self.content
	# 			file.save()
	# 		elif self.crawled:
	# 			file.content = self.content
	# 			file.save()
	# 		return file

	# 	super(File, self).save(*args, **kwargs)
