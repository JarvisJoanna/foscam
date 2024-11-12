import hashlib


def md5(s: str):
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


if __name__ == '__main__':
    strs = '7d4ebc73f0044d21a2320e4a08f047f7F8A61102676D1695264686'
    print(md5(strs))
