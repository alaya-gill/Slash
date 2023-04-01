import json
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from slash_django.utils.functions import call_chat_gpt
from slash_django.slash.utils import save_queries, is_ajax, fetch_chat

# Create your views here.


class Slash:
    def __init__(self) -> None:
        self.queries = []
        
    def get_index(self, request):
        print("index", is_ajax(request))
        length_of_chat = 0
        self.queries = []
        csrf = get_token(request)
        level_1, level_2, level_3 = self.get_levels_data()
        context = {"csrf": csrf, "prompt": None, "query": "Search Your Query", "data": {
            "level_1": level_1, "level_2": level_2, "level_3": level_3}, "chat": [], "length_of_chat": length_of_chat}

        return render(request, 'pages/chat.html', context=context)


    def get_json(self):
        f = open('./slash-django/Slash/slash_django/utils/models.json')
        # f = open('slash_django/utils/models.json')
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        return data


    def get_levels_data(self):
        models = self.get_json()
        level_1 = [obj for obj in models if obj.get('level') == 1]
        level_2 = [obj for obj in models if obj.get('level') == 2]
        level_3 = [obj for obj in models if obj.get('level') == 3]
        return level_1, level_2, level_3


    """
    API triggered when user submit a query in a search box. 
    """


    def query(self, request):
        print("query", is_ajax(request))
        level_1, level_2, level_3 = self.get_levels_data()
        context = {"prompt": None, "query": "", "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3}}

        if request.method == 'POST':
            prompt = request.POST.get('prompt', None)
            if prompt:
                prompt = prompt.replace('/', '')
                response = call_chat_gpt(prompt)
                self.queries.append({
                    "query": prompt,
                    'prompt': response,
                })
                context = {
                    "query": prompt,
                    'prompt': response,
                    "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3},
                    "table-data": self.queries,
                }
                save_queries(self.queries)

        return JsonResponse(context, status=200)


    def conversation(self, request, convo):
        print("conversation", is_ajax(request))
        print("conversation",convo)
        self.queries = []
        length_of_chat = 0
        chat = []
        if convo:
            chat = fetch_chat(convo=convo)
        csrf = get_token(request)
        level_1, level_2, level_3 = self.get_levels_data()
        context = {"csrf": csrf, "prompt": None, "query": "Search Your Query", "data": {
            "level_1": level_1, "level_2": level_2, "level_3": level_3}, "chat": chat, "length_of_chat": len(chat) if chat  else length_of_chat}
        self.queries = chat
        return render(request, 'pages/chat.html', context=context)
