from django.contrib import admin

from apps.products.models import CategoryModel, IngredientModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ('id', 'name',)


@admin.register(IngredientModel)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ('id', 'name',)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category_name", "branch_name", "price")
    list_display_links = ('id', 'name',)
    list_filter = ("created_at", "category", "branch")

    def category_name(self, obj):
        return obj.category.name

    def branch_name(self, obj):
        return obj.branch.name
