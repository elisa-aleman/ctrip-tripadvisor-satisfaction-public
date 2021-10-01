#-*- coding: utf-8 -*-
#!python3

import string
import re
import sys

def ConstructNoiseVars():
    noise = string.punctuation
    cpun=["，","、","。","（","）","！","？",\
    "；","：","［","］","【","】","，","「","」",\
    "『","』","‧","《","》","〈","〉", "+","-", \
    "“", "”","‘","’", "＇","×", "ᵒ̤","👍","⚠", "​", "⊙"]
    noise.extend(cpun)
    romaji=["亅", "ω", "é", "è", "à", "ó"]
    romaji.extend(string.ascii_letters)
    hiraganamin = 'ぁ'
    hiraganamax = 'ん'
    katakanamin = 'ァ'
    katakanamax = 'ヿ'
    halfkatakanamin = 'ｦ'
    halfkatakanamax = 'ﾝ'
    kanjimin = '亜'
    kanjimax = '話'
    hangulminA = u'\u3130'
    hangulmaxA = u'\u318F'
    hangulminB = "가"
    hangulmaxB = "힣"
    splitlist = ["·","…", "～","⋯","·","〜","•","˙","️",\
                    "♨", "ᵒ","丶","＂","＂", ".", "…", "′", "－", "—", "�", \
                    "°","＝", "．", "̀", "∶", "ˇ", "‸"]
    splitlist.extend(noise)
    splitlist.extend(romaji)
    onsen = "♨"
    onsenu = u'\u2668'
    noisevars = (noise, romaji, hiraganamin, hiraganamax, \
        katakanamin, katakanamax, halfkatakanamin, halfkatakanamax, \
        kanjimin, kanjimax, hangulminA, hangulmaxA, hangulminB, hangulmaxB, splitlist, onsen, onsenu)
    return noisevars

def RemoveNoise(segmented, noisevars):
    comment=[]
    ##ReadNoisevars
    noise, romaji, hiraganamin, \
    hiraganamax, katakanamin, katakanamax,\
    halfkatakanamin, halfkatakanamax, \
    kanjimin, kanjimax, hangulminA, hangulmaxA,\
    hangulminB, hangulmaxB, splitlist, onsen, onsenu = noisevars
    for word in segmented:
        if isinstance(word, int):
            uword = str(word)
        else: 
            uword = word
        if uword not in noise:
            if (uword.isdigit()==False):
                isnoise=False
                isromaji=False
                isjapanese = False
                iskorean = False
                for char in uword:
                    charnum = char
                    if hiraganamin <= charnum <= hiraganamax:
                        isjapanese=True
                        isnoise=True
                    if katakanamin <= charnum <= katakanamax:
                        #and not kanjimin <= charnum <= kanjimax:
                        isjapanese=True
                        isnoise=True
                    if halfkatakanamin <= charnum <= halfkatakanamax:
                        isjapanese=True
                        isnoise=True
                    if (hangulminA <= charnum <= hangulmaxA) or (hangulminB <= charnum <= hangulmaxB):
                        iskorean=True
                        isnoise=True
                    if char in romaji:
                        isromaji=True
                    if char in noise:
                        isnoise=True
                    if (char.isdigit()):
                        isnoise=True
                if isromaji:
                    if (len(uword)==1):
                        isnoise=True
                if not isnoise:
                    spword = []
                    spword.append(uword)
                    for sp in splitlist:
                        nspword = [spm for temword in spword for spm in temword.split(sp)]
                        spword = nspword
                    noisewordadded = False
                    ###Split consecutive hao 
                    nspword = []
                    for i in spword:
                        if re.match(u'好+',i)!=None:
                            newi = list(i)
                            nspword+=newi
                        else:
                            nspword.append(i)
                    spword = nspword
                    ###
                    for i in spword:
                        if i in splitlist:
                            if (i == onsen or i == onsenu):
                                comment.append(i)
                        else: 
                            comment.append(i)
    return comment
#########################################
#########################################
#########################################

if __name__ == "__main__":
    pass