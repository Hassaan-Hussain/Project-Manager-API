from django.db.models import Q
import django_filters 
from .models import Team

class TeamFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search",
        label='Name or Description'
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    class Meta:
        model = Team
        fields = []