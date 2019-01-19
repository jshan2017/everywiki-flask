from flask import Flask, request
import json, os, requests, uuid, sqlite3, datetime, time
from google.cloud import translate
app = Flask(__name__)
#db initialization



@app.route('/')
def hello_world():
    return 'Helllll World!'
@app.route('/documents/<string:title>/<string:lang>', methods=['GET'])
def get_document(title, lang):
    print('you are trying to get : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT article FROM wiki WHERE title = ? ORDER BY time DESC LIMIT 1"
    cur.execute(sql, (title,))
    rows = cur.fetchall()
    articleArray=None
    for row in rows:
        articleArray=json.loads(row[0])
    print(articleArray)
    for i in range(len(articleArray)):
        if articleArray[i]['lang']==lang:
            articleArray[i] = articleArray[i]['text']
        else :
            articleArray[i] = gTranslate(articleArray[i]['text'], lang)
    #print(articleArray)
    result = ' '.join(articleArray)
    print(result)
    conn.close()
    return result
@app.route('/documents/<string:title>', methods=['POST'])
def post_document(title):
    print('you are trying to post : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "INSERT INTO wiki VALUES (?,?, ?)"
    now = int(time.time())
    article = str(request.get_json()['article'])
    print('article: '+article)
    cur.execute(sql, (title, now, article))
    conn.commit()
    conn.close()
    return 'success posting'

def gTranslate(inText, lang):
    text =u'{}'.format(inText)
    translate_client = translate.Client()
    target = lang
    translation = translate_client.translate(
        text,
        target_language=target)
    return u'{}'.format(translation['translatedText'])

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=80)

