from django.contrib import admin
from .models import Category, Post


def nullfy_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)
    nullfy_quantity.short_description = 'Обнулить новости'

class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ('name', 'categoty', 'rating')
    search_fields = ('name', 'categoty', 'rating')
    actions = [nullfy_quantity]


admin.site.register(Category)
admin.site.register(Post)
