import base64
import json


class Base(object):
    """ encode & decode を Base64 で試しす """

    def __init__(self, word):
        self.encoded = base64.b64encode(bytes(word, "utf-8"))

    def __str__(self):
        return self.encoded

    def logic(self):
        return {"sub": "{}".format(self.encoded)}


if __name__ == '__main__':
    base = Base('test')
    base2 = Base('test2')
    base3 = Base('test3')

    # encode
    print(base.encoded)
    print(base2.encoded)
    print(base3.encoded)
    print('-' * 20)

    # decode
    print(base64.b64decode(base.encoded))
    print(base64.b64decode(base2.encoded))
    print(base64.b64decode(base3.encoded))
    print('-' * 20)

    # logic encode
    base_logic = base.logic()

    print(type(base_logic))
    print(base_logic)

    base_logic_json = json.dumps(base_logic)
    print(type(base_logic_json))

    print(base_logic_json)
    print('-' * 20)

    # logic decode
    encode = base64.b64encode(bytes(str(base_logic), "utf-8"))
    print(encode)

    encode_ = base64.urlsafe_b64encode(encode)
    print(encode_)

    decode = base64.urlsafe_b64decode(encode)
    print(decode)
