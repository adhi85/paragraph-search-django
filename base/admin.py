from django.contrib import admin
from .models import Paragraph, Word, User

# Register your models here.
admin.site.register(Paragraph)
admin.site.register(Word)
admin.site.register(User)
