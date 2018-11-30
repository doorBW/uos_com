#-*- coding:utf-8 -*-

from django.shortcuts import render
from konlpy.tag import Komoran
from imp import reload
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
		browser.implicitly_wait(3)

		answer = ''
		input = unquote(input)
		input = input.upper()
		komoran = Komoran()
		nouns_list = komoran.nouns(input)

		for i in nouns_list:
			i = i.upper()
			i = i.replace(' ','')

		company = None
		who = None
		action = 0
		# 키워드 추가
		for noun in nouns_list:
			answer += noun
			# 액션 설정
			if (noun=='채용공고')or(noun=='공고')or(noun=='일자리')or(noun=='자리'):# 채용공고
				action = 1
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




		# 채용공고 크롤링 처리
		if action == 1:
			if who == None:
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi',company,who)
				answer += '전체검색결과: '
				who = ''
			elif who == '신입':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=A',company,who)
				answer += '신입검색결과: '
				who += ' '
			elif who == '경력':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=B',company,who)
				answer += '경력검색결과: '
				who += ' '
			elif who == '인턴':
				res = crawl(action,'http://careers.lg.com/app/job/RetrieveJobNotices.rpi?careerCode=C',company,who)
				answer += '인턴검색결과: '
				who += ' '
			else:
				res = 0
				answer += '이건뭐냐: '
				answer += who
			if company == None and res > 0:
				answer += '네, 현재 '+who+'채용공고가 '+res+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">\>\>채용공고확인하기\<\<</a><br>'
			elif res > 0:
				answer += '네, 현재 '+company+'에 대한 '+who+'채용공고가 '+res+'개 있습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">\>\>채용공고확인하기\<\<</a><br>'
			elif company == None:
				answer += '현재 '+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">\>\>채용공고확인하기\<\<</a><br>'
			else:
				answer += '현재 '+company+'에 대한'+who+'채용공고가 없습니다.<br><br><a href="http://careers.lg.com/app/job/RetrieveJobNotices.rpi">\>\>채용공고확인하기\<\<</a><br>'
		# 채용공고
		# 1개이상: 네, 현재 LG CNS에 대한 n개의 공고가 있습니다. >>링크에서확인하기

		
		# 채용절차

		# 채용문의

		# 기타프로그램

		# 예외
		answer += '/답변 끝'

	finally:
		display.stop()
		browser.quit()
	
	return answer

def crawl(action, url, key1=None, key2=None, key3=None):
	global display, browser

	browser.get(url)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	if action == 1:
		res = 0
		company_list = soup.select('tbody > tr > td.companyName')
		who_list = soup.select('tbody > tf > td > span.applyAs')
		# 회사별, who별로 나눠야함
		if (key1 != None and key2 != None): # 회사, 지원방법 받았을 때
			for company,idx in enumerate(company_list):
				if key1 in company:
					if key2 in who_list[idx]:
						res += 1
		elif key1 != None:
			for company in company_list:
				if key1 in company:
					res += 1
		elif key2 != None:
			for who in who_list:
				if key2 in who:
					res += 1
		else:
			res = len(company_list)
			
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
