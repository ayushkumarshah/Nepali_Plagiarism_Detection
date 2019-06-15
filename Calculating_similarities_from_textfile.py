# -*- coding: utf-8 -*-
#split at ?, । or !
import re
import math
import numpy as np
import docx


def tokenize_sentence(text):
    sentences=re.split('(?<=[।?!]) +', text)
    print("Sentences")
    print(sentences)
    return sentences

def tokenize_word(sentences):
    words=[]
    for sentence in sentences:
        words.extend(re.split(', |,| ', sentence))
    print("Words after tokenization")
    print (words)
    return words

def clean_text(words):
    punctuations=r',|\)|\(|\{|\}|\[|\]|\?|\!|।|\‘|\’|\“|\”|\:-|/|—|-'
    numbers = r'[0-9o१२३४५६७८९]'
    words = [re.sub(numbers, '', i) for i in words]
    words = [re.sub(punctuations, '', i) for i in words]
    #Removing empty strings
    words = [x for x in words if x]
    print("After removing special symbols and numbers")
    print(words)
    return words


def remove_stopwords(words):
    with open('datasets/stopwords.txt',encoding="utf8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
#     print("Stopwords dataset")
#     print(lines)
    words = [w for w in words if not w in lines]
    print("Words after removing stopwords")
    print(words)
    return words

def preprocess(text):
    sentences=tokenize_sentence(text)
    words=tokenize_word(sentences)
    words=clean_text(words)
    words=remove_stopwords(words)
    return words

def calculate_TF_Dict(doc):
    """ Returns a tf dictionary for each doc whose keys are all
    the unique words in the review and whose values are their
    corresponding tf.
    """
    TF_Dict = {}

    # Total number of terms in the document
    len_of_document = float(len(doc))

    for word in doc:

        # Number of times the term occurs in the document
        term_in_document = doc.count(word)

        #Computes tf for each word
        TF_Dict[word] = term_in_document / len_of_document


    return TF_Dict

def calculate_IDF_Dict():
    """ Returns a dictionary whose keys are all the unique words in the
    dataset and whose values are their corresponding idf.
    """
    countDict = {}
    for word in vocabulary:
        countDict[word]=0
    # Run through each doc's tf dictionary and increment countDict's (word, doc) pair
    for word in vocabulary:
        for doc in range(len(Docs)):
            if word in Docs[doc]:
                countDict[word]+=1


    #Stores the doc count dictionary
    IDF_Dict = {}
    total_num_docs = len(Docs)
    for word in countDict:
        IDF_Dict[word] = 1+math.log(float(total_num_docs) /countDict[word])
    return IDF_Dict

def calculate_TFIDF_Dict(TF_Dict,IDF_Dict):
    """ Returns a dictionary whose keys are all the unique words in the
    review and whose values are their corresponding tfidf.
    """
    TFIDF_Dict = {}
    #For each word in the review, we multiply its tf and its idf.
    for word in TF_Dict:
        TFIDF_Dict[word] = TF_Dict[word] * IDF_Dict[word]
    return TFIDF_Dict


def calculate_TFIDF_Vector(doc):
    TFIDF_Vector = [0.0] * len(vocabulary)
    # For each unique word, if it is in the doc, store its TF-IDF value.
    for i, word in enumerate(vocabulary):
          if word in doc:
                TFIDF_Vector[i] = doc[word]

    return TFIDF_Vector

def create_vector():
    TF_Dict = [calculate_TF_Dict(doc) for doc in Docs]
    IDF_Dict=calculate_IDF_Dict()
    TFIDF_Dict = [calculate_TFIDF_Dict(doc,IDF_Dict) for doc in TF_Dict]
    TFIDF_Vector = [calculate_TFIDF_Vector(doc) for doc in TFIDF_Dict]
    return TFIDF_Vector


def get_jaccard_sim(token1, token2):
    a = set(token1)
    b = set(token2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def get_cosine_sim(a,b):
    a = np.array(a)
    b = np.array(b)
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    return cos


def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

eg1=readtxt('D:\nlp_project\Nepali_Plagiarism_Detection\datasets\data\Student1.docx')
tokens1=preprocess(eg1)
eg2=readtxt('D:\nlp_project\Nepali_Plagiarism_Detection\datasets\data\Student2.docx')
tokens2=preprocess(eg2)
print(tokens1)
print(tokens2)
vocabulary=sorted(set(tokens1+tokens2))
Docs=[tokens1,tokens2]
TFIDF_Vector=create_vector()
print(TFIDF_Vector)
jsim=get_jaccard_sim(tokens1,tokens2)
csim=get_cosine_sim(TFIDF_Vector[0],TFIDF_Vector[1])
print(jsim)
print(csim)
