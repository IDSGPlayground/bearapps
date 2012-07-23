from store.models import User_Apps, User, App, Group, Chartstring
from django.contrib import admin

class AppsInline(admin.TabularInline):
	model = User_Apps

class ChartstringInline(admin.TabularInline):
	model = Chartstring

class UserAdmin(admin.ModelAdmin):
	inlines = [AppsInline]

admin.site.register(User, UserAdmin)
admin.site.register(App)
admin.site.register(Group)
admin.site.register(Chartstring)
admin.site.register(admin)
# admin.site.register(User)