from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class MessageModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recipientu')
    timestamp = models.DateTimeField( auto_now_add=True)
    content = models.TextField()

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.content = self.content.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()


    #def last_10_messages(self):
       #return Message.objects.order_by('-timestamp').all()[:10]

class UserProfile(models.Model):
    userprofile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')
    image = models.ImageField(default='default.png', blank=True)
    aboutyou = models.TextField()