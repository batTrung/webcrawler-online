from django import forms
from .models import Item
from .clean import validate_url


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('url', 'email',)
	
	def clean_url(self):
		url = self.cleaned_data['url']
		if validate_url(url) is None:
			raise forms.ValidationError('Đường dẫn không hợp lệ')

		return url