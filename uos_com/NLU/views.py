#-*- coding:utf-8 -*-

from django.shortcuts import render
from konlpy.tag import Komoran
from imp import reload
from urllib.parse import unquote
# Create your views here.
def getInput(input):
	return 0

def MA(input):
	answer = ''
	input = unquote(input)
	komoran = Komoran()
	nouns = komoran.nouns(input)
	answer += '형태소 분석 결과: '
	for i in nouns:
		answer += i
		answer += ', '
	return answer