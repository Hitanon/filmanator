from questionnaire import serializers, services

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class QuestionnaireView(APIView):
    def _start_session(self):
        session = services.start_session(self.request.user)
        skip_answered_question = services.get_skip_answered_question(session)
        serializer = serializers.SessionSkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _get_session_state(self, session):
        services.check_session_not_over(session)
        skip_answered_question = services.get_skip_answered_question(session)
        serializer = serializers.SkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _get_finished_session_titles(self, session):
        data = services.get_finished_session_titles_data(session)
        data = services.get_titles_full_info(data)
        return Response(data=data, status=status.HTTP_200_OK)

    def _get_next_question(self, session):
        services.update_session_state(session)
        skip_answered_question = services.get_skip_answered_question(session)
        serializer = serializers.SkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _select_titles(self, session):
        titles = services.select_session_titles(session)
        services.write_result_titles_to_history(self.request.user, session, titles)
        services.write_result_to_session(session, titles)
        data = services.get_titles_full_info(titles)
        return Response(data=data, status=status.HTTP_200_OK)

    def get(self, request, session_id=None, *args, **kwargs):
        if not session_id:
            return self._start_session()
        session = services.get_session(session_id)
        if session.is_finished:
            return self._get_finished_session_titles(session)
        return self._get_session_state(session)

    def post(self, request, *args, **kwargs):
        session = services.check_session_id(**request.data)
        answer = services.check_answer_id(**request.data)
        services.check_is_author(session, request.user)
        if session.is_finished:
            return self._get_finished_session_titles(session)

        services.write_result(session, answer)
        if services.is_end(session):
            return self._select_titles(session)
        return self._get_next_question(session)

    def delete(self, request, session_id, *args, **kwargs):
        session = services.get_session(session_id)
        services.delete_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)
