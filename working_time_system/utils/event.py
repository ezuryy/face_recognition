import enum


class Event(enum.Enum):
    weekend = 'Выходной'
    turnout = 'Явка'
    vacation = 'Отпуск'
    business_trip = 'Командировка'
    sick = 'Больничный'
    strike = 'Забастовка'
