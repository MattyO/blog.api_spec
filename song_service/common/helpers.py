import base64
import json

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.core import serializers
import django.core.serializers.json

def resolve_http_method(request, methods):
    '''Thinking this method is pasted a list of methods or the dictonary returned from the python core function locals.  However any dictonary with function objects will do which gives it a nice amount of scoping and configurablity
    '''
    if isinstance(methods, list):
        methods = { a_function.__name__ : a_function for a_function in methods }
    if request.method.lower() not in methods.keys():
        return HttpResponse(status=501)
    return methods[request.method.lower()]()      



def basicauth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode("utf8").split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        request.user = user
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format(
            settings.BASIC_AUTH_REALM
        )
        return response
    return wrap

def jsonify(thing):
    def jsonify_list(model_query):
        return json.loads(serializers.serialize('json', model_query, cls=django.core.serializers.json.DjangoJSONEncoder))

    return { key: jsonify_list(value) for key, value in thing.items() }

