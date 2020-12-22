from rest_framework import serializers
from .models import Answercount




# 챗봇답변
class AnswercountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answercount
        fields= '__all__'