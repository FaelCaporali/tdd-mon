import sys
import threading
from signal import SIGINT, signal
from src.chore.signal_handler import exit_handler
from file_handling.args.args_parse import parser


EXIT_EVENT = threading.Event()

if __name__ == "__main__":
    try:
        with open("src/out/welcome.txt") as welcome:
            print(welcome.read())
        sc_file, tests_dir, test_file = parser(sys.argv)

        signal(SIGINT, exit_handler)

    except IndexError:
        raise IndexError
    except FileNotFoundError:
        print("Não foi encontrado o caminho.")
        print("tdd-u.monitor somente cria arquivos")
        print(
            "Tem certeza que os diretórios existem nos locais especificados?"
        )
        raise FileNotFoundError
    except AssertionError:
        print(f"O teste falhou: {AssertionError}")
    except KeyboardInterrupt:
        sys.exit(0)
