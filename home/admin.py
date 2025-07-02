from django.contrib import admin
from users.models import UserProfile
# Register your models here.
admin.site.site_header = 'إدارة موقع Prodamin'
admin.site.site_title = 'Prodamin Admin'    
admin.site.index_title = 'لوحة تحكم إدارة موقع Prodamin'
admin.site.register(
    # add the users profile
    UserProfile,
)