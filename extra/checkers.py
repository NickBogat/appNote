from callbacks import *


class Checker:
    def __init__(self):
        pass

    def check_valid_number(self, tender: str):
        if len(tender) < 2 or tender[0] not in ("=", "-"):
            raise BadMoneyAmount("Неверный формат суммы!")
        _available = "0123456789"
        sign = tender[0]
        tender = tender[1:]
        for i in range(len(tender)):
            if tender[i] not in _available:
                raise BadMoneyAmount("Неверный формат суммы!")
        return True

    def check_valid_category(self, tender: str):
        if len(tender) < 3:
            raise BadCategoryName("Невеный формат категории!")
        if tender.isdigit():
            raise BadCategoryName("Невеный формат категории!")
        return True

    def check_valid_post_argument(self, argument: str):
        __argument = argument.split()
        if len(__argument) < 2:
            return False
        try:
            __number = __argument[0]
            __category = " ".join(__argument[1:])
            self.check_valid_number(__number)
            self.check_valid_category(__category)
            return int(__number), __category
        except BadMoneyAmount as er:
            return False
        except BadCategoryName as er:
            return False
