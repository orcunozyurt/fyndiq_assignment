from django.contrib import admin
from models import WordList,PairedUrl
# Register your models here.
class WordListAdmin(admin.ModelAdmin):
    list_display = ['id', 'word', 'is_used']
    pass

class PairedUrlAdmin(admin.ModelAdmin):
    model = PairedUrl
    extra = 3
    
    
admin.site.register(WordList, WordListAdmin)
admin.site.register(PairedUrl, PairedUrlAdmin)