# source: https://www.tangowithdjango.com/book17/chapters/models.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.models import *

from django.contrib.auth.models import User
import csv
import json

def random_password(length=10):
    from string import digits, ascii_letters
    from random import choices, shuffle
    chars = list(f"{digits}{ascii_letters}!#$%&'*+-<=>?@^_|~")
    shuffle(chars)
    result = choices(chars, k=length)
    return ''.join(result)

"""
The input file must be a UTF-8 encoded, csv file with three columns and no headers.
The content of the row must be : <names>,<email>,<password>
This file must be built manually in with some spreadsheet tool. To generate 
passwords use the function  `random_password`

Example of row:

    Aragu Vara Karle Mary,aragu.mery1991@gmail.com,Q+#ySkxo4f

"""
def add_annotators():
    # Make sure .csv is saved as UTF-8 encoding
    input_file = 'data/Lista_anotadores_03.csv'
    with open(input_file, encoding="utf-8") as csv_file:            
        rows = list(csv.reader(csv_file, delimiter=','))
        for i, row in enumerate(rows):
            name = row[0]
            username = row[1] #same as email
            password = row[2]
            
            #print(i, username, password, name)
            #if i == 0 : break

            u, _ = User.objects.get_or_create(username=username)
            u.set_password(password)
            u.save()

            #Mirror an annotator with same id as user
            a, _ = Annotator.objects.get_or_create(id=u.id, name=name)
            
            print(i, username, password, name, 'id=' + str(u.id))


if __name__ == '__main__':
    print("Adding annotators...")
    add_annotators()
