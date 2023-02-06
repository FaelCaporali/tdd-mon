import sys
from signal import SIGINT, signal
from src.chore.signal_handler import exit_handler
from src.chore.args_parse import parser
from src.file_handling.collect_test_files import collect_test_files
from src.chore.monitor import monitor
from src.chore.trigger_test import trigger_test
from src.file_handling.read_doc import read_doc


def main():
    try:
        tests_dir, test_file = parser(sys.argv)

        signal(SIGINT, exit_handler)

        sc_read = read_doc(sys.argv[1])
        if test_file is False:
            tests_files = collect_test_files(tests_dir)
            for file in tests_files:
                trigger_test(file)
                first_read = read_doc(file)
                monitor(first_read, file)
            monitor(sc_read, sys.argv[1], tests_dir)
        else:
            path = f"{tests_dir}/{test_file}"
            first_read = read_doc(path)
            trigger_test(path)
            monitor(first_read, path)
            monitor(sc_read, sys.argv[1], path)

    except FileNotFoundError:
        raise FileNotFoundError(
            "Não foi encontrado o caminho.\n"
            "tdd-monitor somente cria arquivos.\n"
            "Tem certeza que os diretórios existem nos locais especificados?"
        )
    except ImportError:
        raise UserWarning(
            "Nenhum arquivo de teste neste diretório\n"
            "crie ao menos um arquivo de teste!"
        )
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    print(read_doc("runner/src/templates/welcome.txt"), file=sys.stdout)
    main()
