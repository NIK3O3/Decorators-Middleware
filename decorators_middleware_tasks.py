from __future__ import annotations

import argparse
import time
from functools import reduce, wraps
from typing import Any, Callable, Iterable, TypeVar


T = TypeVar("T")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Допоміжні функції
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def is_number(value: Any) -> bool:
    """bool не рахуємо числом, хоча технічно bool наслідується від int."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ---------------------------------------------------------------------------
# Завдання 1. Функція, що повертає функцію
# ---------------------------------------------------------------------------

def outer() -> Callable[[], None]:
    def inner() -> None:
        print("Hello from inner")

    return inner


def task_1_function_returns_function() -> None:
    print_header("Завдання 1. Функція, що повертає функцію")

    result = outer()
    print(f"Результат outer(): {result}")
    result()

    print(
        "\nПояснення:\n"
        "- У Python функція є об'єктом першого класу: її можна зберігати у змінній, "
        "передавати як аргумент і повертати з іншої функції.\n"
        "- outer() повертає функцію inner, а не викликає її.\n"
        "- Це приклад функції вищого порядку, бо outer працює з іншою функцією "
        "як зі значенням."
    )


# ---------------------------------------------------------------------------
# Завдання 2. Ручне обгортання функції
# ---------------------------------------------------------------------------

def greet_task_2(name: str) -> str:
    return f"Hello, {name}"


def wrapper_task_2(func: Callable[[str], str]) -> Callable[[str], str]:
    def inner(name: str) -> str:
        print("Before function call")
        result = func(name)
        print("After function call")
        return result

    return inner


def task_2_manual_wrapping() -> None:
    print_header("Завдання 2. Ручне обгортання функції")

    wrapped_greet = wrapper_task_2(greet_task_2)
    result = wrapped_greet("Anna")

    print(f"Результат: {result}")
    print(
        "\nПояснення:\n"
        "- wrapper приймає функцію greet і повертає нову функцію inner.\n"
        "- Нова функція виконує додаткові дії до та після виклику greet.\n"
        "- Поведінка оригінальної функції змінюється без зміни її коду."
    )


# ---------------------------------------------------------------------------
# Завдання 3. Декоратор логування
# ---------------------------------------------------------------------------

def logger(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result

    return inner


@logger
def square_logged(x: int) -> int:
    return x * x


@logger
def add_logged(a: int, b: int) -> int:
    return a + b


@logger
def greet_logged(name: str) -> str:
    return f"Hello, {name}"


def task_3_logger_decorator() -> None:
    print_header("Завдання 3. Декоратор логування")

    square_logged(5)
    add_logged(10, 15)
    greet_logged("Oleh")


# ---------------------------------------------------------------------------
# Завдання 4. Декоратор вимірювання часу
# ---------------------------------------------------------------------------

def timer(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"Function {func.__name__} executed in {end_time - start_time:.6f} seconds")
        return result

    return inner


@timer
def slow_sum(n: int) -> int:
    total = 0

    for i in range(n):
        total += i

    return total


def task_4_timer_decorator() -> None:
    print_header("Завдання 4. Декоратор вимірювання часу")

    for n in [10_000, 100_000, 500_000]:
        result = slow_sum(n)
        print(f"slow_sum({n}) = {result}")


# ---------------------------------------------------------------------------
# Завдання 5. Декоратор перевірки аргументу
# ---------------------------------------------------------------------------

def positive_only(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R | str:
        values = list(args) + list(kwargs.values())

        for value in values:
            if is_number(value) and value <= 0:
                return "Error: all numeric arguments must be positive"

        return func(*args, **kwargs)

    return inner


@positive_only
def multiply(a: int, b: int) -> int:
    return a * b


def task_5_positive_only() -> None:
    print_header("Завдання 5. Декоратор перевірки аргументу")

    print(f"multiply(2, 3) = {multiply(2, 3)}")
    print(f"multiply(-2, 3) = {multiply(-2, 3)}")
    print(
        "\nПояснення:\n"
        "- Декоратор positive_only перехоплює виклик функції.\n"
        "- Перед виконанням multiply він перевіряє числові аргументи.\n"
        "- Якщо аргумент недодатний, оригінальна функція не викликається."
    )


# ---------------------------------------------------------------------------
# Завдання 6. Декоратор для *args і **kwargs
# ---------------------------------------------------------------------------

def debug_args(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print(f"Function: {func.__name__}")
        print(f"Positional args: {args}")
        print(f"Keyword args: {kwargs}")

        return func(*args, **kwargs)

    return inner


@debug_args
def no_args_function() -> str:
    return "No arguments"


@debug_args
def positional_function(a: int, b: int) -> int:
    return a + b


@debug_args
def greet_with_prefix(name: str, prefix: str = "Hello") -> str:
    return f"{prefix}, {name}"


def task_6_args_kwargs_decorator() -> None:
    print_header("Завдання 6. Декоратор для *args і **kwargs")

    print(no_args_function())
    print(positional_function(3, 7))
    print(greet_with_prefix("Anna", prefix="Hi"))


# ---------------------------------------------------------------------------
# Завдання 7. Декоратор збереження метаданих
# ---------------------------------------------------------------------------

def decorator_without_wraps(func: Callable[..., R]) -> Callable[..., R]:
    def wrapper(*args: Any, **kwargs: Any) -> R:
        return func(*args, **kwargs)

    return wrapper


def decorator_with_wraps(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        return func(*args, **kwargs)

    return wrapper


@decorator_without_wraps
def original_without_wraps() -> str:
    """Функція без збереження метаданих."""
    return "without wraps"


@decorator_with_wraps
def original_with_wraps() -> str:
    """Функція зі збереженням метаданих."""
    return "with wraps"


def task_7_wraps_metadata() -> None:
    print_header("Завдання 7. Декоратор збереження метаданих")

    print(f"original_without_wraps.__name__ = {original_without_wraps.__name__}")
    print(f"original_with_wraps.__name__ = {original_with_wraps.__name__}")

    print(
        "\nПояснення:\n"
        "- Без functools.wraps ім'я декорованої функції стає wrapper.\n"
        "- wraps копіює важливі метадані: __name__, __doc__, __module__ тощо.\n"
        "- Це потрібно для логування, документації, тестів, дебагу і фреймворків."
    )


# ---------------------------------------------------------------------------
# Завдання 8. Параметризований декоратор
# ---------------------------------------------------------------------------

def repeat(n: int) -> Callable[[Callable[..., R]], Callable[..., R | None]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R | None]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> R | None:
            result: R | None = None

            for _ in range(n):
                result = func(*args, **kwargs)

            return result

        return inner

    return decorator


@repeat(3)
def say_hi() -> None:
    print("Hi")


def task_8_parameterized_decorator() -> None:
    print_header("Завдання 8. Параметризований декоратор")

    say_hi()

    print(
        "\nПояснення:\n"
        "- repeat(3) спочатку приймає параметр n.\n"
        "- Потім повертає справжній decorator, який приймає функцію.\n"
        "- Тому потрібна додаткова вкладеність: repeat -> decorator -> inner."
    )


# ---------------------------------------------------------------------------
# Завдання 9. Параметризований логер
# ---------------------------------------------------------------------------

def log_with_prefix(prefix: str) -> Callable[[Callable[..., R]], Callable[..., R]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> R:
            print(f"[{prefix}] Calling function: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[{prefix}] Result: {result}")
            return result

        return inner

    return decorator


@log_with_prefix("INFO")
def run_info_task() -> str:
    return "Done"


@log_with_prefix("WARNING")
def run_warning_task() -> str:
    return "Something may be wrong"


@log_with_prefix("ERROR")
def run_error_task() -> str:
    return "Something failed"


def task_9_parameterized_logger() -> None:
    print_header("Завдання 9. Параметризований логер")

    run_info_task()
    run_warning_task()
    run_error_task()


# ---------------------------------------------------------------------------
# Завдання 10. Проста middleware-обгортка
# ---------------------------------------------------------------------------

def middleware(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print("Before request")
        result = func(*args, **kwargs)
        print("After request")
        return result

    return inner


def handle_request_task_10() -> str:
    return "OK"


def task_10_simple_middleware() -> None:
    print_header("Завдання 10. Проста middleware-обгортка")

    wrapped_handle_request = middleware(handle_request_task_10)
    result = wrapped_handle_request()

    print(f"Result: {result}")
    print(
        "\nПояснення:\n"
        "- Middleware стоїть між викликом клієнта і реальною обробкою запиту.\n"
        "- Воно може виконати код до запиту, передати керування далі й виконати код після запиту."
    )


# ---------------------------------------------------------------------------
# Завдання 11. Middleware для авторизації
# ---------------------------------------------------------------------------

def require_auth(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(user: dict[str, Any], *args: Any, **kwargs: Any) -> R | str:
        if user.get("authenticated") is not True:
            return "Access denied"

        return func(user, *args, **kwargs)

    return inner


@require_auth
def dashboard(user: dict[str, Any]) -> str:
    return f"Welcome, {user['name']}"


def task_11_auth_middleware() -> None:
    print_header("Завдання 11. Middleware для авторизації")

    authorized_user = {"name": "Anna", "authenticated": True}
    unauthorized_user = {"name": "Petro", "authenticated": False}

    print(f"Authorized:   {dashboard(authorized_user)}")
    print(f"Unauthorized: {dashboard(unauthorized_user)}")


# ---------------------------------------------------------------------------
# Завдання 12. Middleware для обробки помилок
# ---------------------------------------------------------------------------

def handle_errors(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R | str:
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return f"Friendly error: {type(error).__name__}: {error}"

    return inner


@handle_errors
def divide(a: float, b: float) -> float:
    return a / b


def task_12_error_handling_middleware() -> None:
    print_header("Завдання 12. Middleware для обробки помилок")

    print(f"divide(10, 2) = {divide(10, 2)}")
    print(f"divide(10, 0) = {divide(10, 0)}")


# ---------------------------------------------------------------------------
# Завдання 13. Комбінування декораторів
# ---------------------------------------------------------------------------

@logger
@timer
@positive_only
def process_data(x: int) -> int:
    return x * 2


def task_13_combining_decorators() -> None:
    print_header("Завдання 13. Комбінування декораторів")

    print("Виклик process_data(5):")
    process_data(5)

    print("\nВиклик process_data(-5):")
    process_data(-5)

    print(
        "\nПояснення порядку:\n"
        "- Декоратори застосовуються знизу вгору: спочатку positive_only, потім timer, потім logger.\n"
        "- Під час виклику виконання йде зверху вниз: logger -> timer -> positive_only -> process_data.\n"
        "- positive_only може зупинити виклик оригінальної функції, якщо аргумент некоректний."
    )


# ---------------------------------------------------------------------------
# Завдання 14. Побудова middleware-ланцюжка вручну
# ---------------------------------------------------------------------------

def log_request_middleware(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print("log_request: request received")
        result = func(*args, **kwargs)
        print("log_request: response sent")
        return result

    return inner


def authorize_middleware(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(user: dict[str, Any], *args: Any, **kwargs: Any) -> R | str:
        if user.get("authenticated") is not True:
            return "Access denied"

        return func(user, *args, **kwargs)

    return inner


def handle_request_task_14(user: dict[str, Any]) -> str:
    if user.get("force_error"):
        raise RuntimeError("Unexpected request error")

    return f"Request handled for {user['name']}"


def task_14_manual_middleware_chain() -> None:
    print_header("Завдання 14. Побудова middleware-ланцюжка вручну")

    chain = handle_errors(
        log_request_middleware(
            authorize_middleware(
                handle_request_task_14
            )
        )
    )

    users = [
        {"name": "Anna", "authenticated": True},
        {"name": "Petro", "authenticated": False},
        {"name": "ErrorUser", "authenticated": True, "force_error": True},
    ]

    for user in users:
        print(f"\nUser: {user}")
        print(chain(user))


# ---------------------------------------------------------------------------
# Завдання 15. Rate limiting
# ---------------------------------------------------------------------------

def limit_calls(n: int) -> Callable[[Callable[..., R]], Callable[..., R | str]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R | str]:
        calls = 0

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> R | str:
            nonlocal calls

            if calls >= n:
                return "Call limit exceeded"

            calls += 1
            return func(*args, **kwargs)

        return inner

    return decorator


@limit_calls(3)
def ping() -> str:
    return "pong"


def task_15_rate_limiting() -> None:
    print_header("Завдання 15. Rate limiting")

    for i in range(1, 6):
        print(f"Call {i}: {ping()}")

    print(
        "\nПояснення:\n"
        "- Лічильник calls зберігається у замиканні decorator.\n"
        "- Кожен виклик inner має доступ до того самого calls через nonlocal.\n"
        "- Після 3 успішних викликів функція повертає повідомлення про перевищення ліміту."
    )


# ---------------------------------------------------------------------------
# Завдання 16. Кешування результатів
# ---------------------------------------------------------------------------

def make_cache_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[Any, ...]:
    """
    Створює ключ кешу з позиційних та іменованих аргументів.
    Для простоти очікуємо, що всі аргументи hashable.
    """
    return args + tuple(sorted(kwargs.items()))


def simple_cache(func: Callable[..., R]) -> Callable[..., R]:
    cache: dict[tuple[Any, ...], R] = {}

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        key = make_cache_key(args, kwargs)

        if key in cache:
            print(f"Cache hit for {key}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return inner


@simple_cache
def cached_square(x: int) -> int:
    print("Calculating...")
    return x * x


def task_16_simple_cache() -> None:
    print_header("Завдання 16. Кешування результатів")

    print(f"cached_square(5) = {cached_square(5)}")
    print(f"cached_square(5) = {cached_square(5)}")
    print(f"cached_square(10) = {cached_square(10)}")
    print(f"cached_square(10) = {cached_square(10)}")


# ---------------------------------------------------------------------------
# Завдання 17. Middleware для валідації даних
# ---------------------------------------------------------------------------

def validate_name(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(data: dict[str, Any], *args: Any, **kwargs: Any) -> R | str:
        name = data.get("name")

        if name is None:
            return "Validation error: key 'name' is required"

        if not isinstance(name, str) or not name.strip():
            return "Validation error: name must be a non-empty string"

        return func(data, *args, **kwargs)

    return inner


@validate_name
def create_user(data: dict[str, Any]) -> str:
    return f"User {data['name']} created"


def task_17_validation_middleware() -> None:
    print_header("Завдання 17. Middleware для валідації даних")

    test_data = [
        {"name": "Anna"},
        {"name": ""},
        {"age": 20},
        {"name": "   "},
    ]

    for data in test_data:
        print(f"{data} -> {create_user(data)}")


# ---------------------------------------------------------------------------
# Завдання 18. Декоратор як чиста трансформація поведінки
# ---------------------------------------------------------------------------

def to_uppercase_result(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        result = func(*args, **kwargs)

        if isinstance(result, str):
            return result.upper()  # type: ignore[return-value]

        return result

    return inner


@to_uppercase_result
def greet_uppercase(name: str) -> str:
    return f"Hello, {name}"


@to_uppercase_result
def number_result() -> int:
    return 123


def task_18_functional_transformation() -> None:
    print_header("Завдання 18. Декоратор як чиста трансформація поведінки")

    print(f"greet_uppercase('Anna') = {greet_uppercase('Anna')}")
    print(f"number_result() = {number_result()}")

    print(
        "\nПояснення:\n"
        "- Декоратор можна розглядати як функцію, яка приймає функцію і повертає нову функцію.\n"
        "- Тобто це трансформація поведінки: old_function -> new_function.\n"
        "- to_uppercase_result не змінює тіло greet_uppercase, а змінює результат її виклику."
    )


# ---------------------------------------------------------------------------
# Завдання 19. Compose для декораторів
# ---------------------------------------------------------------------------

def compose_decorators(
    d1: Callable[[Callable[..., R]], Callable[..., R]],
    d2: Callable[[Callable[..., R]], Callable[..., R]],
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Поєднує два декоратори.

    compose_decorators(d1, d2)(func) еквівалентно:
        d1(d2(func))

    Тобто d2 застосовується до функції першим, а d1 стає зовнішнім декоратором.
    """
    def composed(func: Callable[..., R]) -> Callable[..., R]:
        return d1(d2(func))

    return composed


