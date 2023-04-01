import json
import re

def save_queries(request, queries):
    filename = queries[0].get('query')
    filename = re.sub(r'\W+', '', filename)
    session_filename = request.session.get('filename', False)
    if not session_filename:
        request.session['filename'] = filename
    print("save_queries", filename)
    fout = open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(filename.lower()), 'w', encoding='utf-8')
    json.dump(queries, fout)
    fout.close()
        
def fetch_chat(convo):
    print("fetch_chat",convo)
    chat = []
    try:
        filename = re.sub(r'\W+', '', convo)
        fout=open('./slash-django/Slash/slash_django/utils/conversations/{}.json'.format(filename.lower()), 'r', encoding='utf-8')
        chat = json.loads(fout.read())
        fout.close()
    except OSError as e:
        pass
    return chat
    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'