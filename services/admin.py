from django.contrib import admin
from .models import Item, File


class FileInline(admin.StackedInline):
	model = File


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('slug', 'url', 'email')
	inlines = [FileInline]

