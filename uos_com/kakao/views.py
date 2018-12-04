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
							chr(0x2753)+' 기능 이용할래요!',
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
			answer = '현재 다음과 같은 기능을 제공하고 있어요 :-) \n1. 채용공고 안내 \n예시) LG CNS 신입 채용공고 있어? \n2. 채용절차 안내 \n예시) 신입 채용절차가 어떻게 돼? \n3. 채용문의 \n예시) 자주묻는질문은 뭐가 있어?'
		elif content == (chr(0x2753)+' 기능 이용할래요!'):
			answer = '네. 원하시는 기능을 말씀해주세요. \n(채용공고안내, 채용절차안내, 채용문의에 대한 기능이 제공되고 있습니다.)'
			return JsonResponse({
						'message':{
							"user_key": "encryptedUserKey",
							'text': answer
						}
					})
		elif content == (chr(0x2753)+' 문의할게 있어요.'):
			answer = '현재 1:1질문은 로그인상태에서만 가능합니다 :-( \n 자주묻는질문은 아래 버튼을 눌러서 확인해보세요!'
		else:
			answer_list = MA(content)
			# answer_list = {'action':action, 'company':company, 'who':who, 'res':str(res), 'url':url}
			if 'action' in answer_list:
				# action = 1: 채용공고 질문
				# action = 2: 채용절차 질문
				# action = 3: 채용문의
				# action = 0: 예외 처리
				if answer_list['action'] == 1:
					if answer_list['company'] == None and int(answer_list['res']) > 0:
						answer = '네, 현재 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다. \n'
					elif int(answer_list['res']) > 0:
						answer = '네, 현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다. \n'
					elif answer_list['company'] == None:
						answer = '현재 '+answer_list['who']+'채용공고가 없습니다. \n'
					else:
						answer = '현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 없습니다. \n'
				elif answer_list['action'] == 2:
					answer = answer_list['process']
				elif answer_list['action'] == 3:
					answer = '현재 1:1질문은 로그인상태에서만 가능합니다 :-( \n 자주묻는질문은 아래 버튼을 눌러서 확인해보세요!'
				elif answer_list['action'] == 0:
					answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-( \n저는 아직 LG채용 관련 내용만 답변드릴 수 있어요. \n오탈자나 띄어쓰기를 확인해주시고 다시 말씀해주세요.'
				else:
					answer = '????ㅇㅅㅇ????'
			else:
				answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-( \n저는 아직 LG채용 관련 내용만 답변드릴 수 있어요. \n오탈자나 띄어쓰기를 확인해주시고 다시 말씀해주세요.'

		if 'url' in answer_list:
			if answer_list['url'] != None:
				return JsonResponse({
							'message':{
								"user_key": "encryptedUserKey",
								'text': answer,
								'message_button':{
									'label': '공식홈에서 확인하기',
									'url': answer_list['url']
								}
							},
							'keyboard':{
								'type':'buttons',
								'buttons':[ 
									chr(0x2753)+' 어떤 기능이 있나요?',
									chr(0x2753)+' 기능 이용할래요!',
									chr(0x2753)+' 문의할게 있어요.'
								]
							}
						})
			else:
				return JsonResponse({
							'message':{
								"user_key": "encryptedUserKey",
								'text': answer
							},
							'keyboard':{
								'type':'buttons',
								'buttons':[ 
									chr(0x2753)+' 어떤 기능이 있나요?',
									chr(0x2753)+' 기능 이용할래요!',
									chr(0x2753)+' 문의할게 있어요.'
								]
							}
						})
		else:
			return JsonResponse({
						'message':{
							"user_key": "encryptedUserKey",
							'text': answer
						},
						'keyboard':{
							'type':'buttons',
							'buttons':[ 
								chr(0x2753)+' 어떤 기능이 있나요?',
								chr(0x2753)+' 기능 이용할래요!',
								chr(0x2753)+' 문의할게 있어요.'
							]
						}
					})
	else:
		return False