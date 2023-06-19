from questionnaire import models

from rest_framework import serializers


# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Answer
#         fields = (
#             'id',
#             'body',
#         )


# class QuestionSerializer(serializers.ModelSerializer):
#     answers = serializers.SerializerMethodField('get_answers')

#     class Meta:
#         model = models.Question
#         fields = (
#             'body',
#             'answers',
#         )

#     def get_answers(self, obj):
#         return AnswerSerializer(obj.answer.all(), many=True).data


# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Session
#         fields = (
#             'id',
#         )


# class StartedSessionSerializer(serializers.Serializer):
#     # question = QuestionSerializer(read_only=True)

#     # class Meta:
#     #     model = models.SessionState
#     #     fields = (
#     #         'session',
#     #         'question',
#     #     )

#     session = serializers.SerializerMethodField('get_session')
#     question = serializers.SerializerMethodField('get_question')

#     def get_session(self, obj):
#         return obj.session.id

#     def get_question(self, obj):
#         question = QuestionSerializer(obj.question)
#         skip_answer = AnswerSerializer(obj.skip_answer)
#         question.data['answers'].append(skip_answer.data)
#         return question.data


# class SessionStateSerializer(serializers.ModelSerializer):
#     question = QuestionSerializer(read_only=True)

#     class Meta:
#         model = models.SessionState
#         fields = (
#             'question',
#         )


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
    # session = serializers.SerializerMethodField('get_session')
    question = serializers.SerializerMethodField('get_question')

    # def get_session(self, obj):
    #     return obj.session.id

    def get_question(self, obj):
        question = QuestionSerializer(obj.question)
        skip_answer = AnswerSerializer(obj.skip_answer)
        question.data['answers'].append(skip_answer.data)
        return question.data


class SessionSkipAnsweredQuestionSerializer(SkipAnsweredQuestionSerializer):
    session = serializers.SerializerMethodField('get_session')

    def get_session(self, obj):
        return obj.session.id
