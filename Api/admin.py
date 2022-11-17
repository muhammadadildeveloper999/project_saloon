from django.contrib import admin

# Register your models here.

from Api.models import*

admin.site.register(Role)
admin.site.register(register)
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(package)
admin.site.register(country)
admin.site.register(city)
admin.site.register(saloon)
admin.site.register(employee)
admin.site.register(facility)
admin.site.register(appointment)
admin.site.register(whitelistToken)