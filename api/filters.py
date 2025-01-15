from django_filters import rest_framework as filters
from app.cafe.models import Order
from app.cafe.status import STATUS_CHOICES

class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=STATUS_CHOICES, method='filter_by_status')

    def filter_by_status(self, queryset, name, value):
        if value:
            return queryset.filter(status=value)
        return queryset

    class Meta:
        model = Order
        fields = ['table_number', 'status']
