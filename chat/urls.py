from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
from chat.api import MessageModelViewset,UserModelViewset

router=DefaultRouter()
router.register('chat',MessageModelViewset,basename='message')
router.register('user',UserModelViewset,basename='users')
urlpatterns = [
    path('talkapi/',include(router.urls)),
     path('home/',views.home,name='home')

 ]