from store.models import User_Apps, User, App, Group, Chartstring
from django.contrib import admin

class AppsInline(admin.TabularInline):
	model = User_Apps

class UsersInLine(admin.TabularInline):
	model = User.groups.through

class ChartstringInline(admin.TabularInline):
	model = Chartstring

class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'password', 'SID', 'owner', 'notifications']
    inlines = [AppsInline, UsersInLine]

class GroupAdmin(admin.ModelAdmin):
	inlines = [UsersInLine]



admin.site.register(User, UserAdmin)
admin.site.register(App)
admin.site.register(Group, GroupAdmin)
admin.site.register(Chartstring)
# admin.site.register(admin)
# admin.site.register(User)
