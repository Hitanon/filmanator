from questionnaire import serializers, services

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class QuestionnaireView(APIView):
    def _start_session(self):
        session = services.start_session(self.request.user.id)
        session_state = services.get_session_state(session.id)
        serializer = serializers.StartedSessionSerializer(session_state)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _get_session_state(self, session_id):
        services.check_session_not_over(session_id)
        session_state = services.get_session_state(session_id)
        serializer = serializers.SessionStateSerializer(session_state)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _get_titles(self, session_id):
        result_titles = services.get_titles(session_id)
        services.stop_session(session_id)
        services.write_result_titles_to_history(self.request.user, session_id, result_titles)
        serializer = serializers.SelectedTitlesSerializer(result_titles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _get_next_question(self, session_id):
        question = services.get_next_question(session_id)
        serializer = serializers.QuestionSerializer(question)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, session_id=None, *args, **kwargs):
        return self._get_session_state(session_id) if session_id else self._start_session()

    def post(self, request, *args, **kwargs):
        session, answer = services.check_questionnaire_post_data(**request.data)
        services.write_result(session.id, answer.id)
        return self._get_titles(session.id) if services.is_end(session.id) else self._get_next_question(session.id)

    def delete(self, request, session_id, *args, **kwargs):
        services.stop_session(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
