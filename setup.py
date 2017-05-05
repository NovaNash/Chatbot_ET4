#!/usr/bin/python3
#-*-coding-utf-8-*-

from itertools import *
import nltk.data
import nltk.tag
from nltk.tokenize import word_tokenize

listDoc = list()

"""Load every documents"""
def loadDocs():
    couple = list()

    #TODO fill the array to load files
    for fileName in ["American-Pie.txt"]:
        #Get the data from a file
        data = None
        with open(fileName, "r") as f:
            data = f.read()

        #Get only dialogues
        lines = data.split('\n')
        for i in range(len(lines)):
            #Find the first dialog (start with 25 spaces and the nextline has some contents)
            if len(list(takewhile(lambda x : x== ' ', lines[i]))) == 25 and len(lines[i+1]) > 1: 
                lines = lines[i::]
                break;

        #We cut in paragraph
        tempPara = list()
        lastI = 0
        for i in range(len(lines)):
            if len(lines[i])==0:
                tempPara.append(lines[lastI:i])
                lastI = i+1

        #Get only dialog paragraphes
        paragraph = []
        for p in tempPara:
            if len(p) > 0 and len(list(takewhile(lambda x : x== ' ', p[0]))) == 25: 
                paragraph.append(p)

        #Now get only questions
        lenP = len(paragraph)
        i = 0
        while i < lenP:
            #We need a question / answer, only one sentence per paragraph, and that this sentence finish by '?' or '?!' (maybe we can add some other things)
            if i + 1 < lenP and len(paragraph[i]) == 1 and paragraph[i][-1][-1] == '?' or paragraph[i][-1][-2] == '?' and paragraph[i][-1][-1] == '!':
                #Strip the line in this paragraph
                for j in range(len(paragraph[i])):
                    paragraph[i][j] = paragraph[i][j].strip()
                #And append it and its answer and our question
                couple.append([paragraph[i], paragraph[i+1]])
            i+=1
    transformLabel(couple)

    saveFile(couple)

"""Make labels"""
def transformLabel(couple):
    #Per response/answer
    for c in couple:
        #Per paragraph
        for p in c:
            #Per lines (we skip the first line)
            for i in range(1, len(p)):
                text = word_tokenize(p[i])
                p[i] = " ".join("|".join(x) for x in nltk.pos_tag(text, tagset="universal"))
                print(p)

def saveFile(couple):
    print(couple[0])
    text = "".join(["\n".join([p[1] for p in c]) for c in couple])
    with open("file.txt", "w") as f:
        f.write(text)

def main():
    loadDocs()
    pass

if __name__ == "__main__":
    main()
