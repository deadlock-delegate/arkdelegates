from django.urls import path, re_path

from app.views.api.delegates import Delegates


urlpatterns = [
    path("delegates/", Delegates.as_view(), name="api-delegates"),
    re_path(
        r"delegates/(?P<wallet_address>[0-9A-Za-z]{34})/$", Delegates.as_view(), name="api-delegate"
    ),
    path("delegates/<slug:delegate_slug>/", Delegates.as_view(), name="api-delegate"),
]
