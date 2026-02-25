class InvalidStatusTransition(Exception):
    """Erro lançado quando uma transição de status não é permitida."""
    pass


class UnknownStatusError(Exception):
    """Erro lançado quando um status desconhecido é utilizado."""
    pass