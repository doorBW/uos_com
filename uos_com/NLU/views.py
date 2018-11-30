#-*- coding:utf-8 -*-

from django.shortcuts import render
from konlpy.tag import Komoran
from imp import reload
from urllib.parse import unquote
# Create your views here.
def getInput(input):
	return 0

def MA(input):
	input = unquote(input)
	komoran = Komoran()
	answer = 'MA함수 호출'
	nouns = komoran.nouns(input)
	for i in nouns:
		answer += i
		answer += '*'
	answer += '//'
	answer += input
	return answer