from django.urls import path, re_path
from knox import views as knox_views

from app.views.api.auth import ClaimDelegate, LoginView
from app.views.api.contributions import Contributions
from app.views.api.delegates import Delegates
from app.views.api.news import News


urlpatterns = [
    path("delegates/", Delegates.as_view(), name="api-delegates"),
    re_path(
        r"delegates/(?P<wallet_address>[0-9A-Za-z]{34})/$",
        Delegates.as_view(),
        name="api-delegate-a",
    ),
    path("delegates/<slug:delegate_slug>/", Delegates.as_view(), name="api-delegate-b"),
    # contributions
    path(
        "contributions/<str:contribution_id>/", Contributions.as_view(), name="api-contributions-id"
    ),
    path(
        "contributions/<slug:delegate_slug>/",
        Contributions.as_view(),
        name="api-contributions-slug",
    ),
    path("contributions/", Contributions.as_view(), name="api-contributions"),  # old
    # nnews
    path("news/<str:news_id>/", News.as_view(), name="api-news-id"),
    path("news/<slug:delegate_slug>/", News.as_view(), name="api-news-slug"),
    path("news/", News.as_view(), name="api-news"),  # old
    # auth
    path("auth/login/", LoginView.as_view(), name="api-auth-login"),
    path("auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("auth/logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path(
        "auth/claim-delegate/<slug:delegate_slug>/",
        ClaimDelegate.as_view(),
        name="api-claim-delegate",
    ),
]
