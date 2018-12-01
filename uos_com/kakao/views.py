#-*- coding:utf-8 -*-
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt    #포스트 에러 방지

# Create your views here.
def index(requset):
	return 0

def userChatRoot(request):
	return 0

@csrf_exempt
def keyboardInit(request):
	return JsonResponse({
				'type':'buttons',
				'buttons':[ chr(0x2753)+' 어떤 기능이 있나요?',
							chr(0x2753)+' 대화 시작할래요!',
							chr(0x2753)+' 문의할게 있어요.']
				})

@csrf_exempt
def getMessage(request):
	if request.method == 'POST':
		message = (request.body).decode('utf-8')
		jsonMessage = json.loads(message)
		user_key = jsonMessage['user_key']
		message_type = jsonMessage['type']
		content = jsonMessage['content']
		answer = '사용자 입력:'
		answer += content
		return JsonResponse({
					'message':{
						"user_key": "encryptedUserKey",
						'text': answer
					},
					'keyboard':{
						'type':'text'
					}
				})
	else:
		return False