def decorator_a(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print("Decorator A: before")
        result = func(*args, **kwargs)
        print("Decorator A: after")
        return result

    return inner


def decorator_b(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print("Decorator B: before")
        result = func(*args, **kwargs)
        print("Decorator B: after")
        return result

    return inner


@compose_decorators(decorator_a, decorator_b)
def composed_function() -> str:
    print("Original function")
    return "Done"


def task_19_compose_decorators() -> None:
    print_header("Завдання 19. Compose для декораторів")

    result = composed_function()
    print(f"Result: {result}")


# ---------------------------------------------------------------------------
# Завдання 20. Functional Request Processing Engine
# ---------------------------------------------------------------------------

def engine_logger(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        print("[LOGGER] Request started")
        result = func(*args, **kwargs)
        print(f"[LOGGER] Response: {result}")
        print("[LOGGER] Request finished")
        return result

    return inner


def engine_require_auth(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(user: dict[str, Any], *args: Any, **kwargs: Any) -> R | str:
        if user.get("authenticated") is not True:
            return "Access denied"

        return func(user, *args, **kwargs)

    return inner


def engine_validate_positive(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(user: dict[str, Any], value: int | float, *args: Any, **kwargs: Any) -> R | str:
        if value <= 0:
            return "Validation error: value must be positive"

        return func(user, value, *args, **kwargs)

    return inner


def engine_handle_errors(func: Callable[..., R]) -> Callable[..., R | str]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R | str:
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return f"Handled error: {type(error).__name__}: {error}"

    return inner


def engine_timer(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"[TIMER] {func.__name__}: {end_time - start_time:.6f} seconds")
        return result

    return inner


def base_handle_request(user: dict[str, Any], value: int | float) -> str:
    if user.get("force_error"):
        raise RuntimeError("Internal processing error")

    return f"Processed value: {value}"


def build_request_engine(handler: Callable[..., R]) -> Callable[..., Any]:
    """
    Єдиний middleware-ланцюжок.

    Порядок застосування:
        engine_handle_errors(
            engine_logger(
                engine_timer(
                    engine_require_auth(
                        engine_validate_positive(handler)
                    )
                )
            )
        )

    Під час виконання виклик проходить ззовні всередину:
        handle_errors -> logger -> timer -> require_auth -> validate_positive -> handler
    """
    return engine_handle_errors(
        engine_logger(
            engine_timer(
                engine_require_auth(
                    engine_validate_positive(handler)
                )
            )
        )
    )


def task_20_functional_request_processing_engine() -> None:
    print_header("Завдання 20. Functional Request Processing Engine")

    engine = build_request_engine(base_handle_request)

    scenarios = [
        (
            "Авторизований користувач і коректні дані",
            {"name": "Anna", "authenticated": True},
            10,
        ),
        (
            "Неавторизований користувач",
            {"name": "Petro", "authenticated": False},
            10,
        ),
        (
            "Від'ємне значення",
            {"name": "Anna", "authenticated": True},
            -5,
        ),
        (
            "Помилка всередині функції",
            {"name": "ErrorUser", "authenticated": True, "force_error": True},
            10,
        ),
    ]

    for title, user, value in scenarios:
        print("\n" + "-" * 80)
        print(title)
        print(f"user = {user}")
        print(f"value = {value}")
        print(f"Result = {engine(user, value)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_selected_task(task_number: str) -> None:
    tasks: dict[str, Callable[[], None]] = {
        "1": task_1_function_returns_function,
        "2": task_2_manual_wrapping,
        "3": task_3_logger_decorator,
        "4": task_4_timer_decorator,
        "5": task_5_positive_only,
        "6": task_6_args_kwargs_decorator,
        "7": task_7_wraps_metadata,
        "8": task_8_parameterized_decorator,
        "9": task_9_parameterized_logger,
        "10": task_10_simple_middleware,
        "11": task_11_auth_middleware,
        "12": task_12_error_handling_middleware,
        "13": task_13_combining_decorators,
        "14": task_14_manual_middleware_chain,
        "15": task_15_rate_limiting,
        "16": task_16_simple_cache,
        "17": task_17_validation_middleware,
        "18": task_18_functional_transformation,
        "19": task_19_compose_decorators,
        "20": task_20_functional_request_processing_engine,
    }

    if task_number == "all":
        for number in map(str, range(1, 21)):
            tasks[number]()
        return

    if task_number not in tasks:
        available = ", ".join(["all"] + list(tasks.keys()))
        raise ValueError(f"Невідоме завдання: {task_number}. Доступні варіанти: {available}")

    tasks[task_number]()


def main() -> None:
    parser = argparse.ArgumentParser(description="Завдання з декораторів і middleware у Python")
    parser.add_argument(
        "--task",
        default="all",
        help="Номер завдання: 1..20 або all. За замовчуванням: all",
    )

    args = parser.parse_args()
    run_selected_task(args.task)


if __name__ == "__main__":
    main()
