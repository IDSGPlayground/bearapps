from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from store.models import User, App, Chartstring, Group
from tastypie import fields

class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'groups'
        fields = ['name']

class UserResource(ModelResource):
    groups = fields.ManyToManyField(GroupResource, 'groups')
    class Meta:
        queryset = User.objects.all()
        resources_name = 'user'
        excludes = ['password']
        # authorization = Authorization()


class AppResource(ModelResource):
    class Meta:
        queryset = App.objects.all()
        resource_name = 'app'


class ChartResource(ModelResource):
    group = fields.ManyToManyField(GroupResource, 'groups')
    manager = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Chartstring.objects.all()
        resource_name = 'chartstring'
