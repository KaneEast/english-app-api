from django.contrib import admin
from .models import Celebrity, Quote

class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1  # 默认显示一个空的输入行

@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']
    search_fields = ['name', 'title']
    inlines = [QuoteInline]

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['content', 'celebrity', 'tag']
    search_fields = ['content', 'tag']
    list_filter = ['celebrity', 'tag']
