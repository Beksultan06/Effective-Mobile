from django.db import models
from app.cafe.status import STATUS_CHOICES

# Create your models here.
class Order(models.Model):

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    table_number = models.IntegerField(verbose_name='Номер стола')
    items = models.JSONField(verbose_name='список заказов')
    total_price = models.FloatField(editable=False, verbose_name='общая стоимость заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='статус заказа')

    def save(self, *args, **kwargs):
        """
        Пересчитывает общую стоимость заказа, основываясь на стоимости каждого товара.
        """
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id} - Стол #{self.table_number} ({self.status})"