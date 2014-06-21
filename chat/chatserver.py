# -*- coding: utf-8 -*-

'''
Here is basic explanation:
http://ferretfarmer.net/2013/09/05/tutorial-real-time-chat-with-django-twisted-and-websockets-part-2/

Installation:
#checkout the twisted project
git clone https://github.com/twisted/twisted.git twisted-websocket

#switch to the most up to date websocket branch
cd twisted-websocket
git fetch
git checkout websocket-4173-4

#install it - preferably do this in a virtualenv
python setup.py install



#after install twistd -n -y chatserver.py
'''
import os
from random import randint
import sys
os.getcwd()
path = os.path.join(os.getcwd(), '..')
# Add path to run django app this action has
# to be done before import django libs
if path not in sys.path:
    sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kitty.settings")
import json
import datetime
from twisted.internet.protocol import connectionDone
from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, lookupProtocolForFactory
from collections import deque
from django.contrib.sessions.models import Session
from django.contrib.auth import models
from cgi import escape
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.application import service, internet
from twisted.internet.protocol import Factory


class MyChat(basic.LineReceiver):
    '''Class controls messages propagation via Messenger class helper.
    Data can be send to all users or single user. User is identified by his
    username, each username should be unique. Class can receive and send
    message from / to specific user in real time.
    Chat data (messages) is stored inside Chat factory'''

    factory = None

    def connectionMade(self):
        '''On connection we give username for connected client.
        Creator for unique username is inside User class,
        after that welcome message is sended to connected
        client and lasted chat messages
        '''
        self.username = User().get_unique_name(self.factory.clients,
                                               random=True)
        self.factory.clients.append(self)
        messenger = Messenger()
        #send welcome message
        messenger.connected_message(self)
        #show stored discussion in the factory class
        iterator = 0
        for message in self.factory.messages:
            messenger.message(self, self.factory.authors[iterator],
                              message, self.factory.time[iterator])
            iterator += 1
        #send all available users to connected clients
        messenger.send_users(self.factory.clients)

    def connectionLost(self, reason=connectionDone):
        '''When client is disconnected just send information about
        this user to other connected clients and then
        remove client from factory'''
        print 'Lost client!'
        Messenger().send_lost_user(self.factory.clients, self)
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        '''Receiving data from clients and decide what action have to be done,
        messenger object has the delegator role.
        The object do delegated actions on passed data to his methods'''
        messenger = Messenger()
        #if data is not json send it to client as message
        try:
            data = json.loads(data)
        except ValueError:
            pass
        print data
        #if json has 'key' this means to look for the user in django's ORM
        if 'key' in data:
            username = self.username
            #if session key is invalid or user cant be found
            # don't change the name
            try:
                self.username = User.get_user_by_session(data['key'])
                #tell about changed username to all connected clients,
                # append new and the old username
                messenger.changed_username(self.factory.clients,
                                           self.username, username)
            except Exception:
                print 'Can\'t find user by session, "key": ', data['key']
        elif 'receiver' in data:
            messenger.private_message(self.factory.clients, data['receiver'],
                                      self.username, data['prvMsg'])
        else:
            print 'received', repr(data)
            self.factory.messages.append(data)
            self.factory.authors.append(self)
            self.factory.time.append(messenger.get_time())
            #propagate the message to all
            messenger.to_all(self.factory.clients, self, data)

    def message(self, message):
        '''Transport from client to another should be done via this method'''
        self.transport.write(message + '\n')
    def message_utf8(self, message):
        '''Use it from server site when message is utf8.
        For example server has to send some message with utf-8
        characters, this message should be passed by this method'''
        self.message(message.encode('utf8'))


class ChatFactory(Factory):
    '''Factory - container for stored data, lastest
    messages are stored with limited size container.'''

    protocol = MyChat
    clients = []
    messages = deque(maxlen=20)
    authors = deque(maxlen=20)
    time = deque(maxlen=20)

