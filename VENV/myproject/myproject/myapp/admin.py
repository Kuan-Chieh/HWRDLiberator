from django.contrib import admin
from myproject.myapp.models import *
admin.site.register(Document)
admin.site.register(Session)
admin.site.register(Element)
admin.site.register(Property)
admin.site.register(BOM)
admin.site.register(Substitute)
# Register your models here.
