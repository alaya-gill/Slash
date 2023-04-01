import json
import re

def save_queries(uuid, queries):
    # filename = queries[0].get('query')
    # filename = re.sub(r'\W+', '', filename)
    print("save_queries", uuid)
    try:
        with open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(uuid), 'w+', encoding='utf-8') as fout:
            fout.seek(0)
            file_data =  fout.read()
            if len(file_data)==0 or file_data is None:
                with open('./slash_django/utils/conversations/{}.json'.format(uuid), 'w', encoding='utf-8') as fout:
                    json.dump(queries, fout)
            else:
                json_data = json.load(file_data)
            
                json_data += queries
                fout.seek(0)
                json.dump(json_data, fout, indent=4)
    except FileNotFoundError as e:
        with open('./slash_django/utils/conversations/{}.json'.format(uuid), 'w', encoding='utf-8') as fout:
            json.dump(queries, fout)
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