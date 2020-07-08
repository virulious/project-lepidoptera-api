from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.species import Species
from ..serializers import SpeciesSerializer, UserSerializer

#Create views
class SpeciesView(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request):
      """Index request"""
      # species = Species.objects.all()
      species = Species.objects.filter(owner=request.user.id)
      data = SpeciesSerializer(species, many=True).data
      return Response(data)

  serializer_class = SpeciesSerializer
  def post(self, request):
      """Create request"""
      # Add user to request object
      request.data['species']['owner'] = request.user.id
      # Serialize/create species
      species = SpeciesSerializer(data=request.data['species'])
      if species.is_valid():
          m = species.save()
          return Response(species.data, status=status.HTTP_201_CREATED)
      else:
          return Response(species.errors, status=status.HTTP_400_BAD_REQUEST)

class SpeciesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        species = get_object_or_404(Species, pk=pk)
        data = SpeciesSerializer(species).data
        # Only want to show owned Genus?
        # if not request.user.id == data['owner']:
        # raise PermissionDenied('Unauthorized, you do not own this species')
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        species = get_object_or_404(Species, pk=pk)
        print(request.user)
        print(species)
        if not request.user == species['owner']:
            raise PermissionDenied('Unauthorized, you do not own this species')
        species.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['species'].get('owner', False):
            del request.data['species']['owner']

        # Locate Species
        species = get_object_or_404(Species, pk=pk)
        # Check if user is  the same
        if not request.user.id == species['owner']:
            raise PermissionDenied('Unauthorized, you do not own this species')

        # Add owner to data object now that we know this user owns the resource
        request.data['species']['owner'] = request.user.id
        # Validate updates with serializer
        ms = SpeciesSerializer(species, data=request.data['species'])
        if ms.is_valid():
            ms.save()
            print(ms)
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
