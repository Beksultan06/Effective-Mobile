from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class OrderPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        print("Следующая страница:", self.get_next_link())
        print("Предыдущая страница:", self.get_previous_link())
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })