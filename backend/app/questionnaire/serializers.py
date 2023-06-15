from questionnaire import models

from rest_framework import serializers


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = (
            'id',
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = (
            'id',
            'body',
        )


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = (
            'id',
            'body',
            'answer',
        )


class SessionStateSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = models.SessionState
        fields = (
            'id',
            'question',
        )
