from django.urls import path
# from .views.mango_views import Mangos, MangoDetail
from .views.activity_views import Activities, ActivityDetail
# from .views.parent_views import Parents, ParentDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    # path('mangos/', Mangos.as_view(), name='mangos'),
    # path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    #
    # path('parents', Parents.as_view(), name='parents'),
    # path('parents/<int:pk>', ParentDetail.as_view(), name='parent_detail'),
    path('activities/', Activities.as_view(), name='activities'),
    path('activities/<int:pk>/', ActivityDetail.as_view(), name='activity_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
