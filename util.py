from io import BytesIO
from pdfdocument.document import PDFDocument

from datetime import date
import random
import sys
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

def makemPdf():
  pdf = PDFDocument("qa.pdf")
  pdf.init_report()
  pdf.h1("Bindu's Jewelery Store")
  pdf.h2("Sanjaynagar, Bangalore 560094")
  pdf.h2('9480529032, 8795652460')  
  pdf.h2("Receipt",pdf.style.center)
  pdf.hr()
  pdf.generate()

