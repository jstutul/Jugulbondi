import django_filters
from accounts.models import *

class SearhPatner(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ('gender','marital_status','body_type','religion','education')
