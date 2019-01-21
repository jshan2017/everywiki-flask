from flask import Flask, request, jsonify, Response
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
        print(row[0])
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
    return jsonify({"result":result})

@app.route('/documents/<string:title>/versions', methods=['GET'])
def get_all_version(title):
    print('get every versions of : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT time FROM wiki WHERE title = ?"
    cur.execute(sql, (title,))
    rows = cur.fetchall()
    versions=[]
    for row in rows:
        versions.append(row[0])
    return Response(json.dumps(versions),  mimetype='application/json')

@app.route('/documents/<string:title>/versions/<int:version>', methods=['GET'])
def get_raw_version(title, version):
    print('get'+str(version)+ 'th versions of : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT article FROM wiki WHERE title = ? AND time = ?"
    cur.execute(sql, (title,version,))
    rows = cur.fetchall()
    result=rows[0][0]
    print(result)
    return jsonify({"result":result})
@app.route('/documents/<string:title>/versions/<int:version>/<string:lang>', methods=['GET'])
def get_rendered_version(title, version, lang):
    print('you are trying to get : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT article FROM wiki WHERE title = ? AND time = ?"
    cur.execute(sql, (title,version,))
    rows = cur.fetchall()
    articleArray=None
    for row in rows:
        print(row[0])
        articleArray=json.loads(row[0])
    print(articleArray)
    for i in range(len(articleArray)):
        if articleArray[i]['lang']==lang:
            articleArray[i] = articleArray[i]['text']
        else :
            articleArray[i] = gTranslate(articleArray[i]['text'], lang)
    result = ' '.join(articleArray)
    print(result)
    conn.close()
    return jsonify({"result":result})
@app.route('/documents/<string:title>', methods=['POST'])
def post_document(title):
    print('you are trying to post : '+ title)
    article=str(request.get_json()['article'])
    article=article.replace("'",'"')
    print(article)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "INSERT INTO wiki VALUES (?,?, ?)"
    now = int(time.time())
    cur.execute(sql, (title, now, article))
    conn.commit()
    conn.close()
    return 'success posting'

def gTranslate(inText, lang):
    text =u'{}'.format(inText)
    translate_client = translate.Client().from_service_account_json('gcpkey.json')
    target = lang
    translation = translate_client.translate(
        text,
        target_language=target)
    return u'{}'.format(translation['translatedText'])

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=80)

