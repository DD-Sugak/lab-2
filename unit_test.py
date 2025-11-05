import unittest
from LAba2 import MathExpressionFinder


#Тесты скомпилированного регулярного выражения
class TestMathExpressionRegex(unittest.TestCase):
    def setUp(self):
        self.MATH_EXPRESSION_PATTERN = MathExpressionFinder.MATH_EXPRESSION_PATTERN

    def test_matches_valid_format(self):
        test_cases = [
            "2 + 2",
            "3 * 4",
            "10 - 5",
            "15 / 3",
            "20 % 6"
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                matches = self.MATH_EXPRESSION_PATTERN.findall(test_case)
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0].strip(), test_case)

    def test_matches_valid_format_in_text(self):
        text_samples = [
            ("Выражение: 2 + 2", ["2 + 2"]),
            ("Результаты: 3 * 4 и 10 - 5", ["3 * 4", "10 - 5"]),
            ("Выражения: 2 + 2, 3 * 4, 10 - 5", ["2 + 2", "3 * 4", "10 - 5"]),
            ("Здесь выражений нет", []),
            ("Смешанно: 2 + 2 и просто текст", ["2 + 2"]),
        ]

        for text, expected in text_samples:
            with self.subTest(text=text):
                matches = self.MATH_EXPRESSION_PATTERN.findall(text)
                matches_clean = [match.strip() for match in matches]
                self.assertEqual(matches_clean, expected)

    def test_reject_invalid_format(self):
        test_cases = [
            "2 +",           #неполное выражение
            "+ 3",           #неполное выражение
            "abc + 3",       #буквы
            "2 . 3",         #неправильный оператор
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                matches = self.MATH_EXPRESSION_PATTERN.findall(test_case)
                self.assertEqual(len(matches), 0)

    def test_boundary_cases(self):
        test_cases = [
            ("2 + 3 + 4", True),           #сложное выражение
            ("-5 + 10", True),             #унарный минус
            ("+8 - 3", True),              #унарный плюс
            ("3.14 * 2", True),            #дробные числа
            ("2 +", False),                #неполное
            ("+ 3", False),                #неполное
        ]

        for test_case, should_match in test_cases:
            with self.subTest(test_case=test_case):
                matches = self.MATH_EXPRESSION_PATTERN.findall(test_case)
                if should_match:
                    self.assertEqual(len(matches), 1)
                else:
                    self.assertEqual(len(matches), 0)

#Тесты для выражений со скобками
class TestMathExpressionWithParentheses(unittest.TestCase):

    def setUp(self):
        self.MATH_EXPRESSION_PATTERN = MathExpressionFinder.MATH_EXPRESSION_PATTERN

    def test_finds_expressions_inside_parentheses(self):
        # Тест, что находит математические выражения внутри скобок
        test_cases = [
            ("(2 + 2)", True),  # Должно найти "2 + 2"
            ("(3 * 4)", True),  # Должно найти "3 * 4"
            ("2 * (3 + 4)", True),  # Должно найти "3 + 4"
            ("(5 + 3) * 2", True),  # Должно найти "5 + 3"
            ("((2 + 3))", True),  # Должно найти "2 + 3"
        ]

        for expression, should_find in test_cases:
            with self.subTest(expression=expression):
                matches = self.MATH_EXPRESSION_PATTERN.findall(expression)
                if should_find:
                    self.assertTrue(len(matches) > 0,
                                    f"Не найдено совпадений для: {expression}")
                else:
                    self.assertEqual(len(matches), 0,
                                     f"Найдены лишние совпадения для: {expression}")

    def test_finds_parentheses_expressions_in_text(self):
        # Тест поиска выражений со скобками в тексте
        text_samples = [
            ("Выражение: (2 + 2) = 4", True),  # Должно найти
            ("Результаты: (3 * 4) и (10 - 5)", True),  # Должно найти
            ("Текст без выражений", False),  # Не должно найти
        ]

        for text, should_find in text_samples:
            with self.subTest(text=text):
                matches = self.MATH_EXPRESSION_PATTERN.findall(text)
                if should_find:
                    self.assertTrue(len(matches) > 0)
                else:
                    self.assertEqual(len(matches), 0)

    def test_does_not_find_empty_parentheses(self):
        # Тест, что не находит пустые или некорректные скобки
        test_cases = [
            "()",  # Пустые скобки
            "(+)",  # Только оператор
            "(abc)",  # Буквы в скобках
        ]

        for expression in test_cases:
            with self.subTest(expression=expression):
                matches = self.MATH_EXPRESSION_PATTERN.findall(expression)
                self.assertEqual(len(matches), 0,
                                 f"Найдены совпадения для некорректного выражения: {expression}")

    def test_debug_what_regex_finds(self):
        # Простой тест для отладки - что находит регулярное выражение
        debug_cases = [
            "(2 + 2)",
            "2 * (3 + 4)",
            "((2 + 3))",
            "(2 +",
        ]

        for expression in debug_cases:
            with self.subTest(expression=expression):
                matches = self.MATH_EXPRESSION_PATTERN.findall(expression)

#Тест функций библиотеки re
class TestFormatCompilation(unittest.TestCase):
    def setUp(self):
        self.MATH_EXPRESSION_PATTERN = MathExpressionFinder.MATH_EXPRESSION_PATTERN

    #Проверка на то, что MATH_EXPRESSION_PATTERN - скомпилированный
    def test_format_type(self):
        from re import Pattern
        self.assertIsInstance(self.MATH_EXPRESSION_PATTERN, Pattern)

    #Проверка методов формата
    def test_format_methods(self):
        text = "Выражения: 2 + 2 и 3 * 4"

        matches = self.MATH_EXPRESSION_PATTERN.findall(text)
        self.assertEqual(len(matches), 2)

        search_result = self.MATH_EXPRESSION_PATTERN.search(text)
        self.assertIsNotNone(search_result)

        matches = list(self.MATH_EXPRESSION_PATTERN.finditer(text))
        self.assertEqual(len(matches), 2)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestMathExpressionRegex))
    suite.addTests(loader.loadTestsFromTestCase(TestMathExpressionWithParentheses))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatCompilation))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    run_tests()