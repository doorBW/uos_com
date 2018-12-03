from django.shortcuts import render
from django.http import HttpResponse
from NLU.views import MA
# Create your views here.
def index(request):
	return 0

def getInput(request,input):
	answer_list = MA(input,1)
	if 'action' in answer_list:
		# answer_list = {'action':action, 'company':company, 'who':who, 'res':str(res), 'url':url}
		# 	# if company == None and res > 0:
		# 	# 	answer += '네, 현재 '+who+'채용공고가 '+str(res)+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
		# 	# elif res > 0:
		# 	# 	answer += '네, 현재 '+company+'에 대한 '+who+'채용공고가 '+str(res)+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
		# 	# elif company == None:
		# 	# 	answer += '현재 '+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
		# 	# else:
		# 	# 	answer += '현재 '+company+'에 대한'+who+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
		if answer_list['action'] == 1:
			if 'company' not in answer_list and int(answer_list['res']) > 0:
				answer = '네, 현재 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			elif int(answer_list['res']) > 0:
				answer = '네, 현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 '+answer_list['res']+'개 있습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			elif 'company' not in answer_list:
				answer = '현재 '+answer_list['who']+'채용공고가 없습니다.<br><br><a href="'+answer_list['url']+'">>>채용공고확인하기<<</a><br>'
			else:
				answer = '현재 '+answer_list['company']+'에 대한 '+answer_list['who']+'채용공고가 없습니다.<br><br><a href="'+answer_list['res']+'">>>채용공고확인하기<<</a><br>'
		else:
			answer = '???'
	else:
		answer = '미안해요. 무슨 말씀이신지 이해하지 못하겠어요 :-(<br>저는 아직 LG채용 관련 내용만 답변드릴 수 있어요.<br>오탈자나 띄어쓰기를 확인해주시고, 불편사항이 있으시다면 "챗봇 개선점"이라고 말씀해주세요.'
	return HttpResponse(answer)