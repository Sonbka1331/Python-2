

class BlockErrors:

    def __init__(self, errors):
        self.errors = errors

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if type in self.errors:
            return True


def test_ignore_error():
    err_blocked = {ZeroDivisionError}
    with BlockErrors(err_blocked):
        1 / 0
    print('Тест игнорирования ошибок выполнен успешно')


def test_error_throwing_up():
    outer_err_types = {TypeError}
    with BlockErrors(outer_err_types):
        inner_err_types = {ZeroDivisionError}
        with BlockErrors(inner_err_types):
            1 / '0'
        print('Ошибка во внутреннем блоке!')
    print('Тест игнорирования ошибки во внешнем блоке выполнен')


def test_error_not_ignore():
    errs = {TypeError}
    try:
        with BlockErrors(errs):
            1 / 0
        print('except zero division')
    except ZeroDivisionError:
        print('Тест игнорирования другой ошибки выполнен')


def test_all_inner_errors_ingnored():
    outer_errs = {TypeError}
    with BlockErrors(outer_errs):
        inner_err = {AttributeError}
        with BlockErrors(inner_err):
            1 / '0'
        print('Внутренняя ошибка')
    print('Тест игнорирования внутренней ошибки выполнен')


if __name__ == '__main__':
    test_ignore_error()
    test_error_throwing_up()
    test_error_not_ignore()
    test_all_inner_errors_ingnored()
