import re
from typing import List

class MathExpressionFinder:
    # Класс для поиска математических выражений в тексте и файлах

    # Регулярное выражение для поиска математических выражений
    MATH_EXPRESSION_PATTERN = re.compile(
        r'''
                (                                 
                    (?:                           
                        [-+]?                      
                        \s*                        
                        (?:                        
                            \d+(?:\.\d+)?          # Только числа
                            |                      
                            \(                     # Скобки с математическим содержимым
                                \s*[-+]?\s*\d+(?:\.\d+)?          # Число
                                (?:\s*[-+*/%]\s*[-+]?\s*\d+(?:\.\d+)?)+  # Операторы с числами
                                \s*
                            \)                     
                        )
                        (?:                        # Операторы с операндами
                            \s*                    
                            [-+*/%]                
                            \s*                      
                            [-+]?                  
                            \s*                    
                            (?:                    
                                \d+(?:\.\d+)?      # Число
                                |                  
                                \(                 # Скобки с математическим содержимым
                                    \s*[-+]?\s*\d+(?:\.\d+)?
                                    (?:\s*[-+*/%]\s*[-+]?\s*\d+(?:\.\d+)?)+
                                    \s*
                                \)                 
                            )
                        )+                         
                    )
                )                                  
                ''', re.VERBOSE
    )

    @classmethod
    def is_valid_expression(cls, expression: str) -> bool:
        expression = expression.strip()

        # Проверка на пустую строку
        if not expression:
            return False

        # Проверка на посторонние символы
        allowed_chars = set('0123456789.+-*/%() \t\n')
        if any(char not in allowed_chars for char in expression):
            return False

        # Проверяем баланс скобок
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()

        if stack:
            return False

        # Проверка структуры
        cleaned = expression.replace(' ', '')

        # Пустые скобки
        if '()' in cleaned:
            return False

        # Не может заканчиваться оператором
        if cleaned and cleaned[-1] in '+-*/%':
            return False

        # Не может иметь оператор перед закрывающей скобкой
        if re.search(r'[-+*/%]\)', cleaned):
            return False

        # Не может иметь два оператора подряд (кроме унарных)
        if re.search(r'[+*/%][+*/%]', cleaned):
            return False

        # Проверка деления на ноль
        if '/0' in cleaned:
            return False


        return True

    @classmethod
    def find_in_text(cls, text: str) -> List[str]:
        # Находит все математические выражения в тексте

        if not text:
            return []

        potential_matches = cls.MATH_EXPRESSION_PATTERN.findall(text)
        valid_expressions = []

        for match in potential_matches:
            match = match.strip()
            # Дополнительная проверка для выражений со скобками
            if cls.is_valid_expression(match):
                valid_expressions.append(match)

        return valid_expressions

    @classmethod
    def find_in_file(cls, filename: str) -> List[str]:
        # Находит математические выражения в файле

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return cls.find_in_text(content)

        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден")
            return []
        except UnicodeDecodeError:
            print(f"Ошибка: Не удалось декодировать файл '{filename}'")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

def main():
    # Основная функция для взаимодействия с пользователем

    print("*=== Поиск математических выражений ===*")

    while True:
        print("\n1. Проверить ваше выражение")
        print("2. Найти выражения в файле")
        print("3. Выйти")

        choice = input("Ваш выбор (1-3): ").strip()

        if choice == '1':
            expression = input("Введите математическое выражение: ").strip()
            if MathExpressionFinder.is_valid_expression(expression):
                print("✓ Выражение корректно")
            else:
                print("✗ Выражение некорректно")

        elif choice == '2':
            filename = input("Введите имя файла: ").strip()
            expressions = MathExpressionFinder.find_in_file(filename)

            if expressions:
                print(f"\nНайдено {len(expressions)} выражений:")
                for i, expr in enumerate(expressions, 1):
                    print(f"{i}. {expr}")
            else:
                print("\nВыражения не найдены")

        elif choice == '3':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
