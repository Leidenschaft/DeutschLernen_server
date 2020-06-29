from django.test import TestCase
from Word_edit import html_form_to_xml
import os

class WordEditTest(TestCase):
    def test_get_form(self):
        response = self.client.get('/Word_edit/create_new_word')
        self.assertEqual(response.status_code, 200)
    def test_post_form(self):
        data = {'Stichwort' : 'Abschlussarbeit',
                        'category' : 'Substantiv',
                        'Genus' :  'die',
                        'unittype'  :  '3',
                        'Anteil' : '1',
                        'isCreated' : '',
                        'wordAddr' :  '/Wort/233.xml',
                        'explanation_1': 'thesis',
                        'translation_1_1': 'He is writing his thesis',
                        'original_1_1': 'Er schreibt gerade an seiner Abschlussarbeit.'
                        }
        response = self.client.post('/Word_edit/create_new_word', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists('frontend/Wort/233.xml'))
        os.remove('frontend/Wort/233.xml')

    def test_post_empty_stichwort(self):
        data = {'category': 'Substantiv'}
        response = self.client.post('/Word_edit/create_new_word', data)
        self.assertEqual(response.status_code, 400)
    def test_post_empty_explanation(self):
        data = {'category': 'Substantiv', 'Stichwort': 'Abschlussarbeit'}
        response = self.client.post('/Word_edit/create_new_word', data)
        self.assertEqual(response.status_code, 400)

    def test_post_form_minimal(self):
        data = {'Stichwort' : 'Apfel',
                        'category' : 'Substantiv',
                        'isCreated' : '',
                        'wordAddr' :  '/Wort/233.xml',
                        'explanation_1': 'apple'
                }
        response = self.client.post('/Word_edit/create_new_word', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists('frontend/Wort/233.xml'))
        os.remove('frontend/Wort/233.xml')

    def test_post_form_verb(self):
        data = {'Stichwort' : 'haben',
                        'category' : 'Verben',
                        'isCreated' : '',
                        'wordAddr' :  '/Wort/V233.xml',
                        'explanation_1': 'have'
                }
        response = self.client.post('/Word_edit/create_new_word', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists('frontend/Wort/V233.xml'))
        os.remove('frontend/Wort/V233.xml')

class UtilityTest(TestCase):
    def test_function_addWord(self):
        noun_len = html_form_to_xml.addWord('', '', '', word_type='Substantiv')
        self.assertEqual(noun_len, 1)
        verb_len = html_form_to_xml.addWord('', '', '', word_type='Verben')
        self.assertEqual(verb_len, 1)
        a_len = html_form_to_xml.addWord('', '', '', word_type='Others')
        self.assertEqual(a_len, 1)
