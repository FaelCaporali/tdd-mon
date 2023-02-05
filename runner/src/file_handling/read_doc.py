def read_doc(path: str) -> str:
    with open(path, mode="r") as file:
        return file.read()
