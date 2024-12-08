from django.db import models

class Category(models.Model):
    """
    Модель категории для классификации объектов или записей.

    Attributes:
        name (str): Название категории, отображаемое в интерфейсе и используемое для фильтрации объектов.
    """

    name: str = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Категория",
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории.

        Returns:
            str: Название категории.
        """
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'