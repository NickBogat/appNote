from PyQt5.QtWidgets import QErrorMessage


class ProgramExceptions(Exception):
    pass


class BadArgument(ProgramExceptions):
    pass


class BadMoneyAmount(ProgramExceptions):
    pass


class BadCategoryName(ProgramExceptions):
    pass


class LoginAlreadyExists(ProgramExceptions):
    pass


class BadEnterData(ProgramExceptions):
    pass


def show_error_box(er):
    error_dialog = QErrorMessage()
    error_dialog.showMessage(er)
