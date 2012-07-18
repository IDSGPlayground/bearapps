from store.models import User_Apps, User, App
from django.contrib import admin
class AppsInline(admin.TabularInline):
	model = User_Apps
	extra = 3

class UserAdmin(admin.ModelAdmin):
	inlines= [AppsInline]

admin.site.register(User, UserAdmin)
admin.site.register(App)
# admin.site.register(User)