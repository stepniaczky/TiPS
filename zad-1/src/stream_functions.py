def save(filename, msg):
    with open(f"stream-files/{filename}", "w") as file:
        file.write(msg)


def load(filename):
    with open(f"stream-files/{filename}") as file:
        arr = file.readlines()
    return arr
