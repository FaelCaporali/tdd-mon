def create_file(file_path: str):
    print(f"\n-----\nCreating file at {file_path}")
    create = open(file_path, mode="w")
    create.close()
    print("\nFile created! Happy testing!\n-----\n")
