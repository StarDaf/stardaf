import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.humanize.templatetags.humanize import naturaltime

from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('connected', event)
        
        me = self.scope['user']
        other_user = self.scope['url_route']['kwargs']['username']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = f'thread_{thread_obj.id}'  # chat room name
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
       

        await self.send({
            'type':'websocket.accept'
        })

       

    async def websocket_receive(self, event):

        print('receive', event)  

        sent_text = event.get('text', None)
        if sent_text is not None:
            loaded_msg = json.loads(sent_text)
            msg = loaded_msg['message']
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
                
            
            chat = await self.create_chat_message(user, msg)
            timestamp = str(naturaltime(chat.timestamp))
            
            response = {
                'message' : msg,
                'username':username,
                'timestamp':timestamp
            }

            # broadcast the message
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type':'chat_message',
                    'text':json.dumps(response)
                }

            )

    async def chat_message(self, event):

        # sends the message
        await self.send({
            'type':'websocket.send',
            'text':event['text']
        })

          
                

    async def websocket_disconnect(self, event):
        print('disconnect', event)     

    @database_sync_to_async
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user, other_user)[0]

    @database_sync_to_async
    def create_chat_message(self, user, message):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=user, message=message)


    



    
    
        
        

    