import requests
from django.shortcuts import render, \
							redirect,\
							get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from .forms import ItemForm
from .models import Item
from .decorators import check_recaptcha


def home(request):
	return render(request,
				'services/home.html')


@check_recaptcha
def item_register(request):
	data = {}
	if request.method == 'POST':
		itemForm = ItemForm(request.POST)
		if itemForm.is_valid() and request.recaptcha_is_valid:
			item = itemForm.save()
			data['html_item_form'] = render_to_string(
								'services/includes/form_success.html',
								{'item': item},
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
	template_path = settings.TEMP_DIR + '/'
	print(template_path)
	r = requests.get('http://themepixels.me/dashforge/lib/@fortawesome/fontawesome-free/css/all.min.css')
	with open(template_path + 'all.min.css', 'w+') as f:
		f.write(r.text)

	context = {
		'item': item}

	return render(request,
				'services/item/site-download.html',
				context)
