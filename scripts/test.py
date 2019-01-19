import json, os, requests, uuid
from google.cloud import translate
def gTranslate(inText):
    text =u'{}'.format(inText)
    translate_client = translate.Client()
    target ='ko'
    translation = translate_client.translate(
        text,
        target_language=target)
    return u'{}'.format(translation['translatedText'])
'''
def translate(text):
    subscriptionKey = "a33c2ee62a9843c3b4c90a3b5903a141"
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=ko'
    constructed_url = base_url + path + params
    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text' : text
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
  #  result= json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': '))
    print(response[0]['translations'][0]['text'])
text = 'As of 2016, Vietnam was the worlds largest producer and exporter of black peppercorns, producing 216,000 tonnes or 39% of the world total of 546,000 tonnes. Other major producers include Indonesia (15%), India (10%), and Brazil (10%). Global pepper production may vary annually according to crop management, disease, and weather. Vietnam dominates the export market, using almost none of its production domestically.'
translate(text)
'''
text = 'コショウは、古代からインド地方の主要な輸出品だった。紀元前4世紀の初め頃、古代ギリシアの植物学者テオフラストゥスは『植物誌』の中でコショウと長コショウを考察している。コショウは当時から貴重で、紀元1世紀のローマの歴史家大プリニウスは1ポンド（約500グラム）の長コショウの価値は15デナーリ、白コショウは7デナーリ、黒コショウは4デナーリと記録している。古代の地中海世界では、長コショウが成熟したものが黒コショウになると考えられており、その間違いは、16世紀にガルシア・デ・オルタによって改められるまで続いた'
print(gTranslate(text))

