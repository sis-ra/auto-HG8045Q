from auto_HG8045Q.api import Api

client = Api(username='admin', password='helloworld1', host='192.168.1.1')
if client.get_session():
    print('logged in')