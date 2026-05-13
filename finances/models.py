from django.conf import settings
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#0d6efd", help_text="HEX color, e.g. #0d6efd")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tables",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.owner.email})"


class Transaction(models.Model):
    class Currency(models.TextChoices):
        UAH = "UAH", "Гривня"
        USD = "USD", "Долар США"
        EUR = "EUR", "Євро"

    title = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01"),
                message="Сума має бути більшою за нуль.",
            )
        ],
    )
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UAH)
    date = models.DateField()
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title or 'Transaction'} — {self.amount} {self.currency}"

    _FALLBACK_RATES_TO_UAH = {
        "UAH": 1,
        "USD": 41,
        "EUR": 44,
    }

    @property
    def amount_in_uah(self):
        """Повертає суму, конвертовану в UAH. Тимчасово на фіксованих курсах."""
        rate = self._FALLBACK_RATES_TO_UAH.get(self.currency, 1)
        return self.amount * rate