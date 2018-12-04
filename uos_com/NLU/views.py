#-*- coding:utf-8 -*-

from django.shortcuts import render
from konlpy.tag import Mecab
from urllib.parse import unquote
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from django.http import HttpResponse
display = None
browser = None
# Create your views here.
def getInput(input):
	return 0

def MA(input):
	global display, browser
	try:

		display = Display(visible=0, size=(1024,768))
		display.start()
		browser = webdriver.Chrome()
		browser.implicitly_wait(2)

		answer_list = {}
		input = unquote(input)
		input = input.upper()
		mecab = Mecab()
		morphs_list = mecab.morphs(input)

		# answer = '형태소분석결과:'
		new_morphs_list = []
		for i in morphs_list:
			# answer += i
			i = i.upper()
			i = i.replace(' ','')
			new_morphs_list.append(i)
			# answer +=' '
		# answer += '//'

		company = None
		who = None
		url = None
		process = None
		action = None
		# 키워드 추가
		for noun in new_morphs_list:
			# answer += noun
			# 액션 설정
			if action == None:
				if (noun=='채용공고')or(noun=='공고')or(noun=='일자리')or(noun=='자리'):# 채용공고
					action = 1
				elif (noun=='채용절차')or(noun=='절차')or(noun=='채용순서')or(noun=='방법')or(noun=='순서'):# 채용절차
					action = 2
				elif (noun=='채용문의')or(noun=='문의')or(noun=='질문')or(noun=='개선점')or(noun=='챗봇개선점'):# 채용문의
					action = 3
				else:
					action = None
			# 채용공고:회사
			if (noun=='LGCNS')or(noun=='CNS')or(noun=='씨엔에스')or\
				(noun=='LG전자')or(noun=='전자')or\
				(noun=='LG디스플레이')or(noun=='디스플레이')or(noun=='LG디플')or\
				(noun=='LG이노텍')or(noun=='이노텍')or\
				(noun=='LG화학')or(noun=='화학')or\
				(noun=='LG생활건강')or(noun=='생활건강')or\
				(noun=='LG유플러스')or(noun=='유플러스')or\
				(noun=='LG상사')or(noun=='상사'):
				company = noun
				if (noun=='LGCNS')or(noun=='CNS')or(noun=='씨엔에스'):
					company = 'LG CNS'

			# 채용공고:신입/경력/인턴
			if (noun=='신입')or(noun=='경력')or(noun=='인턴'):
				who = noun

		if action == None: action = 0


		# 채용공고 크롤링 처리
		if action == 1:
			if who == None:
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi',company,who)
				# answer += '전체검색결과: '
				who = ' '
				url = 'http://careers.lg.com/app/job/RetrieveJobNotices.rpi'

			elif who == '신입':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=A',company,who)
				# answer += '신입검색결과: '
				who += ' '
				url = 'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=A'
			elif who == '경력':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=B',company,who)
				# answer += '경력검색결과: '
				who += ' '
				url = 'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=B'
			elif who == '인턴':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=C',company,who)
				# answer += '인턴검색결과: '
				who += ' '
				url = 'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=C'
			else:
				res = 0
				# answer += '이건뭐냐: '
				answer += who

			answer_list = {'action':action, 'company':company, 'who':who, 'res':str(res), 'url':url}
			# if company == None and res > 0:
			# 	answer += '네, 현재 '+who+'채용공고가 '+str(res)+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
			# elif res > 0:
			# 	answer += '네, 현재 '+company+'에 대한 '+who+'채용공고가 '+str(res)+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
			# elif company == None:
			# 	answer += '현재 '+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
			# else:
			# 	answer += '현재 '+company+'에 대한'+who+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">>>채용공고확인하기<<</a><br>'
		# 채용공고
		# 1개이상: 네, 현재 LG CNS에 대한 n개의 공고가 있습니다. >>링크에서확인하기

		
		# 채용절차
		elif action == 2:
			if who == None:
				who = ''
				process = 'LG그룹은 각 사별 인재상을 기준으로 차별화된 채용 프로그램 및 기준에 의해 우수 인재를 선발합니다. \n\
				지원자의 과도한 개인정보를 받지 않으며, 전형상 불필요한 항목을 과감히 삭제하였습니다. \n\
				또한, 각 계열사마다 상이했던 입사지원서를 통일함으로써 사별 중복지원을 한다면 "입사지원서 불러오기"기능으로 보다 편리하게 지원이 가능합니다. \n\
				최대 3개의 중복지원이 가능하며, 중복지원시에 인적성검사는 한번만 치루시면 됩니다. \n\
				아래 버튼을 통해 관련 내용을 더 상세히 확인하실 수 있으며, 모집단위별 채용절차가 궁금하실때는 인턴/신입/경력 키워드를 넣어서 다시 질문해주세요.'
				url = 'http://careers.lg.com/app/careers/ViewSystem.rpi?requestMenuId=1441'

			elif who == '인턴':
				process = '인턴 프로그램 및 대학생 해외 탐방, 각종 공모전, 마케팅 세미나 등 다양한 체험 프로그램을 통해 LG에 입사할 수 있는 기회를 얻을 수 있습니다. \n\
				아래 버튼을 눌러서 각 사별 진행되는 인턴/체험 프로그램과 더불어 산학협력 프로그램과 해외인재 채용에 대해서 확인해보세요!'
				url = 'http://careers.lg.com/app/careers/ViewProgram.rpi'

			elif who == '신입':
				process = 'LG의 신입사원 공개채용은 다음과 같이 진행됩니다. \n\
				1. 지원서 접수 \n\
				2. 서류전형 \n\
				3. 인적성검사 \n\
				4. 면접전형 \n\
				5. 건강검진 \n\
				6. 최종합격 \n \n\
				다만 지원 회사 및 모집 분야에 따라서 세부적인 전형 절차와 방법이 달라질 수 있으므로 정확한 내용은 개별 채용공고를 확인해주세요.\n\
				(신입 공채의 경우 최대 3개사까지 중복지원이 가능합니다.)'
				url = 'http://careers.lg.com/app/careers/ViewProcedures.rpi'

			elif who == '경력':
				process = 'LG의 경력사원 채용은 필요 인력 발생 시 수시로 진행되며 일반적인 프로세스는 다음과 같습니다. \n\
				1. 지원서 접수 \n\
				2. 서류검토  \n\
				3. 인적성검사(필요시) \n\
				4. 면접전형 \n\
				5. 건강검진 \n\
				6. 처우협의 \n\
				7. 최종합격 \n \n\
				다만 지원 회사 및 모집 분야에 따라서 세부적인 전형 절차와 방법이 달라질 수 있으므로 정확한 내용은 개별 채용공고를 확인해주세요.'
				url = 'http://careers.lg.com/app/careers/ViewExperienced.rpi'

			else:
				who = ''
				process = 'LG그룹은 각 사별 인재상을 기준으로 차별화된 채용 프로그램 및 기준에 의해 우수 인재를 선발합니다. \n\
				지원자의 과도한 개인정보를 받지 않으며, 전형상 불필요한 항목을 과감히 삭제하였습니다. \n\
				또한, 각 계열사마다 상이했던 입사지원서를 통일함으로써 사별 중복지원을 한다면 "입사지원서 불러오기"기능으로 보다 편리하게 지원이 가능합니다. \n\
				최대 3개의 중복지원이 가능하며, 중복지원시에 인적성검사는 한번만 치루시면 됩니다. \n\
				아래 버튼을 통해 관련 내용을 더 상세히 확인하실 수 있으며, 모집단위별 채용절차가 궁금하실때는 인턴/신입/경력 키워드를 넣어서 다시 질문해주세요.'
				url = 'http://careers.lg.com/app/careers/ViewSystem.rpi?requestMenuId=1441'
			answer_list = {'action':action, 'who':who, 'url':url, 'process':process}
		# 채용문의
		elif action == 3:
			url = 'http://careers.lg.com/app/faq/RetrieveFaq.rpi?requestMenuId=1069'
			answer_list = {'action':action, 'url':url}
		# 예외
		else: #action == 0
			answer_list = {'action':0}


	finally:
		display.stop()
		browser.quit()
	
	return answer_list

def crawl(action, url, key1=None, key2=None, key3=None):
	global display, browser

	browser.get(url)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	if action == 1:
		res = 0
		company_list = soup.select('tbody > tr > td.companyName')
		who_list = soup.select('tbody > tr > td > span.applyAs')
		# 회사별, who별로 나눠야함
		if (key1 != None and key2 != None): # 회사, 지원방법 받았을 때
			for idx,company in enumerate(company_list):
				if key1 in company.text:
					if (key2 in who_list[idx].text) or ('무관' in who_list[idx].text):
						res += 1
		elif key1 != None:
			for company in company_list:
				if key1 in company.text:
					res += 1
		elif key2 != None:
			for who in who_list:
				if (key2 in who.text) or ('무관' in who.text):
					res += 1
		else:
			res = len(company_list) - 1
			
#LtableJobNoticesList > tbody > tr:nth-child(2) > td:nth-child(2) > span
	return res

def displayStart(request):
	global display, browser
	display = Display(visible=0, size=(1024,768))
	display.start()
	browser = webdriver.Chrome()
	browser.implicitly_wait(3)
	return HttpResponse('display start')

def displayStop(request):
	global display, browser
	display.stop()
	browser.quit()
	return HttpResponse('display stop')
