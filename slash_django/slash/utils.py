import json
import re

def save_queries(queries):
    filename = queries[0].get('query')
    filename = re.sub(r'\W+', '', filename)
    with open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(filename.lower()), 'w', encoding='utf-8') as fout:
        json.dump(queries, fout)
        
def fetch_chat(convo):
    chat = []
    try:
        filename = re.sub(r'\W+', '', convo)
        with open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(filename.lower()), 'r', encoding='utf-8') as fout:
            chat = json.loads(fout.read())
    except OSError as e:
        pass
    return chat
    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'