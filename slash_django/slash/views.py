import json
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.template.loader import render_to_string
from slash_django.utils.functions import call_chat_gpt
from slash_django.slash.utils import save_queries


# Create your views here.
queries = []


def get_index(request):
    global queries
    length_of_chat = 0
    if queries:
        save_queries(queries)
    queries = []
    csrf = get_token(request)
    level_1, level_2, level_3 = get_levels_data()
    context = {"csrf": csrf, "prompt": None, "query": "Search Your Query", "data": {
        "level_1": level_1, "level_2": level_2, "level_3": level_3}, "chat": [], "length_of_chat": length_of_chat}

    return render(request, 'pages/chat.html', context=context)


def get_json():
    f = open('./slash-django/Slash/slash_django/utils/models.json')
    # f = open('slash_django/utils/models.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    return data


def get_levels_data():
    models = get_json()
    level_1 = [obj for obj in models if obj.get('level') == 1]
    level_2 = [obj for obj in models if obj.get('level') == 2]
    level_3 = [obj for obj in models if obj.get('level') == 3]
    return level_1, level_2, level_3


"""
API triggered when user submit a query in a search box. 
"""


def query(request):
    global queries
    level_1, level_2, level_3 = get_levels_data()
    context = {"prompt": None, "query": "", "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3}}

    if request.method == 'POST':
        prompt = request.POST.get('prompt', None)
        if prompt:
            prompt = prompt.replace('/', '')
            response = call_chat_gpt(prompt)
            queries.append({
                "query": prompt,
                'prompt': response,
            })
            context = {
                "query": prompt,
                'prompt': response,
                "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3},
                "table-data": queries,
            }

    print(queries)
    return JsonResponse(context, status=200)


def conversation(request, convo):
    global queries
    length_of_chat = 0
    chat = []
    if queries:
        save_queries(queries)
    if convo:
        try:
            with open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(convo.lower().replace(' ', '-')), 'r', encoding='utf-8') as fout:
                chat = json.loads(fout.read())
        except OSError as e:
            pass
    csrf = get_token(request)
    level_1, level_2, level_3 = get_levels_data()
    context = {"csrf": csrf, "prompt": None, "query": "Search Your Query", "data": {
        "level_1": level_1, "level_2": level_2, "level_3": level_3}, "chat": chat, "length_of_chat": len(chat) if chat  else length_of_chat}
    queries = chat
    return render(request, 'pages/chat.html', context=context)
