from django.shortcuts import render
from django.http import HttpResponse
from NLU.views import MA
# Create your views here.
def index(request):
	return 0

def getInput(request,input):
	answer_list = MA(input)
	if 'action' in answer_list:
		# action = 1: 채용공고 질문
		# action = 2: 채용절차 질문
		# action = 3: 채용문의
		# action = 0: 예외 처리
		if answer_list['action'] == 1:

			if 'company' not in answer_list and int(answer_list['res']) > 0:
				answer = '네, 현재 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			elif int(answer_list['res']) > 0:
				answer = '네, 현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			elif 'company' not in answer_list:
				answer = '현재 '+answer_list['who']+'채용공고가 없습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			else:
				answer = '현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 없습니다.<br><br><a href="'+answer_list['res']+'">>>채용공고확인하기<<</a><br>'
		elif answer_list['action'] == 2:
			answer_list['process'] = answer_list['process'].replace('\n','<br>')
			answer = answer_list['process']
		elif answer_list['action'] == 3:
			answer = '현재 1:1질문은 로그인상태에서만 가능합니다 :-( <br>자주묻는질문은 아래 버튼을 눌러서 확인해보세요!'
		elif answer_list['action'] == 0:
			answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-( <br>저는 아직 LG채용 관련 내용만 답변드릴 수 있어요. <br>오탈자나 띄어쓰기를 확인해주시고 다시 말씀해주세요.'
		else:
			answer = '????ㅇㅅㅇ????'
	else:
		answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-(<br>저는 아직 LG채용 관련 내용만 답변드릴 수 있어요.<br>오탈자나 띄어쓰기를 확인해주시고 다시 말씀해주세요.'
	return HttpResponse(answer)