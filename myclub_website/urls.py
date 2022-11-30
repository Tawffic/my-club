
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),

]

#configure admin
admin.site.site_header ="My Club Administration Page"
admin.site.site_title ="Browser Title"
admin.site.index_title ="Welcome to the admin area"