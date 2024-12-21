from django.http import JsonResponse
from django.views import View


class BaseView(View):
    """ ������� ����� ������� ����������� ��� ���������� ,�������
        �� ���� ���������� �����
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response(e, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        """����������� HTTP ����� � �������� ������ ��� ��������� JSON ����� � ������ ������������� """
        if status != 200:
            res = JsonResponse({
                "errorMessage": str(data),
                "status": status
            })
        else:
            res = JsonResponse({
                "data": str(data),
                "status": status
            })
        return res