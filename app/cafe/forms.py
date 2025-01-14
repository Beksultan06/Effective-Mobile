from django import forms
from app.cafe.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']

    items = forms.CharField(widget=forms.Textarea, label='Список блюд и цен', help_text='Введите список блюд в формате: название_блюда:цена')

    def clean_items(self):
        """
        Преобразует строку в формат JSON.
        """
        items_str = self.cleaned_data['items']
        try:
            items_list = []
            for item in items_str.split("\n"):
                if item.strip():
                    name, price = item.split(":")
                    items_list.append({"name": name.strip(), "price": float(price.strip())})
            return items_list
        except ValueError:
            raise forms.ValidationError('Неверный формат списка блюд и цен. Используйте формат: название_блюда:цена')
