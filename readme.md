# Summary of documents.db structure.
1. Every Document is stored in only one table named "wiki"
2. Each row represents each version of the document.
3. The first column:title:text reperesents title of the document which must be in Korean.
4. The second column:time:integer represents time(format : Unix Time) of the version.
5. The third column:article:text represents string converted form of contents-JSONArray.
6. Each content of the contents-JSONArray should be aligned in order of text flow.

# Sample of contents-JSONArray
    [    
        {
            "lang": "ko",
            "text": "후추의 열매는 직경 5mm의 핵과로 열매 안에 한 개의 씨가 있으며 다 익으면 어두운 붉은 색을 띤다. 후추는 향신료로 쓰기 위해 다 익기 전에 수확하여 건조하며 이렇게 만들어진 후추는 검은 빛을 띤다. 흰 후추, 붉은 후추도 모두 같은 열매로 만든 것인데, 흰 후추는 검은 후추의 껍질을 제거한 것이고 붉은 후추는 다 익은 열매를 사용한 것이다. 검은 후추와 백색 후추가 요리에 주로 쓰인다."
        },
        {
            "lang": "en",
            "text": "As of 2016, Vietnam was the world's largest producer and exporter of black peppercorns, producing 216,000 tonnes or 39% of the world total of 546,000 tonnes. Other major producers include Indonesia (15%), India (10%), and Brazil (10%). Global pepper production may vary annually according to crop management, disease, and weather. Vietnam dominates the export market, using almost none of its production domestically."
        },
        {
            "lang": "zh-CN",
            "text": "胡椒的辛辣味主要来源于化合物胡椒碱，胡椒碱同时存在于果皮和种子中。按毫克来计算，精制胡椒碱的辣度大约是辣椒中辣椒素的百分之一。胡椒的外果皮中还含有可产生气味的蒎烯、桧烯、苯烯、石竹烯与芳樟醇等萜类，这些还是让柠檬、树木和花朵等产生气味的物质。白胡椒几乎失去了这些气味，因为白胡椒去掉了果皮层。由于要经历更长的发酵阶段，白胡椒会获得其他的一些气味（包括霉味）"
        },
        {
            "lang": "ko",
            "text": "후추는 선사시대부터 인도에서 양념으로 쓰였다. 아주 오래전부터 후추는 주요 무역 상품이었으며 종종 실물화폐로 사용되어 <검은 금>이라 불렸다. 청년사에서 만든 《조선시대 사람들은 어떻게 살았을까?》에 의하면 조선에서도 후추는 연회에서 손님이 후추를 상에 올리면 기녀들이 다툴 만큼 인기가 있었다. 후추로 지불하는 지대는 오늘날에도 무역의 거래조건으로 존재한다."
        },
    ]

# REST API
1. GET /documents/:title/:lang 
2. POST /documents/:title/:lang
> example: GET http://localhost:3000/documents/후추/ko
# Supported Language
Every language available in GCP Translation API is supported
Avaliable (Language Code / Language) set can be seen in the link below.
> https://cloud.google.com/translate/docs/languages