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
        answers = AnswerSerializer(obj.answer.all(), many=True)
        return answers.data


class SessionStateSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = models.SessionState
        fields = (
            'id',
            'question',
        )


class SkipAnsweredQuestionSerializer(serializers.Serializer):
    question = serializers.SerializerMethodField('get_question')

    def get_question(self, obj):
        question = QuestionSerializer(obj.question)
        if obj.skip_answer:
            skip_answer = AnswerSerializer(obj.skip_answer)
            question.data['answers'].append(skip_answer.data)
        return question.data


class SessionSkipAnsweredQuestionSerializer(SkipAnsweredQuestionSerializer):
    session = serializers.SerializerMethodField('get_session')

    def get_session(self, obj):
        return obj.session.id


class ResultTitleSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = models.ResultTitle
        fields = (
            'id',
            'match_percentage',
        )

    def get_id(self, obj):
        return obj.title.id
