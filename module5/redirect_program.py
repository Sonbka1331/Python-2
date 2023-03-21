import sys
import traceback


class Redirect:

    def __init__(self, stdout_file=None, stderr_file=None):
        self.out_console = sys.stdout
        self.stdout = stdout_file
        self.err_console = sys.stderr
        self.stderr = stderr_file

    def __enter__(self):
        if self.stdout is not None:
            sys.stdout = self.stdout
        if self.stderr is not None:
            sys.stderr = self.stderr

    def __exit__(self, type, value, tb):
        sys.stdout = self.out_console
        sys.stderr = self.err_console
        if type in {Exception}:
            try:
                self.stderr.write(traceback.format_exc())
            except AttributeError:
                return False
            if self.stdout is not None:
                self.stdout.close()
            if self.stderr is not None:
                self.stderr.close()
            return True


stdout_file = open('stdout.txt', 'w')
stderr_file = open('stderr.txt', 'w')


def test_writer():
    print('Начало теста')
    with Redirect(stdout_file, stderr_file):
        print('Hello stdout')
        raise Exception('Hello stderr')

    print('Ошибка и вывод записаны по файлам')
    raise Exception('Ошибка выведена в консоль')


def test_writer_without_error():
    with Redirect(stdout_file=stdout_file):
        print('Запись файла')

    print('Вывод в консоль')


def test_writer_without_print():
    with Redirect(stderr_file=stderr_file):
        raise Exception('Вывод в текстовый файл')

    raise Exception('Предыдущая ошибка записана в файл')


def test_without_args():
    with Redirect():
        print('Вывод в консоль')
        raise Exception('Ошибка выведена в консоль')


if __name__ == '__main__':
    # test_writer()
    # test_writer_without_error()
    # test_writer_without_print()
    test_without_args()
