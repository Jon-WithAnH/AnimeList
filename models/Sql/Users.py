class User:
    def __init__(self, data: list) -> None:
        self.id = data[0]
        self.name = data[1]
        self.createdTime = data[2]