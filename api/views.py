from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

from django.shortcuts import render

# Define a view function for the homepage



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)  # Corrected attribute name
    permission_classes = [AllowAny,]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)  # Corrected attribute name
    permission_classes = [IsAuthenticated]  
    
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure the request contains the 'star' field
        if 'star' in request.data:
            movie = Movie.objects.get(id=pk)
            star = request.data['star']
            user = request.user

            print('Movie title: ', movie.title)
            print('User: ', user)

            try:
                # Check if the user has already rated this movie
                rating = Rating.objects.get(user=user, movie=movie)
                rating.star = star  # Update rating
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Rating.DoesNotExist:
                # If rating doesn't exist, create a new one
                rating = Rating.objects.create(user=user, movie=movie, star=star)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            # Return error if 'star' is not provided in the request data
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)  # Corrected attribute name
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can interact with ratings

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.views import APIView
class MyAPIView(APIView):
    permission_classes = [IsAuthenticated]


