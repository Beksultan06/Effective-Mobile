from rest_framework import serializers
from app.cafe.models import Order

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "table_number", "items", "total_price", "status")
        exclude = []