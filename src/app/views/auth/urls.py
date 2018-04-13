from django.urls import path
from django.contrib.auth.views import LogoutView
from app.views.auth.claim_account import ClaimAccount
from app.views.auth.login import Login


urlpatterns = [
    path('claim-delegate/<slug:delegate_slug>/', ClaimAccount.as_view(), name='claim-delegate'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout')
]
