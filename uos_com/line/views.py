from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt    #포스트 에러 방지
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

#load env
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
# Load file from the path.
load_dotenv(dotenv_path)

channel_access_token = os.getenv('channel_access_token')
line_bot_api = LineBotApi(channel_access_token)

@csrf_exempt
def webhook(request):
    print(request)
    return HttpResponse('webhook OK')

@csrf_exempt
def broadcast(request):
    try:
        line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
    except LineBotApiError as e:
        print(e)
    return HttpResponse('broadcast OK')

@csrf_exempt
def broadcast_sise(request):
    try:
        line_bot_api.broadcast(TextSendMessage(text='Hello World!(TODO SISE)'))
    except LineBotApiError as e:
        print(e)
    return HttpResponse('broadcast_sise OK')