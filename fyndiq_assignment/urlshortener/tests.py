from urlshortener.models import WordList, PairedUrl
from django.test import TestCase
from urlshortener.views import *

#Tests to be created here...

def wordlist_load():
    words = ["scope", "improper", "collagen", "coin"]
    for word in words:
        w = WordList(word=word)
        w.save()

def gen_url_factory(url):
    key = key_generator(url)
    gen_url = PairedUrl(url=url, key_generated=key)
    gen_url.save()
    return gen_url
    
class Word_List_Test_Case(TestCase):
    def setUp(self):
        wordlist_load()
    
    def test_url_for_existing_alias(self):
        test_url = "http://example.com/8576/improper-lolol-lolo-coco/"
        w = key_generator(test_url)
        self.assertEqual("improper", w.word)
  
    def test_url_for_not_existing_alias(self):
        testurl = "http://example.com/8576/zamazingo-papparazzi/"
        w = key_generator(testurl)
        self.assertIsInstance(w, WordList)

    def word_list_pen_test(self):
        g1 = gen_url_factory("http://example.com/8576/scope-bounce-bourn/")
        g2 = gen_url_factory("http://example.com/8576/scope-improper-bourn/")
        g3 = gen_url_factory("http://example.com/8576/scope-improper-coin/")
        g4 = gen_url_factory("http://example.com/8576/scope-collagen-bourn/")
        g5 = gen_url_factory("http://example.com/8576/grosskreutz/")
        
        word = WordList.objects.filter(word="scope")[0]
        self.assertEqual(True, hasattr(word, "pairedurl"))
        self.assertEqual(g5.key_generated.word, "scope")