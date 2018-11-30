from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return 0

# just return string
def getInput(request,input):
	answer = ''
	answer += input
	answer += ' 값 제대로 들어왔음'
	return answer