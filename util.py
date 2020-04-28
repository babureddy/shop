from cryptography.fernet import Fernet # pip install cryptography
def encrypt(s):
    key = Fernet.generate_key()
    f = Fernet(key)
    e = f.encrypt(s)
    return e
    # print(e)
    # >>> token
    # d = f.decrypt(e)
    # print(d)
    # b'This is a SECRET! message.'
