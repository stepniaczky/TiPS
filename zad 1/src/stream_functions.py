def save(filename, msg):
    # with open(f"stream-files/{filename}", "w") as file:
    #     file.write(msg)
    return 0

def load(filename):
    with open(f"stream-files/{filename}") as file:
        message = file.read()
    return message