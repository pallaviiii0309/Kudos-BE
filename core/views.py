from datetime import datetime, timezone
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Kudo, year_week
from .serializers import UserSimpleSerializer, KudoSerializer, MeSerializer

WEEKLY_ALLOWANCE = 3

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSimpleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # peers in same org, exclude self + admins
        return (
            User.objects.filter(organization=self.request.user.organization)
            .exclude(id=self.request.user.id)
            .exclude(is_staff=True)
            .exclude(is_superuser=True)
            .exclude(username__iexact="admin")
        )

class KudoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = KudoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        qs = Kudo.objects.filter(Q(from_user=u) | Q(to_user=u)).select_related("from_user", "to_user")
        box = self.request.query_params.get("box")
        if box == "received":
            qs = qs.filter(to_user=u)
        elif box == "given":
            
            qs = (
                qs.filter(from_user=u)
                .exclude(to_user__is_staff=True)
                .exclude(to_user__is_superuser=True)
                .exclude(to_user__username__iexact="admin")
            )
        return qs

    def create(self, request, *args, **kwargs):
        
        now = datetime.now(timezone.utc)
        y, w = year_week(now)
        used = Kudo.objects.filter(from_user=request.user, year=y, week=w).count()
        if used >= WEEKLY_ALLOWANCE:
            return Response({"detail": "Weekly limit reached (3)."}, status=status.HTTP_400_BAD_REQUEST)

        ser = self.get_serializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        self.perform_create(ser)
        return Response(ser.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials"}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "user": MeSerializer(user).data,
        "remaining": remaining_kudos(user)
    })

@api_view(["GET"])
def me(request):
    return Response({
        "user": MeSerializer(request.user).data,
        "remaining": remaining_kudos(request.user)
    })

def remaining_kudos(user):
    y, w = year_week()
    used = Kudo.objects.filter(from_user=user, year=y, week=w).count()
    return max(0, WEEKLY_ALLOWANCE - used)
