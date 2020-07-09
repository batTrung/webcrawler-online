import os
import zipfile
from io import BytesIO
import requests
from django.shortcuts import render, \
							redirect,\
							get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponse, Http404
from myproject.celery import app
from .forms import ItemForm
from .models import Item, File
from .tasks import async_website
from .helpers import generate_tree, get_zip_file


def home(request):
	return render(request,
				'services/home.html')


def contact(request):
	return render(request,
				'services/contact.html')


def item_register(request):
	data = {}
	if request.method == 'POST':
		itemForm = ItemForm(request.POST)
		if itemForm.is_valid():
			item = itemForm.save()
			web_task = async_website.delay(item.slug)
			data['html_item_form'] = render_to_string(
								'services/includes/form_success.html',
								{
									'item': item,
									'id_task': web_task.id
								},
								request=request)
		else:
			if itemForm['url'].errors:
				messages.error(request, 'Đường dẫn không hợp lệ')
			elif itemForm['email'].errors:
				messages.error(request, 'Địa chỉ email không đúng')
			data['html_item_form'] = render_to_string(
								'services/includes/html_item_form.html',
								{'itemForm': ItemForm},
								request=request)
		return JsonResponse(data)
	else:
		itemForm = ItemForm()

	return render(request,
				'services/item/form.html',
				{'itemForm': ItemForm})


def site_download(request, slug):
	item = get_object_or_404(Item, slug=slug)
	tree_html = generate_tree(item)
	index_path = '/'.join((item.slug, 'index.html'))
	try:
		index = File.objects.get(item=item, path=index_path)
	except:
		index = None

	context = {
		'item': item,
		'index': index,
		'tree_html': tree_html}

	return render(request,
				'services/item/site-download.html',
				context)

def site_preview(request, file_path):
	file_path = file_path.rstrip('/')
	file = File.objects.filter(path=file_path).first()
	if not file:
		raise Http404

	return render(request,
				'/'.join(('websites', file.path)))


def site_refresh(request, slug):
	item = get_object_or_404(Item, slug=slug)
	item.files.all().delete()
	async_website.delay(item.slug)

	return redirect('site_download', slug)


def download_file(request, slug):
	item = get_object_or_404(Item, slug=slug)

	zip_filename = "%s.zip" % slug
	
	filenames = []
	path_temp_item = '/'.join((settings.TEMP_PATH, slug))
	path_static_item = '/'.join((settings.STATIC_PATH, slug))

	s = BytesIO()
	zip_file = zipfile.ZipFile(s, "w")
	
	zip_file = get_zip_file(zip_file, path_static_item, slug)
	zip_file = get_zip_file(zip_file, path_temp_item, slug)
	
	zip_file.close()

	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp


def stop_download(request, task_id):
	 app.control.revoke(task_id)

	 return HttpResponse("success")
