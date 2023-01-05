import json
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import action
from accounts.utils import get_and_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout
from ems_event.models import (
    Event, 

)
from .serializers import (
    EmptySerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    AuthUserSerializer,
    UserRegisterSerializer,
    PasswordChangesSerializer,
    EventCategorySerializer,
    EventSerializer,
    EventSpeakerSerializer,
    AttendeeSerializer,
)

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'profile': UserProfileSerializer,
        'register': UserRegisterSerializer,
        'password_change': PasswordChangesSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status.HTTP_204_NO_CONTENT)
    
    @action(methods=['GET', ], detail=False,  permission_classes=[IsAuthenticated, ])
    def profile(self, request):
        query_set = get_user_model().objects.get(email=request.user.email)
        serializer = UserProfileSerializer(query_set, many=False)
        print(request.data)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict mapping')
        
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
        

class EventViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'events': EventSerializer,
        'category': EventCategorySerializer,
        'speaker': EventSpeakerSerializer,
        'attendee': AttendeeSerializer,
    }

    @action(methods=['POST', 'GET' ], detail=False, permission_classes=[IsAuthenticated, ])
    def events(self, request):
        if request.method == 'GET':
            queryset =  Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_CONTENT)
        
    @action(methods=['GET' ], detail=False, url_path='event/(?P<slug>[-\w]+)', permission_classes=[IsAuthenticated, ])
    def event(self, request, slug):
        if request.method == 'GET':
            queryset =  Event.objects.get(slug=slug)
            serializer = EventSerializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_CONTENT)
        
        
    
    @action(methods=['POST',], detail=False, permission_classes=[IsAuthenticated, ])
    def category(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST',], detail=False, permission_classes=[IsAuthenticated, ])
    def speaker(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST',], detail=False, permission_classes=[IsAuthenticated, ])
    def attendee(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict mapping')
        
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
        
