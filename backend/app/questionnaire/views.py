from questionnaire import serializers, services

from titles.serializers import TitleSerializer
from titles.services import get_titles

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
        if session_id:
            return self._get_session_state(session_id)
        else:
            return self._start_session()

    def post(self, request, *args, **kwargs):
        services.check_session_id(**request.data)
        services.write_result(**request.data)
        session_id = int(request.data['session'])
        # print('\n\n1\n\n')
        is_end = services.is_end(session_id=session_id)
        response_status_code = None
        if is_end:
            titles = get_titles()
            serializer = TitleSerializer(titles, many=True)
            response_status_code = status.HTTP_200_OK
        else:
            question = services.get_next_question(session_id)
            serializer = serializers.QuestionSerializer(question)
            response_status_code = status.HTTP_201_CREATED
        return Response(data=serializer.data, status=response_status_code)
        # return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
