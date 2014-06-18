#http://ferretfarmer.net/2013/09/05/tutorial-real-time-chat-with-django-twisted-and-websockets-part-2/
'''
#checkout the twisted project
git clone https://github.com/twisted/twisted.git twisted-websocket

#switch to the most up to date websocket branch
cd twisted-websocket
git fetch
git checkout websocket-4173-4

#install it - preferably do this in a virtualenv
python setup.py install
'''
from twisted.internet.protocol import connectionDone
from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory


class MyChat(basic.LineReceiver):
    def connectionMade(self):
        print 'got new client'
        self.transport.write('connected... \n')
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        print 'Lost client!'
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        print 'received', repr(data)
        for c in self.factory.clients:
            c.message(data)

    def message(self, message):
        self.transport.write(message + '\n')

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

from twisted.internet.protocol import Factory

class ChatFactory(Factory):
    protocol = MyChat
    clients = []

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()

root.put('ws', resource)
application = service.Application('chatserver')
internet.TCPServer(1025, Site(root)).setServiceParent(application)