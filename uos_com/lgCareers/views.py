from django.shortcuts import render
from django.http import HttpResponse
from NLU.views import MA
# Create your views here.
def index(request):
	return 0

def getInput(request,input):
	answer = MA(input)
	return HttpResponse(answer+'/값 제대로 들어옴')