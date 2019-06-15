# -*- coding: utf-8 -*-
#split at ?, । or !
import re
import math
import numpy as np
import operator
from stemmer import Stemmer
st=Stemmer()

def tokenize_sentence(text):
    sentences=re.split('(?<=[।?!]) +', text)
    return sentences

def tokenize_word(sentences):
    words=[]
    for sentence in sentences:
        words.extend(re.split(', |,| ', sentence))
    return words

def clean_text(words):
    punctuations=r',|\)|\(|\{|\}|\[|\]|\?|\!|।|\‘|\’|\“|\”|\:-|/|—|-'
    numbers = r'[0-9०o१२३४५६७८९]'
    words = [re.sub(numbers, '', i) for i in words]
    words = [re.sub(punctuations, '', i) for i in words]
    #Removing empty strings
    words = [x for x in words if x]
    return words


def remove_stopwords(words):
    with open('datasets/stopwords.txt',encoding="utf8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
#     print("Stopwords dataset")
#     print(lines)
    words = [w for w in words if not w in lines]
    return words

def stem(tokens):
    rep,i,k,repc=0,0,0,0
    new=[]
    unrecog=[]
    count=1
    for token in tokens:
        p="yes"
        i,k = 0,0 #no. of suffix and prefix found
        print("\nUnstemmed input token"+str(count)+":"+token)
        orig_token=token
        end=False
        while (not end):
            print("Checking root word or not")
            if (st.isRoot(token) or( st.isAltRoot(token) and i>0)):
                print("comdition1")
                if( st.isAltRoot(token) and i>0):
                    st.setRoot(st.getAltRoot(token))

                else:
                    st.setRoot(token)
                    print("\nRoot word found:"+token)
                end=True

            elif (st.isRoot(token + "\u094d")) :
                print("comdition2")

                i+=1
                st.setSMorph_number(i)
                st.isASuffix(token)
                token = st.getRoot()


            elif (token.endswith("\u094d") and st.isRoot(token[:len(token)-1])):
                print("comdition3")
                token=token[:len(token)-1]
                st.setRoot(token)

            elif (st.suffixPresent(token,i)) :
                print("comdition4")
                i+=1
                st.setSMorph_number(i)
                st.stripSuffix(token)
                token = st.getRoot()

            elif (st.prefixPresent(token)) :
                print("comdition5")
                k+=1
                st.setPMorph_number(k)
                st.stripPrefix(token)
                token = st.getRoot()

            else:
                print("\nRecombining suffix")

    #           if prefix and suffix present
                if (k > 0 and i > 0) :
                    print("comdition6:bot suffix and prefix found previously")

                    a = st.getPMorph()
                    print("PMorph:"+str(a))
                    for k1 in range(k,0,-1):
                        tmp = token
                        for l in range(i,0,-1):
                            tm = st.generateWord(tmp, l)
                            print("generated word: "+tm)

                            if (st.isRoot(tm) or ( st.isAltRoot(tm) and i>0)):
                                bk = 1
                                st.setSMorph_number(l - 1)
                                st.setPMorph_number(k)
                                if(( st.isAltRoot(tm) and i>0)):
                                    st.setRoot(st.getAltRoot(tm))
                                else:
                                    st.setRoot(tm)
                                token = st.getRoot()
                                break
                            else:
                                bk = 0
                                tmp = tm

                        if (bk == 1) :
                            break


                        if (k1 > 1):
                            token = a[k1] + token


                    if (bk != 1) :
                        st.setRoot("unrecognized")

                        k = 0


                else:
                    print("comdition7:unrecognized")

                    st.setRoot("unrecognized")


                if (st.getRoot()==("unrecognized")):
                    rep+=1

                    repeat = 0
    #               for the second parse
                    if (rep == 1) :
    #                   check for if the any rulenumber of the suffix contains repeat sign "Y"
                        for l in range(i,0,-1):
                            if (st.isRepeat(str(st.getSMorph_rulenum(l)))):
                                repeat = 1
                                break #//for any suffix that has a repeat sign.
                            else:
                                repeat = 0


    #               if any rulenumber has the suffix content as repeat sign"Y"
                    if (repeat == 1) :
                        token = origtoken
                        st.setPMorph_number(0)
                        st.setSMorph_number(0)
                        i = 0
                        k = 0
                        st.setSecParse(rep)
                    else:
                        break
        if(st.getRoot()==("unrecognized")):
            unrecog.append(orig_token)
            new.append(orig_token)
            print("\nfinal token (couldnt stem):"+orig_token)

        else:
            new.append(st.getRoot())
            print("\nfinal stemmed token:"+st.getRoot())
        count+=1
    return new

def preprocess(text):
    sentences=tokenize_sentence(text)
    words=tokenize_word(sentences)
    words=clean_text(words)
    words=remove_stopwords(words)
    words=stem(words)
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

def read(path):
    with open (path,  encoding="utf8") as myfile:
        return myfile.read()


def similarity(eg1, eg2):
    tokens1 = preprocess(eg1)
    tokens2 = preprocess(eg2)
    global vocabulary
    vocabulary = sorted(set(tokens1 + tokens2))
    global Docs
    Docs = [tokens1, tokens2]
    TFIDF_Vector = create_vector()
    jsim = get_jaccard_sim(tokens1, tokens2)
    csim = get_cosine_sim(TFIDF_Vector[0], TFIDF_Vector[1])
    return (jsim, csim)


def get_final_list(basepath):
    import os
    mylist = []
    path = []
    data = []

    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            mylist.append(entry)
    basepath1=basepath+'/'

    for i in range(0, len(mylist)):
        path.append(basepath1 + mylist[i])

    from itertools import combinations
    comb = list(combinations(path, 2))
    dic = {}
    dic_cosim = {}
    for com in comb:
        between = "between" + com[0].replace(basepath1,
                                             '') + ' and ' + com[1].replace(
            basepath1, '')
        sim = similarity(read(com[0]), read(com[1]))
        dic[between] = sim
        dic_cosim[between] = sim[1]

    sorted_x = sorted(dic_cosim.items(), key=operator.itemgetter(1), reverse=True)
    final_list = []
    for i in sorted_x:
        final_list.append(i[0] + " " + str(dic[i[0]]))

    return (final_list)
