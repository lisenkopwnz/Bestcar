from bestcar.constants import *


class DataMixin:
    title_page = None

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['menu'] = MENU  # Предполагается, что MENU - это глобальная переменная
        context.update(kwargs)
        return context
