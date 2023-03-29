import json
from django.shortcuts import render
from slash_django.utils.functions import call_chat_gpt


# Create your views here.
queries = []

def get_index(request):
    level_1, level_2, level_3 = get_levels_data()
    context = {"prompt": None, "query": "Search Your Query", "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3} }
    return render(request, 'pages/index.html', context=context)

def get_json():
    f = open('slash_django/utils/models.json')
  
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    return data

def get_levels_data():
   models = get_json()
   level_1 = [obj for obj in models if obj.get('level')==1]
   level_2 = [obj for obj in models if obj.get('level')==2]
   level_3 = [obj for obj in models if obj.get('level')==3] 
   return level_1, level_2, level_3

"""
API triggered when user submit a query in a search box. 
"""
def query(request):
    level_1, level_2, level_3 = get_levels_data()
    context = {"prompt": None, "query": "", "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3} }
    
    if request.method=='POST':
        prompt = request.POST.get('prompt', None)
        if prompt:
            prompt = prompt.replace('/','')
            response = call_chat_gpt(prompt)
            context = {
                "query": prompt,
                'prompt': response,
                "data": {"level_1": level_1, "level_2": level_2, "level_3": level_3} 
                }
                        
    return render(request, 'pages/index.html', context=context)