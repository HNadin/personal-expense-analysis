from django.db import migrations

DEFAULT_CATEGORIES = [
    ("Продукти", "Витрати на їжу, продукти зі супермаркету"),
    ("Авто", "Паливо, ремонт, страховка, паркінг"),
    ("Одяг", "Одяг, взуття, аксесуари"),
    ("Транспорт", "Громадський транспорт, таксі"),
    ("Розваги", "Кафе, ресторани, кіно, ігри"),
    ("Здоров'я", "Ліки, лікарі, спортзал"),
    ("Комунальні", "Світло, газ, інтернет, оренда"),
    ("Інше", "Все, що не підходить під інші категорії"),
]


def create_default_categories(apps, schema_editor):
    Category = apps.get_model("finances", "Category")
    for name, description in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            name=name,
            defaults={"description": description},
        )


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model("finances", "Category")
    Category.objects.filter(name__in=[name for name, _ in DEFAULT_CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ]