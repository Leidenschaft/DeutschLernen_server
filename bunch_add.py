# add a bunch of words from txt format
from django.test import Client
import django

from Word_edit import html_form_to_xml

django.setup()
client = Client()

def add_word_using_api(index, word):
    parts = word.split(' ')

    data = {'Stichwort' : parts[0],
            'category' : 'Substantiv',
            'isCreated' : '',
            'wordAddr' :  '/Wort/%d.xml' % index,
            'explanation_1': parts[0]
            }
    if len(parts) > 1:
        data['Ausspache'] = parts[1].rstrip()
    if len(parts) > 2:
        data['explanation_1'] = parts[2]
    response = client.post('/Word_edit/create_new_word', data)
    assert(response.status_code == 200)

if __name__ == '__main__':
    
    # treat all words as Substantiv
    noun_len = html_form_to_xml.addWord('', '', '', word_type='Substantiv')
    noun_len = int(noun_len)
    with open('build/word.txt') as f:
        word = f.readline()
        while word != '':
            add_word_using_api(noun_len, word)
            noun_len += 1
            word = f.readline()