request = {
    "data": {
        "id": 1,
        "name": "なまえ",
        "email": "sample@sample.com",
        "hobby": "baseball",
    }
}

request_user = [
    {
        "data": {
            "user": {
                "id": 1,
                "name": "なまえ",
                "email": "sample@sample.com",
                "post_number": "111-1111",
                "address1": "大阪府",
                "address2": "大阪市",
                "job": "witter"
            }
        }
    }
]

if __name__ == '__main__':

    # for k, v in request["data"].items():
    #     print(k, v)

    for k, v in request_user[0]['data']['user'].items():
        print(k, v)
