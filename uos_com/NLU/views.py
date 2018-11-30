from django.shortcuts import render
from konlpy.tag import Komoran
# Create your views here.
def getInput(input):
	return 0

def MA(input):
	komoran = Komoran()
	answer = 'MA함수 호출'
	nouns = komoran.nouns(input)
	for i in nouns:
		answer += i
	answer += '//'
	answer += input
	return answer