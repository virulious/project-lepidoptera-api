from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.species_views import Species, SpeciesDetail
from .views.genus_views import Genus, GenusDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('species/', Species.as_view(), name='species'),
    path('species/<int:pk>/', SpeciesDetail.as_view(), name='species_detail'),
    path('genus/', Genus.as_view(), name='genus'),
    path('genus/<int:pk>/', GenusDetail.as_view(), name='genus_detail')
]
