from PyQt5 import QtCore, QtGui, QtWidgets
#import mysql.connector
import tkinter as tk
import os
#import win32com.client
import csv
import re
import string
import operator
import numpy as np
from unidecode import unidecode
from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag_sents
from nltk.chunk.regexp import RegexpParser
from nltk.chunk import tree2conlltags
from nltk.corpus import stopwords
from itertools import chain, groupby
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer
class Ui_Form(object):
    
    def generate_candidate(self,texts, method='word', remove_punctuation=False):
        """
        Generate word candidate from given string

        Parameters
        ----------
        texts: str, input text string
        method: str, method to extract candidate words, either 'word' or 'phrase'

        Returns
        -------
        candidates: list, list of candidate words
        """
        words_ = list()
        candidates = list()

        # tokenize texts to list of sentences of words
        sentences = sent_tokenize(texts)
        #print(sentences)
        for sentence in sentences:
            if remove_punctuation:
                sentence = punct_re.sub(' ', sentence) # remove punctuation
            words = word_tokenize(sentence)
            words = list(map(lambda s: s.lower(), words))
            words_.append(words)
        tagged_words = pos_tag_sents(words_) # POS tagging

        if method == 'word':
            tags = set(['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'NNPS'])
            tagged_words = chain.from_iterable(tagged_words)
            for word, tag in tagged_words:
                if tag in tags and word.lower() not in stop_words:
                    candidates.append(word)
        elif method == 'phrase':
            grammar = r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'
            chunker = RegexpParser(grammar)
            all_tag = chain.from_iterable([tree2conlltags(chunker.parse(tag)) for tag in tagged_words])
            for key, group in groupby(all_tag, lambda tag: tag[2] != 'O'):
                candidate = ' '.join([word for (word, pos, chunk) in group])
                if key is True and candidate not in stop_words:
                    candidates.append(candidate)
        else:
            print("Use either 'word' or 'phrase' in method")
        #print("booooooooooooooooloooooooooooooooooooood\n")
        #print (candidates)
        return candidates


    def keyphrase_extraction_tfidf(self,texts, method='phrase', min_df=5, max_df=0.8, num_key=5):
        
        print('generating vocabulary candidate...')
        vocabulary = [self.generate_candidate(unidecode(text), method=method) for text in texts]
        vocabulary = list(chain(*vocabulary))
        vocabulary = list(np.unique(vocabulary)) # unique vocab
        print('done!')

        max_vocab_len = max(map(lambda s: len(s.split(' ')), vocabulary))
        tfidf_model = TfidfVectorizer(vocabulary=vocabulary, lowercase=True,
                                      ngram_range=(1,max_vocab_len), stop_words=None,
                                      min_df=min_df, max_df=max_df)
        X = tfidf_model.fit_transform(texts)
        vocabulary_sort = [v[0] for v in sorted(tfidf_model.vocabulary_.items(),
                                                key=operator.itemgetter(1))]
        print(max_vocab_len)
        sorted_array = np.fliplr(np.argsort(X.toarray()))

        # return list of top candidate phrase
        key_phrases = list()
        for sorted_array_doc in sorted_array:
            key_phrase = [vocabulary_sort[e] for e in sorted_array_doc[0:num_key]]
            key_phrases.append(key_phrase)

        return key_phrases


    def freqeunt_terms_extraction(texts, ngram_range=(1,1), n_terms=None):
        """
        Extract frequent terms using simple TFIDF ranking in given list of texts
        """
        tfidf_model = TfidfVectorizer(lowercase=True,
                                      ngram_range=ngram_range, stop_words=None,
                                      min_df=5, max_df=0.8)
        X = tfidf_model.fit_transform(texts)
        vocabulary_sort = [v[0] for v in sorted(tfidf_model.vocabulary_.items(),
                                                key=operator.itemgetter(1))]
        ranks = np.array(np.argsort(X.sum(axis=0))).ravel()
        frequent_terms = [vocabulary_sort[r] for r in ranks]
        frequent_terms = [f for f in frequent_terms if len(f) > 3]
        return frequent_terms_filter
    def setupUi(self, Form):
        root = tk.Tk()
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.left = 0
        self.top = 0
        print(self.width, self.height)
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        Form.setObjectName("Form")
        Form.resize(self.width, self.height)
        Form.setMouseTracking(True)
        Form.setAutoFillBackground(True)
        
        p = Form.palette()
        p.setColor(Form.backgroundRole(), QtGui.QColor(188, 196, 195))
        Form.setPalette(p)

        #Form.setStyleSheet("background-color : rgb(47,76,122)");


        self.label= QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(800, 30, 700, 50))
        self.label.setText("Keyword generation")
        self.label.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Black))

        
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(730, 120, 361, 70))
        self.label1.setText("Select text file")
        self.label1.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.addName = QtWidgets.QTextEdit(Form)
        self.addName.setGeometry(QtCore.QRect(100, 200, 1500, 650))
        self.addName.setObjectName("addName")
        self.addNameButton=QtWidgets.QPushButton(Form)
        self.addNameButton.setGeometry(QtCore.QRect(950,140,93,28))
        self.addNameButton.setObjectName("addNameButton")


        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(100, 930, 361, 70))
        self.label2.setText("Generated keywords ")
        self.label2.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.audlineEdit = QtWidgets.QTextEdit(Form)
        self.audlineEdit.setGeometry(QtCore.QRect(500, 930, 550, 60))
        self.audlineEdit.setObjectName("audlineEdit")
        
        


        self.objpushButton = QtWidgets.QPushButton(Form)
        self.objpushButton.setGeometry(QtCore.QRect(650, 850, 150, 50))
        self.objpushButton.setObjectName("objpushButton")


        self.addNameButton.clicked.connect(self.setImage1)
        #self.audpushButton.clicked.connect(self.setAudio)
        self.objpushButton.clicked.connect(self.additem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addNameButton.setText(_translate("Form","Browse"))
        #self.audpushButton.setText(_translate("Form", "Add audio"))
        self.objpushButton.setText(_translate("Form", "generate keyword"))

    def setImage1(self):
        import pandas as pd
        texts = list(pd.read_csv('something.txt')['abstract'])
        ifileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "/home/anika/Downloads/images", "Text Files (*.txt)")
        
        text=open('something.txt').read()
        self.addName.setText(text)
    

    def setAudio(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Audio", "/home/anika/Downloads/audios", "*.wav")
        print(fileName)
        self.audlineEdit.setText(fileName)

    def deleting(self):
        #self.imgLabel.clear()
        self.imglineEdit.setText("")
        self.imglineEdit2.setText("")
        self.imglineEdit3.setText("")
        #self.VideoLabel.clear()
        self.vidlineEdit.setText("")
        #self.audioLabel.clear()
        self.audlineEdit.setText("")
        self.addName.setText("")

    def additem(self):
        import pandas as pd
        #convertDocToPdf(DOC_FILEPATH)
        texts = list(pd.read_csv('something.txt')['abstract'])
        
        #texts = list(pd.read_csv('data/example.txt', error_bad_lines= False,quoting=csv.QUOTE_NONE)['abstract'])
        

        
        key_phrases = self.keyphrase_extraction_tfidf(texts)
        print(key_phrases[0])
        f= open("output.txt","w+")
        #print(texts[0])
        for val in key_phrases[0]:
            f.write(val)
            f.write(", ")
        f.close()
        text=open('output.txt').read()
        self.audlineEdit.setText(text)


if __name__ == "__main__":
    import sys

    punct_re = re.compile('[{}]'.format(re.escape(string.punctuation)))
    stop_words = set(stopwords.words('english'))
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

