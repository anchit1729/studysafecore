#tidy up url patterns
#Suits Needs of HKU's COVID Task Force in Trace: /venues/ and /contacts/
from django.urls import path, include
from .api_views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'access-records', all_access_records)
router.register(f'venues', view_all_venues)
router.register(f'members', list_all_members)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/contacts/<str:uid>/<str:date>', view_close_contacts.as_view(), name = 'view_close_contacts'),
    path('api/venues/<str:uid>/<str:date>', view_infected_venues.as_view(), name = 'view_infected_venues'),
]
