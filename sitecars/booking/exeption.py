class SeatingError(Exception):
    """
        Пользовательское исклюяение свидетельствующие об отсутствии свободных мест при
        бронировании поездки.
    """

    def __init__(self, message='Похоже все места заняты'):
        self.message = message
        super().__init__(message)


