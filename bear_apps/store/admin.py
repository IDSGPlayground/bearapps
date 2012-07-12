from store.models import Apps, User
from django.contrib import admin
class AppsInline(admin.TabularInline):
	model=Apps
	extra=3

class UserAdmin(admin.ModelAdmin):
	inlines= [AppsInline]

admin.site.register(User, UserAdmin)
# admin.site.register(User)