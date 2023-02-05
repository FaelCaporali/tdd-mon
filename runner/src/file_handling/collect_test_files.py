import os


def collect_test_files(path: str) -> list[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No such folder {path}"
        )
    dir = [
        os.path.join(pth, f)
        for pth, _dirs, files in os.walk(path)
        for f in files
        if f[:4] == 'test' and f[-3:] == '.py'
    ]
    if len(dir) == 0:
        raise UserWarning(
            "Nenhum arquivo de teste neste diretório\n"
            f"crie ao menos um arquivo de teste no diretório {path}"
        )
    return dir
