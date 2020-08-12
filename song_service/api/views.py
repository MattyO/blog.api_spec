from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
import common.models
from common.helpers import resolve_http_method, basicauth, jsonify
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@basicauth
def author(request, id):
    author_instance = common.models.Author.objects.get(pk=id)

    def get():
        return JsonResponse(serializers.serialize('json', author_instance))

    return resolve_http_method(request, [get])


@basicauth
def song(request, id):
    song_instance = common.models.Song.objects.get(pk=id)

    def get():
        return JsonResponse(serializers.serialize('json', song_instance))

    return resolve_http_method(request, [get])


@basicauth
def record(request, id):
    record_instance = common.models.Record.objects.get(pk=id)

    def get():
        return JsonResponse(serializers.serialize('json', record_instance))

    return resolve_http_method(request, [get])


@csrf_exempt
@basicauth
def searches(request):

    def post():
        s = common.models.Search(q=request.GET['q'])
        s.user = request.user
        s.save()

        return JsonResponse(jsonify(s.results()))

    def get():
        searches_by_user  = common.models.Search.filter(user = request.user)
        return JsonResponse(jsonify(searches_by_user))

    return resolve_http_method(request, [get, post])

@basicauth
def search(request, id):

    search_instance = common.models.Search.objects.get(pk=id)

    def get(request):
        return JsonResponse(jsonify(search_instance))

    return resolve_http_method(request, [get])
