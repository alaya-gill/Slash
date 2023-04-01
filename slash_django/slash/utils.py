import json
import re

def save_queries(uuid, queries):
    # filename = queries[0].get('query')
    # filename = re.sub(r'\W+', '', filename)
    print("save_queries", uuid)
    with open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(uuid), 'r+', encoding='utf-8') as fout:
        file_data =  json.load(fout)
        file_data.append(queries)
        fout.seek(0)
        json.dump(file_data, fout, indent=4)
    # json.dump(queries, fout)
    # fout.close()
        
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