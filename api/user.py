request = {
    "data": {
        "id": 1,
        "name": "なまえ",
        "email": "sample@sample.com",
        "hobby": "baseball",
    }
}

if __name__ == '__main__':

    for k, v in request["data"].items():
        print(k, v)
