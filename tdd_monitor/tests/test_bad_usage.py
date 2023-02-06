from tdd_monitor.src.main import main
import pytest
import sys
import os


def test_lack_of_args():
    """Without args or broken ones, should return usage instructions"""

    """Calling without any path pointed
    """
    with pytest.raises(
        IndexError,
        match="Invalid arguments!\n"
        "Usage:\n"
        "python3 tdd-monitor.py /path/to/tested/file.py  /path/to/test/file",
    ):
        sys.argv = ["tdd-mon"]
        main()

    """Calling without file ending
    """
    with pytest.raises(
        IndexError,
        match="Invalid arguments!\n"
        "Usage:\n"
        "python3 tdd-monitor.py /path/to/tested/file.py  /path/to/test/file",
    ):
        sys.argv = ["tdd-mon", "tdd_monitor/src/main"]
        main()


@pytest.fixture
def create_empty_folder_and_remove_it():
    dir_name = ".empty_dir"
    os.mkdir(dir_name)
    yield
    os.rmdir(dir_name)


def tests_empty_tests_dir(create_empty_folder_and_remove_it):
    """Raise an UserWarning if the tests folder is empty"""
    with pytest.raises(
        UserWarning,
        match="Nenhum arquivo de teste neste diretório\n"
        "crie ao menos um arquivo de teste no diretório .empty_dir",
    ):
        sys.argv = ["tdd-mon", "tdd_monitor/src/main.py", ".empty_dir"]
        main()


def tests_dir_not_found():
    """Raise FileNotFoundError for non existing tests path"""
    with pytest.raises(
        FileNotFoundError,
        match="Não foi encontrado o caminho.\n"
        "tdd-monitor somente cria arquivos.\n"
        "Tem certeza que os diretórios existem nos locais especificados?",
    ):
        sys.argv = ["tdd-mon", "tdd_monitor/src/main.py", "non-existing-path"]
        main()
