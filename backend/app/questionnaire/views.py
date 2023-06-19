from questionnaire import serializers, services

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class QuestionnaireView(APIView):
    def _start_session(self):
        session_state = services.start_session(self.request.user)
        skip_answered_question = services.get_skip_answered_question(session_state.session)
        serializer = serializers.SessionSkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _get_session_state(self, session_id):
        services.check_session_not_over(session_id)
        session_state = services.get_session_state(session_id)
        skip_answered_question = services.get_skip_answered_question(session_state.session)
        serializer = serializers.SkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _get_next_question(self, session_id):
        session = services.get_session(session_id)
        question = services.get_question(session)
        services.update_session_state(session, question)
        skip_answered_question = services.get_skip_answered_question(session)
        serializer = serializers.SkipAnsweredQuestionSerializer(skip_answered_question)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _get_titles(self, session_id):
        result_titles = services.get_titles(session_id)
        data = services.get_titles_full_info(result_titles)
        services.write_result_titles_to_history(self.request.user, session_id, result_titles)
        return Response(data=data, status=status.HTTP_200_OK)

    def get(self, request, session_id=None, *args, **kwargs):
        if session_id:
            return self._get_session_state(session_id)
        return self._start_session()

    def post(self, request, *args, **kwargs):
        session, answer = services.check_questionnaire_post_data(**request.data)
        services.write_result(session, answer)
        if services.is_end(session.id):
            return self._get_titles(session.id)
        return self._get_next_question(session.id)

    def delete(self, request, session_id, *args, **kwargs):
        services.stop_session(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
