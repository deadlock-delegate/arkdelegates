"""a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from app.views.delegate import DelegateView
from app.views.edit import EditContributionView, EditNodeView, EditProposalView, StatusUpdateView
from app.views.faq import FAQ
from app.views.home import Homepage, health
from app.views.how_to_get_listed import HowToGetListed
from app.views.update import UpdateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    # pages
    path("", Homepage.as_view(), name="homepage"),
    path("delegate/<slug:delegate_slug>/", DelegateView.as_view(), name="delegate"),
    path(
        "delegate/<slug:delegate_slug>/update/<int:update_id>", UpdateView.as_view(), name="update"
    ),
    # static pages
    path("faq/", FAQ.as_view(), name="faq"),
    path("how-to-get-listed/", HowToGetListed.as_view(), name="how_to_get_listed"),
    # auth
    path("auth/", include("app.views.auth.urls")),
    # edit
    path("edit/proposal/", EditProposalView.as_view(), name="proposal"),
    path("edit/contribution/", EditContributionView.as_view(), name="contribution"),
    path("edit/node/", EditNodeView.as_view(), name="node"),
    path("edit/update/", StatusUpdateView.as_view(), name="status"),
    # api
    path("api/", include("app.views.api.urls")),
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
