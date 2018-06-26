from django.contrib import admin

# Register your models here.
from .models import News,Knowledge,Case,Index,Category,Product

admin.site.register(News)
admin.site.register(Knowledge)
admin.site.register(Case)
admin.site.register(Index)





class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']

	prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Product,ProductAdmin)