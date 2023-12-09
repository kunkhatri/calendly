class CalendlyBaseException(Exception):
    pass


class ObjectNotFoundException(CalendlyBaseException):
    pass

class BadRequestException(CalendlyBaseException):
    pass

class InvalidValueException(CalendlyBaseException):
    pass

class UnknownTimezoneException(CalendlyBaseException):
    pass
