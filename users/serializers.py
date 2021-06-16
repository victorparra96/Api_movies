# Python
from datetime import datetime

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.sessions.models import Session

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from users.models import User

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )

class UserLoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, max_length=10)

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        if created:
            return self.context['user'], token.key
        else:
            # Si ya tiene sesion abierta, elimina la sesion
            all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if self.context['user'].id == int(session_data.get('_auth_user_id')):
                        session.delete()
            # Elimina el token guardado y crea uno nuevo
            token.delete()
            token = Token.objects.create(user=self.context['user'])
            return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], 
        required=False
    )

    about = serializers.CharField(max_length=1000, required=False)

    city = serializers.CharField(max_length=250, required=False)

    country = serializers.CharField(max_length=250, required=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."
    )
    phone = serializers.CharField(validators=[phone_regex], required=False)

    password = serializers.CharField(min_length=4, max_length=10)
    password_confirmation = serializers.CharField(min_length=4, max_length=10)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

        image = None
        if 'photo' in data:
            image = data['photo']

        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(f"La imagen es demasiado grande, el peso máximo permitido es de 512KB y el tamaño enviado es de {round(image.size / 1024)}KB")

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user