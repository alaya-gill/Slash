import json
from datetime import datetime
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from slash_django.utils.functions import call_chat_gpt, call_dalle
from slash_django.slash.utils import save_queries, is_ajax, fetch_chat, imagine
from django.conf import settings
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
        context = {"csrf": csrf, "prompt": None, "query": "/// Search Your Query", "data": {
            "level_1": level_1, "level_2": level_2, "level_3": level_3}, "chat": [], "length_of_chat": length_of_chat}

        return render(request, 'pages/chat.html', context=context)

    def get_json(self):
        f = open(settings.ROOT_FILE_PATH + '/slash_django/utils/models.json')
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
        time_now = datetime.now
        self.queries = []
        print(self.queries)
        print("query", is_ajax(request))
        level_1, level_2, level_3 = self.get_levels_data()
        context = {"prompt": None, "query": "", "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3}}

        if request.method == 'POST':
            prompt = request.POST.get('prompt', None)
            uuid = request.POST.get('uuid', None)
            if prompt:
                prompt = prompt.replace('/', '')
                dall_e = imagine(prompt)
                if dall_e:
                    response = call_dalle(prompt)
                else:
                    response = call_chat_gpt(prompt)
                self.queries.append({
                    "query": prompt,
                    'prompt': response,
                    'time': time_now().strftime('%H:%M'),
                    "dall_e": dall_e
                })
                context = {
                    "query": prompt,
                    'prompt': response,
                    'time': time_now().strftime('%H:%M'),
                    "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3},
                    "table-data": self.queries,
                    "dall_e": dall_e
                }

                print(self.queries)
                save_queries(uuid, self.queries)

        return JsonResponse(context, status=200)

    def conversation(self, request, convo):
        time_now = datetime.now
        print("conversation", is_ajax(request))
        print("conversation", convo)
        self.queries = []
        length_of_chat = 0
        chat = []
        if convo:
            chat = fetch_chat(convo=convo)
        csrf = get_token(request)
        level_1, level_2, level_3 = self.get_levels_data()
        context = {
            "csrf": csrf, 
            "prompt": None, 
            "query": "/// Search Your Query", "data": {
            "level_1": level_1, "level_2": level_2, "level_3": level_3}, 
            "chat": chat, 
            "time": time_now().strftime('%H:%M'),
            "length_of_chat": len(chat) if chat else length_of_chat
            }
        self.queries = chat
        return render(request, 'pages/chat.html', context=context)

    def get_level_data(self, request, level, id):
        level_1, level_2, level_3 = self.get_levels_data()
        if int(id)==2:
            level_id = [obj['id'] for obj in level_1 if obj['displayText'].lower()==level.lower()][0]
            levels = [level for level in level_2 if level["parentModel"]==level_id]
            return JsonResponse({"levels": levels}, status=200)
        elif int(id)==3:
            level_id = [obj['id'] for obj in level_2 if obj['displayText'].lower()==level.lower()][0]
            levels = [level for level in level_3 if level["parentModel"]==level_id]
            return JsonResponse({"levels": levels}, status=200)
            