from django.contrib import admin
from account.models import Account, item_request, category, subcategory, item_available
admin.site.register(Account)
admin.site.register(item_request)
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(item_available)
# Register your models here.
