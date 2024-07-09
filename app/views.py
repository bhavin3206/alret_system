from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.exceptions import *
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, SymbolSerializer, SubscriptionSerializer, DeviceTokenSerializer
from .models import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # No permissions required for registration

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [] 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SymbolListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve query parameters from the request
        name_query = request.GET.get('name', None)
        symbol_query = request.GET.get('symbol', None)
        token_query = request.GET.get('token', None)
        exch_seg_query = request.GET.get('exch_seg', None)

        # Construct a cache key based on the query parameters
        cache_key = f'symbol_data_{name_query}_{symbol_query}_{token_query}_{exch_seg_query}'
        cached_symbols = cache.get(cache_key)

        if not cached_symbols:
            # Start with all symbols
            queryset = SymbolData.objects.all()

            # Apply filters based on query parameters
            if name_query:
                queryset = queryset.filter(name__icontains=name_query)
            if symbol_query:
                queryset = queryset.filter(symbol__icontains=symbol_query)
            if token_query:
                queryset = queryset.filter(token=token_query)
            if exch_seg_query:
                queryset = queryset.filter(exch_seg__icontains=exch_seg_query)

            # Check if queryset is empty
            if not queryset.exists():
                return Response({'detail': 'Data not available'}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the filtered symbols
            serializer = SymbolSerializer(queryset, many=True)
            cached_symbols = serializer.data

            # Cache the serialized data for 15 minutes
            cache.set(cache_key, cached_symbols, timeout=60*15)

        return Response(cached_symbols, status=status.HTTP_200_OK)



class SubscriptionListView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Subscription successfully created"},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class DeviceTokenView(generics.ListCreateAPIView):
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeviceToken.objects.filter(user=self.request.user)
