from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading',)
    list_filter = ('is_publicated',)
    search_fields = ('heading', 'text',)