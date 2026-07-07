from django.urls import path

from integrations.views.meta_ads import (
    MetaCustomersListAllView, 
    MetaConnectView, 
    MetaCallbackView
)
from integrations.views.platform_account import PlatformAccountCreateView
from integrations.views.platform_token import (
    ConnectedIntegrationsView, 
    DisconnectIntegrationView
)

urlpatterns = [
    # PlatformToken urls
    path("all/",  ConnectedIntegrationsView.as_view()),
    path("disconnect/<int:pk>/", DisconnectIntegrationView.as_view()),

    # PlatformAccount urls
    path("platform-accounts/",  PlatformAccountCreateView.as_view()),

    # meta urls
    path("meta/connect/",  MetaConnectView.as_view()),
    path("meta/callback/", MetaCallbackView.as_view()),
    path("meta/customers/all/", MetaCustomersListAllView.as_view()),
    
]