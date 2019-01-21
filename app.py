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
    #getting content
    sql = "SELECT * FROM wiki WHERE title LIKE ? ORDER BY time DESC LIMIT 1"
    cur.execute(sql, ('%'+title+'%',))
    rows = cur.fetchall()
    articleArray=None
    langTitle=None
    for row in rows:

        articleArray=json.loads(row[3])
        print('arti@@@@'+str(articleArray))
        langTitle = json.loads(row[0])[lang]
    conn.close()
    for i in range(len(articleArray)):
        if articleArray[i]["lang"]==lang:
            return jsonify({"title":langTitle, "result":articleArray[i]["text"]})
    
@app.route('/documents/<string:title>/<string:lang>/raw', methods=['GET'])
def get_raw_document(title, lang):
    print('get raw versions of : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT * FROM wiki WHERE title LIKE ? ORDER BY time DESC LIMIT 1"
    cur.execute(sql, ('%'+title+'%',))
    rows = cur.fetchall()
    langTitle = json.loads(rows[0][0])[lang]
    result=rows[0][2]
    print(result)
    return jsonify({"title": langTitle, "result":result})

@app.route('/documents/<string:title>', methods=['POST'])
def post_document(title):
    print('you are trying to post : '+ title)
    articlejson = request.get_json()['article']
    #
    langs=["ko","zh","es","en","hi","ar","pt","bn","ru","ja","pa","de"]
    cachejson = []
    print("now start making cache")
    for i in range(len(langs)):
        obj={"lang": langs[i]}
        objtext=""
        for j in range(len(articlejson)):
            objtext += gTranslate(articlejson[j]["text"], langs[i]) 
            objtext += " "
        obj["text"]=objtext
        cachejson.append(obj)
    cachestr=str(cachejson).replace("'",'"')
    #
    article=str(articlejson)
    article=article.replace("'",'"')
    print(article)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "INSERT INTO wiki VALUES (?, ?, ?, ?)"
    now = int(time.time())
    translated_title = gTranslateTitle(title)
    cur.execute(sql, (translated_title, now, article, cachestr))
    conn.commit()
    conn.close()
    return 'success posting'

@app.route('/documents/<string:title>/versions', methods=['GET'])
def get_all_version(title):
    print('get every versions of : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT time FROM wiki WHERE title LIKE ?"
    cur.execute(sql, ('%'+title+'%',))
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
    sql = "SELECT article FROM wiki WHERE title LIKE ? AND time = ?"
    cur.execute(sql, ('%'+title+'%',version,))
    rows = cur.fetchall()
    result=rows[0][0]
    print(result)
    return jsonify({"result":result})
@app.route('/documents/<string:title>/versions/<int:version>/<string:lang>', methods=['GET'])
def get_rendered_version(title, version, lang):
    print('you are trying to get : '+ title)
    conn = sqlite3.connect("res/documents.db")
    cur= conn.cursor()
    sql = "SELECT * FROM wiki WHERE title LIKE ? AND time = ?"
    cur.execute(sql, ('%'+title+'%',version,))
    rows = cur.fetchall()
    articleArray=None
    langTitle=None
    for row in rows:
        print(row[0])
        articleArray=json.loads(row[2])
        langTitle = json.loads(row[0])[lang]
    print(articleArray)
    for i in range(len(articleArray)):
        if articleArray[i]['lang']==lang:
            articleArray[i] = articleArray[i]['text']
        else :
            articleArray[i] = gTranslate(articleArray[i]['text'], lang)
    result = ' '.join(articleArray)
    print(result)
    conn.close()
    return jsonify({"title":langTitle, "result":result})


def gTranslate(inText, lang):
    text =u'{}'.format(inText)
    translate_client = translate.Client().from_service_account_json('gcpkey.json')
    target = lang
    translation = translate_client.translate(
        text,
        target_language=target)
    return u'{}'.format(translation['translatedText'])

def gTranslateTitle(title):
    allLangTitle={}
    print('gtt')
    langs=['ko','zh','es','en','hi','ar','pt','bn','ru','ja','pa','de']
    for i in range(len(langs)):
        text =u'{}'.format(title)
        translate_client = translate.Client().from_service_account_json('gcpkey.json')
        target = langs[i]
        translation = translate_client.translate(
        text,
        target_language=target)
        allLangTitle[langs[i]] = u'{}'.format(translation['translatedText'])
    output = str(allLangTitle)
    print('allttt: '+output)
    output=output.replace("'",'"')
    return output

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=80)

