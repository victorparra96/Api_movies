# Python
from datetime import datetime

# Django
from django.contrib.sessions.models import Session

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Serializers
from users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, UserTokenSerializer

# Authentication
from users.authentication_mixins import Authentication

# Models
from users.models import User

class UserToken(Authentication, APIView):
    """
    Validate Token
    """
    def get(self, request, *args, **kwargs):        
        try:
            user_token = Token.objects.get(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                'token': user_token.key,
                'user': user.data
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas.'
            },status = status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido, en nuestro caso solo vamos a permitir post
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if self.context['user'].id == int(session_data.get('_auth_user_id')):
                    session.delete()
        request.user.auth_token.delete()
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)