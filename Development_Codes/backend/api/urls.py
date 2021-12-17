from django.urls import path
from .views import *

urlpatterns = [
    path('owner/create', OwnerCreate.as_view()),
    path('owner/list', OwnerList.as_view()),
    path('signup', OwnerCreateView.as_view()),
    path('perish/create', PerishableCreate.as_view()),
    path('perish/list', PerishableList.as_view()),
    path('get_user_perish', GetUsersPerishable.as_view()),

    # path('owner/destroy', OwnerDestroy.as_view()),
]

GetUsersPerishable
