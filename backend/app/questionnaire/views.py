from questionnaire import serializers, services

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from titles.serializers import TitleSerializer


class QuestionnaireView(APIView):
    def get_serializer_class(self):
        pass

    def _start_session(self):
        session = services.start_session(self.request.user.id)
        serializer = serializers.SessionSerializer(session)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def _get_session_state(self, session_id):
        session_state = services.get_session_state(session_id)
        serializer = serializers.SessionStateSerializer(session_state)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        session_id = request.data.get('session', None)
        return self._get_session_state(session_id) if session_id else self._start_session()

    def post(self, request, *args, **kwargs):
        # print('\n\n1\n\n')
        session_id = services.write_result(**request.data)
        if services.is_end(session_id=session_id):
            titles = services.get_titles(session_id)
            services.stop_session(session_id)
            serializer = TitleSerializer(titles, many=True)
            response_status_code = status.HTTP_200_OK
        else:
            question = services.get_next_question(session_id)
            serializer = serializers.QuestionSerializer(question)
            response_status_code = status.HTTP_201_CREATED
        return Response(data=serializer.data, status=response_status_code)

    def delete(self, request, session_id, *args, **kwargs):
        services.stop_session(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
