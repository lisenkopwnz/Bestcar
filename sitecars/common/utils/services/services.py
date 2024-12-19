def elasticsearch_formatting_date(date):
    """
        ‘орматирует дату в строку ISO 8601, подход¤щую дл¤ Elasticsearch.

        :param date: объект даты, который необходимо отформатировать.
        :return: строка, представл¤юща¤ дату в формате ISO 8601.
    """
    return date.isoformat()