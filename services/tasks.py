from django.shortcuts import get_object_or_404
from .models import Item
from celery import shared_task
from myproject.celery import app
from celery.exceptions import SoftTimeLimitExceeded
from .crawlers import Crawler
from .clean import clean_dirs


@app.task(soft_time_limit=60*60)
def async_website(slug):
	try:
		item = get_object_or_404(Item, slug=slug)
		c = Crawler(item, async_website.request.id)
		c.main()
	except SoftTimeLimitExceeded:
		print("STOP TIME LIMIT!!!!!!!!!!!")
