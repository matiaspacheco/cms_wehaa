from django.contrib import admin

# Register your models here.
from .models import Category, Article

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'image', 'approved')
    list_filter = ('name', 'approved',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name', ]


# Registers the category model at the admin backend.
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('category', 'title', 'slug', 'author', 'image', 'image_credit',
                    'body', 'date_published', 'status')
    list_filter = ('status', 'date_created', 'date_published', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_published'
    ordering = ['status', '-date_created', ]
    readonly_fields = ('views', 'count_words',)


# Registers the article model at the admin backend.
admin.site.register(Article, ArticleAdmin)