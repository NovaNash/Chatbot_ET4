#!/usr/bin/python3
#-*-coding-utf-8-*-

from itertools import *
import nltk.data
import nltk.tag
import sys
from nltk.tokenize import word_tokenize

listDoc = list()

"""Load every documents"""
def loadDocs(fileNames):
    #TODO fill the array to load files
    for fileName in fileNames:
        couple = list()
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
                wholePara = " ".join(lines[lastI+1:i])
                tempPara.append(nltk.sent_tokenize(wholePara))
                lastI = i+1

        #Get only dialog paragraphes
#        paragraph = []
#        for p in tempPara:
#            if len(p) > 0 and len(list(takewhile(lambda x : x== ' ', p[0]))) == 25: 
#                paragraph.append(p)

        paragraph = tempPara
        #Now get only questions
        lenP = len(paragraph)
        i = 0
        while i < lenP:
            #We need a question / answer, only one sentence per paragraph, and that this sentence finish by '?' or '?!' (maybe we can add some other things)
            if i + 1 < lenP and len(paragraph[i]) == 1 and paragraph[i][-1][-1] == '?' or len(paragraph[i]) == 2 and paragraph[i][-2][-1] == '?' and paragraph[i][-1] == "!":
                #Strip the line in this paragraph
                for j in range(len(paragraph[i])):
                    paragraph[i][j] = paragraph[i][j].strip()
                #And append it and its answer and our question
                couple.append([paragraph[i], paragraph[i+1]])
                i+=1
            i+=1

        transformLabel(couple)
        saveFile(couple, fileName)

"""Make labels"""
def transformLabel(couple):
    #Per response/answer
    for c in couple:
        #Per paragraph
        for p in c:
            #Per lines (we skip the first line)
            for i in range(0, len(p)):
                text   = word_tokenize(p[i])
                tokens = nltk.pos_tag(text, tagset="universal")

                thisPara = "" 
                for x in tokens:
                    if x[0] in ["Which", "What", "Who", "Where", "When", "How"]:
                        thisPara = thisPara + " " + "|".join([x[0], "QUESTIONTAG"])
                    else:
                        thisPara = thisPara + " " + "|".join(x)
                p[i] = thisPara

def saveFile(couple, fileName):
    text = "\n".join(["\n".join([p[0] for p in c if len(p) > 0]) for c in couple])
    with open("processed/"+fileName, "w") as f:
        f.write(text)

def main(argv):
    loadDocs(argv[1:])

if __name__ == "__main__":
    main(sys.argv)
