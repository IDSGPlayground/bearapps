# from tastypie.resources import Authorization
from tastypie.resources import ModelResource
from store.models import User, App, Chartstring, Group


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resources_name = 'user'
        # authorization = Authorization()


class AppResource(ModelResource):
    class Meta:
        queryset = App.objects.all()
        resource_name = 'app'


class ChartResource(ModelResource):
    class Meta:
        queryset = Chartstring.objects.all()
        resource_name = 'chartstring'


class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'groups'
