from django.contrib import admin

from .models import Category, Table, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "color", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "owner__email")
    autocomplete_fields = ("owner",)
    ordering = ("-created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "currency", "date", "table")
    list_filter = ("currency", "date", "categories")
    search_fields = ("title", "table__name", "table__owner__email")
    autocomplete_fields = ("table",)
    filter_horizontal = ("categories",)
    date_hierarchy = "date"
    ordering = ("-date",)
