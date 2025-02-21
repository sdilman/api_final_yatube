class SerializerInitializationException(Exception):
    """Исключение для некорректно инициализированного сериализатора."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
