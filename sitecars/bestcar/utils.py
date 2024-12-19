from typing import Dict, Any
from bestcar.constants import MENU


class DataMixin:
    """
    Mixin для добавления общей информации (например, заголовка страницы и меню)
    в контекст представлений.
    """

    title_page: str = None

    def get_mixin_context(self, context: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Обновляет контекст с дополнительной информацией: заголовком страницы и меню.
        """
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = MENU

        context.update(kwargs)

        return context
