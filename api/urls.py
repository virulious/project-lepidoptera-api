from django.urls import path
from .views.species_views import SpeciesView, SpeciesDetail
from .views.genus_views import GenusView, GenusDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
	# Restful routing
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('species/', SpeciesView.as_view(), name='species'),
    path('species/<int:pk>/', SpeciesDetail.as_view(), name='species_detail'),
    path('genus/', GenusView.as_view(), name='genus'),
    path('genus/<int:pk>/', GenusDetail.as_view(), name='genus_detail')
]
