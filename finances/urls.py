from django.urls import path

from . import views

urlpatterns = [
    # Tables
    path("tables/", views.TableListView.as_view(), name="table_list"),
    path("tables/new/", views.TableCreateView.as_view(), name="table_create"),
    path("tables/<int:pk>/edit/", views.TableUpdateView.as_view(), name="table_update"),
    path("tables/<int:pk>/delete/", views.TableDeleteView.as_view(), name="table_delete"),
    path("tables/<int:table_id>/analytics/", views.TableAnalyticsView.as_view(), name="table_analytics"),

    # Transactions (nested під table)
    path("tables/<int:table_id>/transactions/", views.TransactionListView.as_view(), name="transaction_list"),
    path("tables/<int:table_id>/transactions/new/", views.TransactionCreateView.as_view(), name="transaction_create"),
    path("transactions/<int:pk>/edit/", views.TransactionUpdateView.as_view(), name="transaction_update"),
    path("transactions/<int:pk>/delete/", views.TransactionDeleteView.as_view(), name="transaction_delete"),
]
