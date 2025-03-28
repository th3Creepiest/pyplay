class Piece:
    def __init__(self, shape: list[list[list[int]]], color: tuple[int, int, int]):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.x = 3
        self.y = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_shape(self) -> list[list[int]]:
        return self.shape[self.rotation]

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1
