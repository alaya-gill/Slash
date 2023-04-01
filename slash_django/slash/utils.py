import json, os
import re

def save_queries(uuid, queries):
    # filename = queries[0].get('query')
    # filename = re.sub(r'\W+', '', filename)
    print("save_queries", uuid)
    file_exists = os.path.exists('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(uuid))
    if not file_exists:
        f = open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(uuid), 'w', encoding='utf-8')
        json.dump(queries, f)
    else:
        fout = open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(uuid), 'r+', encoding='utf-8')
        fout.seek(0)
        file_data =  fout
        json_data = json.load(file_data)
        
        json_data += queries
        fout.seek(0)
        json.dump(json_data, fout, indent=4)
        
def fetch_chat(convo):
    print("fetch_chat",convo)
    chat = []
    try:
        fout=open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(convo), 'r', encoding='utf-8')
        chat = json.loads(fout.read())
        fout.close()
    except OSError as e:
        pass
    return chat
    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'