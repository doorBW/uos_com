from django.shortcuts import render, redirect, HttpResponse
import pandas as pd
import requests, json
import xmltodict
from django.views.decorators.csrf import csrf_exempt

apiKey = '201809507OAM40045'
home_url = 'http://uos-info.com'

# Create your views here.
def index(request):
    return render(request, 'canGraduate/canGraduate_index.html')

def error_page(request):
    return render(request,'canGraduate/error_page.html')

def canI(request):
    return render(request, 'canGraduate/canI_index.html')

@csrf_exempt
def checking_graduataion(request):
    try:
        result_message = {}
        result_message['major'] = {}
        if request.method == 'POST':
            major = request.POST['dept']
            english_test_name = request.POST['english_test_name']
            english_score = request.POST['english_score']
            print("@@", english_test_name)
            # 과별 필요한 값
            if major =='전자전기컴퓨터공학부':
                deptDiv = '23100'
                dept = 'A200110111'
                subDept = 'A200160116'

            # 성적표 불러오기
            grade_card_file = request.FILES['grade_card']
            grade_card = pd.read_excel(grade_card_file,header=0)

            # 총 취득 학점 인덱스
            total_score_idx = list(grade_card['NO']).index('총누계')

            # 필요한 데이터 리스트화
            year_list = list(grade_card['학년도'])
            term_list = list(grade_card['학기'])
            subjectNo_list = list(grade_card['교과번호'])
            subject_list = list(grade_card['교과목명'])
            subjectDiv_list = list(grade_card['교과구분'])
            score_list = list(grade_card['학점'])
            grade_list = list(grade_card['등급'])

            # 교과목명 공백지우기
            for i,v in enumerate(subject_list):
                subject_list[i] = v.replace(" ","")
                
            # 총 취득 학점
            total_score = int(term_list[total_score_idx])

            # 총 평점 평균
            total_grade_avg = float(score_list[total_score_idx])
            major_grade_avg = float(score_list[total_score_idx-4])
            non_major_grade_avg = float(score_list[total_score_idx-3])

            # 0. 영어 성적
            # 영어영문학과 / 사회계열 / 인문계열 / 자연,공학계열()
            # 자연 및 공학계열
            if major == '전자전기컴퓨터공학부':
                if english_test_name == 'TOEIC':
                    if int(english_score) >= 650:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 650점 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'TOEFL(PBT)':
                    if int(english_score) >= 533:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 533점 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'TOEFL(CBT)':
                    if int(english_score) >= 200:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 200점 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'TOEFL(IBT)':
                    if int(english_score) >= 73:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 73점 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'TEPS':
                    if int(english_score) >= 526:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 526점 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'IELTS':
                    end_point = float(english_score[4:])
                    english_score = float(english_score[0:3])
                    if english_score >= 6.0:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}~{2}등급으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score,end_point)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}~{2}등급으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 6.0등급 이상입니다.'.format(english_test_name,english_score,end_point)
                
                elif english_test_name == 'TOEIC Speaking':
                    end_point = int(english_score[4:])
                    english_score = int(english_score[0:3])
                    if english_score >= 120:
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}~{2}점으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score,end_point)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}~{2}점으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 120점 이상입니다.'.format(english_test_name,english_score,end_point)
                
                elif english_test_name == 'TEPS Speaking':
                    if (english_score == '1+') or (english_score == '1') or (english_score == '2+') or (english_score == '2') or (english_score == '3+') or (english_score == '3'):
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}등급으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}등급으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 3등급 이상입니다.'.format(english_test_name,english_score)
                
                elif english_test_name == 'OPIc':
                    if (english_score == 'AL') or (english_score == 'IH') or (english_score == 'IM') or (english_score == 'IL'):
                        result_message['english_result'] = 1
                        result_message['english'] = '공인 영어시험, {0}을 {1}등급으로 졸업자격 기준을 만족하셨습니다.'.format(english_test_name,english_score)
                    else:
                        result_message['english_result'] = 0
                        result_message['english'] = '공인 영어시험, {0}을 {1}등급으로 졸업자격 기준을 만족하지 못했습니다.\n{0}시험의 자연 및 공학계열의 졸업기준은 3등급 이상입니다.'.format(english_test_name,english_score)

                elif english_test_name == 'none':
                    result_message['english_result'] = 2
                    result_message['english'] = '공인 영어시험을 일정 기준점수 이상으로 취득하셔야 합니다. 각 공인 영어시험별 기준 점수는 아래 이미지와 같습니다.(출처: 서울시립대학교 공식홈페이지)'

            # 1. 총 취득 학점 130 이상
            if total_score >= 130:
                result_message['total_score_result'] = 1
                result_message['total_score'] = '총 취득 학점은 {0}학점으로 졸업기준을 채웠습니다.'.format(total_score)
            else:
                result_message['total_score_result'] = 0
                result_message['total_score'] = '총 취득 학점은 {0}학점으로 {1}학점을 더 채우셔야 합니다.'.format(total_score, 130-total_score)

            # 2. 평점 평균 2.0 이상
            if total_grade_avg >= 2.0:
                result_message['total_grade_avg_result'] = 1
                result_message['total_grade_avg'] = '전공 평균 {0}, 교양 평균 {1}, 총 평점 평균{2}점으로 졸업기준을 만족하였습니다.'.format(major_grade_avg,non_major_grade_avg,total_grade_avg)
            else:
                result_message['total_grade_avg_result'] = 0
                result_message['total_grade_avg'] = '전공 평균 {0}, 교양 평균 {1}, 총 평점 평균{2}점으로 졸업기준을 만족하지 못했습니다.'.format(major_grade_avg,non_major_grade_avg,total_grade_avg)

            # 전전컴 졸업 이수 기준
            # 3. 실습과목(마이크로프로세서응용실습, 소프트웨어시스템실습, 초고주파공학실습, 통신공학실습) 1개
            for i in ['마이크로프로세서응용실습','소프트웨어시스템실습','초고주파공학실습','통신공학실습']:
                # i 과목이 수강과목에 있는지 확인하기
                if i in subject_list:
                    practice_course_idx = subject_list.index(i)
                    # F 등급이 아니면 됨
                    practice_course_grade = grade_list[practice_course_idx]
                    if not practice_course_grade == 'F':
                        result_message['major']['practice_course_result'] = 1
                        result_message['major']['practice_course'] = '{0} 수업을 {1}등급으로 수강하셔서 실습과목 이수를 만족하셨습니다.'.format(i,practice_course_grade)
                        break
                    else:
                        result_message['major']['practice_course_result'] = 0
                        result_message['major']['practice_course'] = '{0} 수업을 {1}등급으로 수강하셔서 실습과목 이수를 만족하지 못했습니다.'.format(i,practice_course_grade)
                elif i == '통신공학실습':
                    result_message['major']['practice_course_result'] = 0
                    result_message['major']['practice_course'] = '실습과목 수업을 수강하지 않으셔서 실습과목 이수를 만족하지 못했습니다.\n{0}, {1}, {2}, {3} 과목중 하나를 이수하시길 바랍니다.'.format('마이크로프로세서응용실습','소프트웨어시스템실습','초고주파공학실습','통신공학실습')

            # 4. 전공심화 32학점
            selective_major_subject = []
            idx = -1
            for i in subjectDiv_list:
                if i == '전공선택':
                    idx = subjectDiv_list.index(i,idx+1)
                    selective_major_subject.append(subject_list[idx])
            selective_major_subject_total_score = 0
            for i in selective_major_subject:
                year = year_list[subject_list.index(i)]
                term = term_list[subject_list.index(i)]
                term_code = 'A10'
                if term == '2학기':
                    term_code = 'A20'
                subjectNo = subjectNo_list[subject_list.index(i)]
                params = {
                    'apiKey': apiKey,
                    'year': year,
                    'term': term_code,
                    'deptDiv': deptDiv,
                    'dept': dept,
                    'subDept': subDept,
                    'subjectNo': subjectNo
                }
                res = requests.get('http://wise.uos.ac.kr/uosdoc/api.ApiUcrMjTimeInq.oapi', params=params)
                res_dict = xmltodict.parse(res.text)
                if type(res_dict['root']['mainlist']['list']) == list:
                    one_subject = res_dict['root']['mainlist']['list'][0]
                else:
                    one_subject = res_dict['root']['mainlist']['list']
                grade_num = int(one_subject['shyr'])
                if grade_num == 4:
                    selective_major_subject_total_score += int(one_subject['credit'])
                elif grade_num == 3:
                    if one_subject['term'] == 'A20':
                        selective_major_subject_total_score += int(one_subject['credit'])
            if selective_major_subject_total_score >= 32:
                result_message['major']['selective_major_score_result'] =  1
                result_message['major']['selective_major_score'] = '전공심화 과목을 {0}학점 수강하셔서 전공심화과목학점 이수조건(32학점)을 만족하셨습니다.'.format(selective_major_subject_total_score)
            else:
                result_message['major']['selective_major_score_result'] = 0
                result_message['major']['selective_major_score'] = '전공심화 과목을 {0}학점 수강하셔서 전공심화과목학점 이수조건(32학점)을 만족하지 못했습니다.'.format(selective_major_subject_total_score)

            # 5. 공학소양=haveTo_non_major_a 2학점
            # 6. 자연과기술(자연공학)=haveTo_non_major_b 3학점
            # 7. 문학과예술2(인문사회)=haveTo_non_major_c 3학점
            haveTo_non_major_a = 0
            haveTo_non_major_b = 0
            haveTo_non_major_c = 0
            selective_non_major_subject = []
            idx = -1
            for i in subjectDiv_list:
                if i == '교양선택':
                    idx = subjectDiv_list.index(i,idx+1)
                    selective_non_major_subject.append(subject_list[idx])

            for i in selective_non_major_subject:
                year = year_list[subject_list.index(i)]
                term = term_list[subject_list.index(i)]
                if grade_list[subject_list.index(i)] == "F":
                    continue
                term_code = 'A10'
                if term == '2학기':
                    term_code = 'A20'
                subjectNo = subjectNo_list[subject_list.index(i)]
                params = {
                    'apiKey': apiKey,
                    'year': year,
                    'term': term_code,
                    'subjectDiv': 'A01',
                    'subjectNm':i
                }
                res = requests.get('http://wise.uos.ac.kr/uosdoc/api.ApiUcrCultTimeInq.oapi', params=params)
                res_dict = xmltodict.parse(res.text)
                try:
                    if type(res_dict['root']['mainlist']['list']) == list:
                        one_subject = res_dict['root']['mainlist']['list'][0]
                    else:
                        one_subject = res_dict['root']['mainlist']['list']
                except:
                    continue
                subjectSubDiv = one_subject['subject_div2']
                if subjectSubDiv == '공학소양':
                    haveTo_non_major_a += int(one_subject['credit'])
                elif subjectSubDiv == '자연과기술' or subjectSubDiv == '자연·공학':
                    haveTo_non_major_b += int(one_subject['credit'])
                elif subjectSubDiv == '문학과예술2' or subjectSubDiv == '인문·사회':
                    haveTo_non_major_c += int(one_subject['credit'])
            # 공학소양
            if haveTo_non_major_a >= 2:
                result_message['major']['haveTo_non_major_a_result'] = 1
                result_message['major']['haveTo_non_major_a'] = '공학소양 학점을 {0}학점 수강하셔서 졸업요건(2학점)을 만족하였습니다.'.format(haveTo_non_major_a)
            else:
                result_message['major']['haveTo_non_major_a_result'] = 0
                result_message['major']['haveTo_non_major_a'] = '공학소양 학점을 {0}학점 수강하셔서 졸업요건(2학점)을 만족하지 못했습니다.'.format(haveTo_non_major_a)
            # 자연공학
            if haveTo_non_major_b >= 3:
                result_message['major']['haveTo_non_major_b_result'] = 1
                result_message['major']['haveTo_non_major_b'] = '자연공학 학점을 {0}학점 수강하셔서 졸업요건(3학점)을 만족하였습니다.'.format(haveTo_non_major_b)
            else:
                result_message['major']['haveTo_non_major_b_result'] = 0
                result_message['major']['haveTo_non_major_b'] = '자연공학 학점을 {0}학점 수강하셔서 졸업요건(3학점)을 만족하지 못했습니다.'.format(haveTo_non_major_b)
            # 인문사회
            if haveTo_non_major_c >= 3:
                result_message['major']['haveTo_non_major_c_result'] = 1
                result_message['major']['haveTo_non_major_c'] = '인문사회 학점을 {0}학점 수강하셔서 졸업요건(3학점)을 만족하였습니다.'.format(haveTo_non_major_c)
            else:
                result_message['major']['haveTo_non_major_c_result'] = 0
                result_message['major']['haveTo_non_major_c'] = '인문사회 학점을 {0}학점 수강하셔서 졸업요건(3학점)을 만족하지 못했습니다.'.format(haveTo_non_major_c)
                
            # print(result_message)
        else:
            return redirect(home_url+'/error')
    except:
        return redirect(home_url+'/error')
    return render(request, 'canGraduate/canI_result.html', result_message)


def temp(request):
    return HttpResponse('temp site OK')
