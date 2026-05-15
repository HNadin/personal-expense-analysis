from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Обмежує queryset тільки об'єктами, які належать поточному юзеру.
    Працює для будь-якої моделі, у якої є поле owner (FK на User).
    """

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TableOwnerQuerysetMixin(LoginRequiredMixin):
    """
    Те саме, але через зв'язок table__owner. Для моделей, які належать юзеру опосередковано
    (Transaction належить юзеру через Table).
    """

    def get_queryset(self):
        return super().get_queryset().filter(table__owner=self.request.user)
