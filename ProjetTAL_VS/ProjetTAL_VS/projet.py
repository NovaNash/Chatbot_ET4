#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Tue Apr 18 14:09:35 2017

@author: nova
"""

import nltk
import nltk.data
import nltk.tag
import sys
from nltk.tokenize import word_tokenize

#lit le corpus et le sépare en couple de question réponse
#supose que M a trouvé un corpus entre 2 personnes commençant par des tirets (paire de phrase)
def read_corpus(fileName):
    listCouple = []
    with open(fileName) as f:
        listSent = f.read().split("\n")
        i = 0
        while i < len(listSent):
            listCouple.append((listSent[i].strip(),listSent[i+1].strip()))
            i=i+2
    return listCouple

#separe en trois donnees
def split_data(listData):
    train = listData[0:int(0.70*len(listData))]
    dev = listData[int(0.70*len(listData)):int(0.85*len(listData))]
    test = listData[int(0.85*len(listData)):]
    return train, dev, test

#separe les mots de la question
def split_word(listData):
    listCouple = []
    for c in listData:
        question = c[0].split(" ")
        answer = c[1]
        
        listCouple.append((question, answer))
    return listCouple

#separe le mot de la question de son etiquette de son etiquette
def split_label(listData):
    listCouple = []
    for c in listData:
        question = []
        answer = c[1]
        for w in c[0]:
            label = w.split("|")
            question.append(label)
        listCouple.append((question,answer))
    return listCouple

#pondere les mots de la question
def pound_questionDB(listData):
    listCouple = []
    for c in listData:
        for w in c[0]:
            if w[1] == 'QUESTIONTAG':
                w.append(2)
            elif w[1] == 'VERB':
                w.append(1.2)
            elif w[1] == 'NOUN' or w[1] == 'PRON':
                w.append(0.7)
            elif w[1] == 'ADP' or w[1] == 'ADV':
                w.append(0.25)
            elif w[1] == 'ADJ':
                w.append(0.25)
            else:
                w.append(0)

    listCouple=listData
    return listCouple

def make_database(listData):
    listDB = pound_questionDB(split_label(split_word(listData)))
    dicoDB = dict()
    for c in listDB:
        hasFoundQT = False
        for w in c[0]:
            if w[1] == 'QUESTIONTAG':
                hasFoundQT = True
                if w[0] in dicoDB:
                    dicoDB[w[0]].append(list(c))
                else: 
                    l = list()
                    l.append(list(c))
                    dicoDB[w[0]] = l

        if not hasFoundQT:
            if not "None" in dicoDB:
                l = list()
                l.append(list(c))
                dicoDB["None"] = l
            else:
                dicoDB["None"].append(list(c))
    return dicoDB
          
#traite la question : separe les mots et les pondere
def split_question(question):
    #Tokenize the question
    cutQ = word_tokenize(question)
    tokens = nltk.pos_tag(cutQ, tagset="universal")

    question = " ".join(["|".join([w for w in word]) for word in tokens])

    word = question.split(" ")
    label = []
    for w in word:
        word = w.split("|")
        label.append(word)

    questionTag = None
    for w in label:
        if w[1] == 'QUESTIONTAG':
            questionTag = w[0]
            w.append(2)
        elif w[1] == 'VERB':
            w.append(1.2)
        elif w[1] == 'NOUN' or w[1] == 'PRON':
            w.append(0.7)
        elif w[1] == 'ADP' or w[1] == 'ADV':
            w.append(0.25)
        elif w[1] == 'ADJ':
            w.append(0.25)
        else:
            w.append(0)

    return label, questionTag
          
  
def answer(dataBase, question):
    questionOK, qTag = split_question(question)
    if qTag == None:
        qTag = "None"

    couple = None
    val = 0

    if not qTag in dataBase:
        return "There is no answer to this"
    
    for c in dataBase[qTag]:
        value = 0
        for w in c[0]:
            for m in questionOK:
                if m[0] == w[0]:
                    value = value + w[-1]
        if value > val:
            val = value
            couple = c
    if couple:
        return couple[1]
    return "There is no answer to this"

if __name__ == "__main__":
    #Le main
    listQA = read_corpus("processed/American-Pie.txt")
    train, dev, test = split_data(listQA)
    dataBase = make_database(train)
    question = input()
    answer = answer(dataBase, question)
    print(answer)
    
    
