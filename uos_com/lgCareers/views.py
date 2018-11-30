from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return 0

def getInput(request,input):
	return HttpResponse(input+' 값 제대로 들어옴')