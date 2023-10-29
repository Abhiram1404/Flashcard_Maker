import filters
from .models import FlashCard
from filters import DateFilter


class OrderFilter(filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr="gte")
	class Meta:
		model = FlashCard
		fields = ['front', 'back', 'category']