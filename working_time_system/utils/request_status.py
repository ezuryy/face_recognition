import enum


class RequestStatus(enum.Enum):
    ok = 'Одобрено'
    canceled = 'Отказано'
    sent = 'Не просмотрено'
