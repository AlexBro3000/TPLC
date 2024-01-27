from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from SemanticAnalysis.SemanticAnalysis import Semantic
from CodeGenerator.CodeGenerator import Generator


f = open('Test/temp.txt')
txt = f.read()


print("Лексический анализ:")
lexer = None
result_lexer = None
try:
    print("- Инициализация лексера")
    lexer = Lexer()
    print("- Лексический анализ: запущен")
    result_lexer = lexer.tokenization(txt)
except Exception as exp:
    print("- Лексический анализ: прерван")
    print("- * ERROR:", exp)
    lexer = None
    result_lexer = None
else:
    print("- Лексический анализ: завершон")
    # print("Результат:")
    # print(" ", result_lexer, "\n")
finally:
    print()
    print()
    print()


print("Cинтаксический анализ:")
parser = None
result_parser = None
try:
    if lexer is None and result_lexer is None:
        print("- Cинтаксический анализ: прерван")
    else:
        print("- Инициализация парсера")
        parser = Parser(lexer)
        print("- Cинтаксический анализ: запущен")
        result_parser = parser.parsing()
except Exception as exp:
    print("- Cинтаксический анализ: прерван")
    print("- * ERROR:", exp)
    parser = None
    result_parser = None
else:
    print("- Cинтаксический анализ: завершон")
    # print("Результат:")
    # print(result_parser.syntax_tree("  "), "\n")
finally:
    print()
    print()
    print()


print("Cемантический анализ:")
semantic = None
result_semantic = None
try:
    if parser is None and result_parser is None:
        print("- Cемантический анализ: прерван")
    else:
        print("- Инициализация семантического анализатора")
        semantic = Semantic(result_parser)
        print("- Cемантический анализ: запущен")
        result_semantic = semantic.semantic
except Exception as exp:
    print("- Cемантический анализ: прерван")
    print("- * ERROR:", exp)
    semantic = None
    result_semantic = None
else:
    print("- Cемантический анализ: завершон")
    print("Результат:")
    for semantic in result_semantic:
        print(
            f"  {semantic['type']}::{semantic['message']}\n  ::{semantic['identifier']}"
        )
finally:
    print()
    print()
    print()


print("Генератор кода:")
generator = None
result_generator = None
try:
    print("- Инициализация генератора")
    generator = Generator(result_parser)
    print("- Генерация кода: запущен")
    result_generator = generator.generate()
except Exception as exp:
    print("- Генерация кода: прерван")
    print("- * ERROR:", exp)
    generator = None
    result_generator = None
else:
    print("- Генерация кода: завершон")
    print("Результат:")
    print("\n".join("  " + line for line in result_generator.splitlines()))
finally:
    pass
