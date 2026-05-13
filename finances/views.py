from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import TableForm, TransactionForm
from .mixins import OwnerQuerysetMixin, TableOwnerQuerysetMixin
from .models import Table, Transaction


# === Table CRUD ===

class TableListView(OwnerQuerysetMixin, ListView):
    model = Table
    template_name = "finances/table_list.html"
    context_object_name = "tables"


class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = "finances/table_form.html"
    success_url = reverse_lazy("table_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TableUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = "finances/table_form.html"
    success_url = reverse_lazy("table_list")


class TableDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Table
    template_name = "finances/table_confirm_delete.html"
    success_url = reverse_lazy("table_list")


# === Transaction CRUD ===

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "finances/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 25

    def get_queryset(self):
        self.table = get_object_or_404(Table, pk=self.kwargs["table_id"], owner=self.request.user)
        qs = Transaction.objects.filter(table=self.table).prefetch_related("categories")

        # Пошук за title
        search = self.request.GET.get("search", "").strip()
        if search:
            search_lower = search.lower()
            matched_ids = [
                t.pk for t in qs.only("pk", "title")
                if search_lower in (t.title or "").lower()
            ]
            qs = qs.filter(pk__in=matched_ids)

        # Фільтр за категорією
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(categories__id=category_id)

        # Фільтр за датою
        date_from = self.request.GET.get("date_from")
        if date_from:
            qs = qs.filter(date__gte=date_from)
        date_to = self.request.GET.get("date_to")
        if date_to:
            qs = qs.filter(date__lte=date_to)

        # Сортування (за замовчуванням — нові спочатку, з моделі)
        sort = self.request.GET.get("sort")
        if sort in ("date", "-date"):
            qs = qs.order_by(sort)
            return qs.distinct()

        if sort in ("amount", "-amount"):
            # Сортування за сумою — у Python, бо треба врахувати валюту через amount_in_uah.
            # Це OK для невеликих обсягів; на тисячах транзакцій треба буде anотейшн на SQL.
            qs = list(qs.distinct())
            qs.sort(key=lambda t: t.amount_in_uah, reverse=(sort == "-amount"))
            return qs

        return qs.distinct()

    def get_context_data(self, **kwargs):
        from .models import Category
        ctx = super().get_context_data(**kwargs)
        ctx["table"] = self.table
        ctx["categories"] = Category.objects.all()
        ctx["filters"] = {
            "search": self.request.GET.get("search", ""),
            "category": self.request.GET.get("category", ""),
            "date_from": self.request.GET.get("date_from", ""),
            "date_to": self.request.GET.get("date_to", ""),
            "sort": self.request.GET.get("sort", ""),
        }
        return ctx


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finances/transaction_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.table = get_object_or_404(
            Table, pk=self.kwargs["table_id"], owner=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.table = self.table
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("transaction_list", kwargs={"table_id": self.table.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["table"] = self.table
        return ctx


class TransactionUpdateView(TableOwnerQuerysetMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finances/transaction_form.html"

    def get_success_url(self):
        return reverse_lazy("transaction_list", kwargs={"table_id": self.object.table.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["table"] = self.object.table
        return ctx


class TransactionDeleteView(TableOwnerQuerysetMixin, DeleteView):
    model = Transaction
    template_name = "finances/transaction_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("transaction_list", kwargs={"table_id": self.object.table.pk})