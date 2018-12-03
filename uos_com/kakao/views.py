#-*- coding:utf-8 -*-
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt    #포스트 에러 방지
from NLU.views import MA

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
		answer = ''
		answer_list = {}
		if content == (chr(0x2753)+' 어떤 기능이 있나요?'):
			answer = '현재 다음과 같은 기능을 제공하고 있어요 :)< \n1. 채용공고 안내 \n예시) LG CNS 신입 채용공고 있어?'
		elif content == (chr(0x2753)+' 대화 시작할래요!'):
			answer = '네. 원하시는 기능을 말씀해주세요.'
		elif content == (chr(0x2753)+' 문의할게 있어요.'):
			answer = '해당 기능은 준비중 입니다.'
		else:
			answer_list = MA(content)
			# answer_list = {'action':action, 'company':company, 'who':who, 'res':str(res), 'url':url}
			if 'action' in answer_list:
				if answer_list['action'] == 1:
					if 'company' not in answer_list and int(answer_list['res']) > 0:
						answer = '네, 현재 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다. \n'
					elif int(answer_list['res']) > 0:
						answer = '네, 현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다. \n'
					elif 'company' not in answer_list:
						answer = '현재 '+answer_list['who']+'채용공고가 없습니다. \n'
					else:
						answer = '현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 없습니다. \n'
				else:
					answer = '????'
			else:
				answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-( \n저는 아직 LG채용 관련 내용만 답변드릴 수 있어요. \n오탈자나 띄어쓰기를 확인해주시고, 불편사항이 있으시다면 "챗봇 개선점"이라고 말씀해주세요.'

		if 'url' in answer_list:
			if answer_list['url'] != None:
				return JsonResponse({
							'message':{
								"user_key": "encryptedUserKey",
								'text': answer,
								'message_button':{
									'label': '채용공고 확인하기',
									'url': answer_list['url']
								}
							}
						})
			else:
				return JsonResponse({
							'message':{
								"user_key": "encryptedUserKey",
								'text': answer
							}
						})
		else:
			return JsonResponse({
						'message':{
							"user_key": "encryptedUserKey",
							'text': answer
						}
					})
	else:
		return False