import os
from django.core.management.base import BaseCommand, CommandError
from urlshortener.models import WordList

class Command(BaseCommand):
    args = 'None'
    help = 'It hopefully loads the word list given by Fyndiq to DB..:)))'

    def handle(self, *args, **options):
        print "we are starting.."
       
        parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        fixed_words_file = "%s/Resource/fixed_words.txt" % parent_directory

        lines = open(fixed_words_file, "r").readlines()
        for line in lines:
            fixed_word = line.strip()
            try:
                db_entry = WordList.objects.get(word=fixed_word)
            except WordList.DoesNotExist:
                obj = WordList(word=fixed_word)
                obj.save()