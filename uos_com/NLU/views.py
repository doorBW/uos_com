#-*- coding:utf-8 -*-

from django.shortcuts import render
from konlpy.tag import Komoran
from imp import reload
import sys
# Create your views here.
def getInput(input):
	return 0

def MA(input):
	answer = ''
	answer += str(type(input))
	input = input.decode('utf-8')
	komoran = Komoran()
	answer = 'MA함수 호출'
	nouns = komoran.nouns(input)
	for i in nouns:
		answer += i
	answer += '//'
	answer += input
	return answer