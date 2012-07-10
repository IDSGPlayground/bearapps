from store.models import Apps, User
from django.contrib import admin
class UserInline(admin.TabularInline):
	model=User
	extra=3

class AppsAdmin(admin.ModelAdmin):
	inlines= [UserInline]

admin.site.register(Apps, AppsAdmin)
# admin.site.register(User)