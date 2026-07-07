from django.utils import timezone
from datetime import timedelta

import requests
from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from integrations.models import PlatformToken

META_AUTH_URL = "https://www.facebook.com/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
META_GRAPH_API = "https://graph.facebook.com/v23.0"
PLATFORM = "META_ADS"

class MetaConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        state = signing.dumps(request.user.id, salt=settings.META_STATE_SALT)

        url = (
            f"{META_AUTH_URL}"
            f"?client_id={settings.META_APP_ID}"
            f"&redirect_uri={settings.META_REDIRECT_URI}"
            f"&scope=ads_read,ads_management,business_management"
            f"&state={state}"
        )
        return Response({"redirect_url": url})

class MetaCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or not state:
            return redirect(f"{settings.FRONTEND_URL}/integrations?integration=meta_ads&status=error")

        try:
            user_id = signing.loads(state, salt=settings.META_STATE_SALT, max_age=settings.META_STATE_MAX_AGE)
        except (BadSignature, SignatureExpired):
            return redirect(f"{settings.FRONTEND_URL}/integrations?integration=meta_ads&status=error")

        response = requests.get(META_TOKEN_URL, params={
            "client_id": settings.META_APP_ID,
            "client_secret": settings.META_APP_SECRET,
            "redirect_uri": settings.META_REDIRECT_URI,
            "code": code,
        })
        data = response.json()

        if "access_token" not in data:
            return redirect(f"{settings.FRONTEND_URL}/integrations?integration=meta_ads&status=error")

        PlatformToken.objects.update_or_create(
            agency_id=user_id,
            platform=PLATFORM,
            defaults={
                "access_token": data["access_token"],
                "expires_at": timezone.now() + timedelta(seconds=data["expires_in"]),
            },
        )

        return redirect(f"{settings.FRONTEND_URL}/integrations?integration=meta_ads&status=success")
    
class MetaCustomersListAllView(APIView):
    permission_classes = [IsAuthenticated]
    META_API_URL = f"{META_GRAPH_API}/me/adaccounts"

    def get(self, request):
        meta_account = PlatformToken.objects.filter(
            agency=request.user,
            platform=PLATFORM,
        ).first()

        if not meta_account:
            return Response(
                {"detail": "No Meta Ads account connected."},
                status=404,
            )

        response = requests.get(
            self.META_API_URL,
            params={
                "access_token": meta_account.access_token,
                "fields": "id,name,account_id,account_status,currency,timezone_name",
            },
        )

        return Response(response.json(), status=response.status_code)