from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import AnswercountSerializer
from .models import Answercount, IntentModel, Preprocess, Grocery
import pymysql
import re
import pandas as pd
import time
import requests
import json
import random
from .import load





# 음성 답변 검색
# 받는 값 : email
# 만든이 : jr
def AnswerGroceryCount(email, query):
    start = time.time()
    # 전처리 객체 생성 (load.py)
    # 의도 파악
    # intent = IntentModel(model_name='./bigdata/chatbot/intent_model_21.h5', proprocess=p)
    predict = load.pre_intent.intent.predict_class(query)
    intent_name = load.pre_intent.intent.labels[predict]
    print('시간1', time.time() - start)
    # 개체명 인식 (향후 추가 예정)
    # from models.ner.NerModel import NerModel
    # ner = NerModel(model_name='../models/ner/ner_model.h5', proprocess=p)
    # predicts = ner.predict(query)
    # ner_tags = ner.predict_tags(query)

    print("질문 : ", query)
    print("=" * 100)
    print("의도 파악 : ", intent_name)
    # print("개체명 인식 : ", predicts)
    # print("답변 검색에 필요한 NER 태그 : ", ner_tags)
    print("=" * 100)

    start3 = time.time()
    # 답변 검색
    answer = Answercount.objects.values_list('answer').filter(email=email, intent=intent_name)
    if not answer:
        answer = "현재 냉장고 속에 존재하지 않습니다."
    else:
        answer = answer[0][0]

    print("답변 : ", answer)
    print('시간3', time.time() - start3)
    print('총시간', time.time()-start)
    return answer


# 챗봇 재료 개수 답변 검색
# 받는 값 : query
# 만든이 : jr
@api_view(['GET'])
def AnswerCountGet(request):
    email = request.GET.get('email')
    query = request.GET.get('query')
    # Answercount_queryset = Answercount.objects.all()
    # serializers = AnswercountSerializer(Answercount_queryset, many=True)
    # 빅데이터 함수 호출(삽입)
    result = AnswerGroceryCount(email,query)
    print('result : ', result)
    print('---------end--------')
    return Response({"result":result})


# 챗봇 답변 저장
# 받는 값 : email
# 만든이 : jr
def SaveGroceryCount(email):
    start = time.time()
    # 현재 식재료 받아오기
    grocery_name = Grocery.objects.filter(email=email).values_list('name', 'count')
    print('grocery_name',grocery_name)
    now_grocery_dict = {}

    # 현재 식재료별 개수 dictionary 생성
    for grocery in grocery_name:
        # 향후 DB 저장 형식이 동일 식재료는 1행으로 저장될 경우 if문 삭제가능
        if grocery[0] in now_grocery_dict.keys():
            total_count = now_grocery_dict[grocery[0]] + grocery[1]
            now_grocery_dict.update({grocery[0]: total_count})
        else:
            now_grocery_dict.update({grocery[0]: grocery[1]})
    print('now_grocery_dict',now_grocery_dict)
    print('시간1', time.time()-start)

    start2 = time.time()
    # email, 의도, 재료개수 dict형식 list 생성
    answer_dict_list = []
    intent_list = list(now_grocery_dict.keys())
    count_list = list(now_grocery_dict.values())
    for i in range(len(now_grocery_dict)):
        answer_dict = {'email' : email, 'intent': intent_list[i] + '개수', 'answer': count_list[i]}
        answer_dict_list.append(answer_dict)

    # DB삭제
    answer_grocery_count = Answercount.objects.filter(email=email)
    answer_grocery_count.delete()
    print('시간2', time.time() - start2)
    start3 = time.time()

    for answer in answer_dict_list:
        # 데이터 저장
        serializer = AnswercountSerializer(data=answer)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return False
    print('시간3', time.time() - start3)
    print('최종시간', time.time() - start)
    return True

# 챗봇 답변 저장(list)
# 받는 값 : email
# 만든이 : jr
@api_view(['POST'])
def SaveCountGet(request):

    # email = request.GET.get('email')
    data = request.data
    email = data['email']
    # Answercount_queryset = Answercount.objects.filter(email=email)
    # serializers = AnswercountSerializer(Answercount_queryset, many=True)

    # 빅데이터 함수 호출(삽입)
    result = SaveGroceryCount(email)
    print('result : ', result)
    if result:
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    print('---------end--------')
    return Response({"result : ", result})