from django.urls import path

from app.views.api.delegates import Delegates


urlpatterns = [
    path('delegates/', Delegates.as_view(), name='api-delegates'),
    path('delegates/<slug:delegate_slug>/', Delegates.as_view(), name='api-delegate'),
]
