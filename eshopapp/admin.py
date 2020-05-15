from django.contrib import admin

# Register your models here.
from eshopapp import models

admin.site.register(models.Product)
admin.site.register(models.User)
admin.site.register(models.ProdectDetail)
admin.site.register(models.Orders)