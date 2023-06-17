from questionnaire import models

from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = (
            'id',
            'body',
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        model = models.Question
        fields = (
            'body',
            'answers',
        )

    def get_answers(self, obj):
        return AnswerSerializer(obj.answer.all(), many=True).data


class StartedSessionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = models.SessionState
        fields = (
            'session',
            'question',
        )


class SessionStateSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = models.SessionState
        fields = (
            'question',
        )


# class SelectedTitlesSerializer(serializers.Serializer):
#     match_percentage = serializers.IntegerField()
    # length = serializers.IntegerField()
    # titles = serializers.SerializerMethodField('get_titles')

    # def get_titles(self, obj):
    #     return obj['titles']
    # id = serializers.IntegerField()
