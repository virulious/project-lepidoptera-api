from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.genus import Genus
from ..serializers import SpeciesSerializer, UserSerializer, GenusSerializer

#Create views
class GenusView(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request):
      """Index request"""
      genus = Genus.objects.all()
      # genus = Genus.objects.filter(owner=request.user.id)
      data = GenusSerializer(genus, many=True).data
      return Response(data)

  serializer_class = GenusSerializer
  def post(self, request):
      """Create request"""
      # Add user to request object
      # request.data['genus']['owner'] = request.user.id
      # Serialize/create genus
      genus = GenusSerializer(data=request.data['genus'])
      if genus.is_valid():
          m = genus.save()
          return Response(genus.data, status=status.HTTP_201_CREATED)
      else:
          return Response(genus.errors, status=status.HTTP_400_BAD_REQUEST)

class GenusDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        genus = get_object_or_404(Genus, pk=pk)
        data = genus.species_set.all()
        # Only want to show owned Genus?
        # if not request.user.id == data['owner']:
        # raise PermissionDenied('Unauthorized, you do not own this genus')
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        genus = get_object_or_404(Genus, pk=pk)
        if not request.user.id == genus['owner']:
            raise PermissionDenied('Unauthorized, you do not own this genus')
        genus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['genus'].get('owner', False):
            del request.data['genus']['owner']

        # Locate Genus
        genus = get_object_or_404(Genus, pk=pk)
        # Check if user is  the same
        if not request.user.id == genus['owner']:
            raise PermissionDenied('Unauthorized, you do not own this genus')

        # Add owner to data object now that we know this user owns the resource
        request.data['genus']['owner'] = request.user.id
        # Validate updates with serializer
        ms = GenusSerializer(genus, data=request.data['genus'])
        if ms.is_valid():
            ms.save()
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
