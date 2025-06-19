def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов параметров функции
        annotations = func.__annotations__

        # Проверяем позиционные аргументы
        for i, (arg_name, expected_type) in enumerate(annotations.items()):
            if arg_name == 'return':
                continue  # Пропускаем аннотацию возвращаемого значения
            if i < len(args):
                arg_value = args[i]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be {expected_type.__name__}, not {type(arg_value).__name__}")

        # Проверяем именованные аргументы
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations and annotations[arg_name] != 'return':
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be {expected_type.__name__}, not {type(arg_value).__name__}")

        # Вызываем исходную функцию
        return func(*args, **kwargs)

    return wrapper




# Декоратор получает аннотации типов параметров функции из func.__annotations__
# Для каждого позиционного аргумента проверяется, соответствует ли его тип аннотированному типу.
# Если тип не совпадает, вызывается исключение TypeError
# Для каждого именованного аргумента проверяется его тип по аннотации.
# Если тип не совпадает, также вызывается исключение TypeError.
# Пример работы:

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))  # Выведет: 3
print(sum_two(1, 2.4))  # Вызовет TypeError: Argument 'b' must be int, not float