class Messenger(object):
    '''This class helps to do the action on clients.
    Class contains method for standard output data. Data usually
    formated by JSON '''

    def __init__(self):
        super(Messenger, self).__init__()

    @staticmethod
    def get_time():
        '''Every message has time with the same format'''
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def message(receiver, sender, message, time):
        '''Standard formatted message, empty text is ommited,
        HTML tags are escaped.'''
        if message:
            pack = json.dumps({
                'msg': escape(message),
                'time': time,
                'sender': sender.username,
                'receiver': receiver.username
            })
            receiver.message(pack)

    @staticmethod
    def propagate(clients, message):
        '''Send string message to given clients list'''
        for client in clients:
            client.message(message)

    @staticmethod
    def connected_message(user):
        '''Connection message to user'''
        user.message(json.dumps({
            'connection_status': True,
            'you': user.username
        }))

    @staticmethod
    def find_user_by_name(clients, username):
        '''Find username in clients list, if username
        not exists method return none'''
        for client in clients:
            if client.username == username:
                return client
        return None

    def to_all(self, clients, sender, message, time=None):
        '''Message sends to all clients list passed to the method'''
        if not time:
            time = self.get_time()
        for client in clients:
            self.message(client, sender, message, time)

    def send_users(self, clients, users=None):
        '''Sends username to given clients list,
        if users is none method sends list of clients to each client'''
        if not users:
            users = clients
        all_clients = json.dumps({
            'all_clients': [user.username for user in users]
        })
        self.propagate(clients, all_clients)

    def send_lost_user(self, clients, user):
        '''Send information about disconnected client. Data is JSON formatted'''
        self.propagate(clients, json.dumps({'client_lost': user.username}))

    def changed_username(self, clients, new_username, old_username):
        '''Send information about username changed to given clients list.
        Data in JSON contains information about
        new and name before change'''
        self.propagate(clients, json.dumps({
            'username_changed': {
                'new': new_username, 'old': old_username
            }
        }))

    def private_message(self, clients, receiver, sender, msg):
        '''Send private message to receiver and sender username
        (sending for sender can be useful for delivery).
        Message can not be send if client close the connection'''
        pack = json.dumps({
            'prvMsg': escape(msg),
            'time': self.get_time(),
            'sender': sender,
            'receiver': receiver
        })
        receiver_user = self.find_user_by_name(clients, receiver)
        sender_user = self.find_user_by_name(clients, sender)
        if sender_user:
            sender_user.message(pack)
        if receiver_user:
            receiver_user.message(pack)

class User(object):
    '''Class organize unique usernames or / and read username
    from django logged in username'''

    #base username
    DEFAULT_USERNAME = 'guest'

    def __init__(self):
        super(User, self).__init__()

    @staticmethod
    def is_unique_name(clients, name):
        '''Check username in clients list,
        if unique return True else return False'''
        for client in clients:
            if name == client.username:
                return False
        return True

    @staticmethod
    def get_user_by_session(key):
        '''Reads current logged in user in Django session,
        if such data not found error will be raised'''
        session = Session.objects.get(session_key=key)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        user = models.User.objects.get(id=uid)
        return str(user)


    def get_unique_name(self, clients, random=False):
        '''Methods adds unique number to base username,
        if random is set then starting postfix
        will be random unsigned integer'''
        postfix = 1 if random is False else randint(1, 1000)

        while True:
            #username to try
            name = self.DEFAULT_USERNAME + str(postfix)
            #if username not exists in connected clients return unique username,
            # else increment id and check again
            if self.is_unique_name(clients, name):
                return name
            postfix += 1

if __name__ == '__builtin__':
    #initialize and run websocket
    resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
    root = Resource()

    root.putChild('ws', resource)
    application = service.Application('chatserver')
    #start server on 1025 port
    internet.TCPServer(1025, Site(root)).setServiceParent(application)
