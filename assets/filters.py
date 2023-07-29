import django_filters

from .models import *

class AssetFilter(django_filters.FilterSet):
    class Meta:
        model = Assets
        fields = ('Employee','Departments','Asset_State')

class AssetFilter_User(django_filters.FilterSet):
    class Meta:
        model = Assets
        fields = ('Employee','Departments')