from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from chat.Serializers import MessageModelSerializer, UserModelSerializer, UserProfileSerializer
from chat.models import MessageModel,UserProfile
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
class MessageModelViewset(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def list(self, request, *args, **kwargs):
        recipientName = self.request.query_params.get('recipientName', None)
        if recipientName is not None:
            self.queryset = self.queryset.filter(
                Q(recipient__username=request.user.username, user__username=recipientName) |
                Q(recipient__username=recipientName, user__username=request.user.username))
        serializer=MessageModelSerializer(self.queryset,many=True)
        return Response(serializer.data)





class UserModelViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    def list(self,request,*args,**kwargs):
        self.queryset=self.queryset.exclude(username=self.request.user.username)
        serializer = UserModelSerializer(self.queryset, many=True)
        return Response(serializer.data)
class UserProfileViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(userprofile=self.request.user)
        serializer = UserModelSerializer(self.queryset)
        return Response(serializer.data)


