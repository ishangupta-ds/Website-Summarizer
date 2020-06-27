import urllib.request
from inscriptis import get_text
import re
import nltk
import contractions
import string


class Preprocesstowords:

    def __init__(self, url):

        self.url = url

    def textpreprocessor(self):

        try:
            html = urllib.request.urlopen(self.url).read().decode('utf-8')
        except:
            print("not good url try again!")

        sitetext = get_text(html)

        #expand words
        def replace_contractions(text):
            """Replace contractions in string of text"""
            return contractions.fix(text)

        uncontracted = replace_contractions(sitetext)

        #text cleaning
        cleantext=' '

        for i, char in enumerate(uncontracted):
            if ord(char) in [46, 95] or ord(char) in range(48, 58) or ord(char) in range(65, 91) or ord(char) in range(97, 123):
                if i != 0 and i != (len(uncontracted)-1):
                    if uncontracted[i-1] != '.' or uncontracted[i-1] != ' ' or ord(uncontracted[i-1]) != 10 or ord(uncontracted[i-1]) != 13:
                        if uncontracted[i+1] != '.' or uncontracted[i+1] != ' ' or ord(uncontracted[i+1]) != 10 or ord(uncontracted[i+1]) != 13:
                            if uncontracted[i-1] == ' ' and uncontracted[i+1] == ' ':
                                continue
                            else:
                                cleantext += char
            elif ord(char) in [10, 13]:
                cleantext += '.'
            else:
                cleantext += ' '

        textset = " "

        for i, char in enumerate(cleantext):
            if uncontracted[i - 1] == ' ' and uncontracted[i + 1] == ' ':
                continue
            elif ord(char) == 9:
                continue
            elif uncontracted[i] == ' ' and uncontracted[i + 1] == ' ':
                continue
            else:
                textset += char

        #text processing
        #Convert text to lowercase
        lower_textset = textset.lower()
        #Remove numbers
        nonnumber_textset = re.sub(r"\d+", ' ', lower_textset)
        #Remove punctuation
        nopunc_textset = nonnumber_textset.translate(str.maketrans('', '', string.punctuation))
        #Remove whitespaces
        nopunc_textset = nopunc_textset.strip()
        #tokenization
        words = nltk.word_tokenize(nopunc_textset)

        return words

