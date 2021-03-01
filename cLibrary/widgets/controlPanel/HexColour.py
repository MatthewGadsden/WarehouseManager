

class HexColour:
    def __init__(self, red, green, blue):
        self.check_val(red)
        self.check_val(green)
        self.check_val(blue)

        self._red = red
        self._green = green
        self._blue = blue

    def get_red(self):
        return self._red

    def get_green(self):
        return self._green

    def get_blue(self):
        return self._blue

    def increment_red(self):
        self.check_val((self._red + 1))
        self._red += 1

    def decrement_red(self):
        self.check_val((self._red - 1))
        self._red -= 1

    def increment_green(self):
        self.check_val((self._green + 1))
        self._red += 1

    def decrement_green(self):
        self.check_val((self._green - 1))
        self._red -= 1

    def increment_blue(self):
        self.check_val((self._blue + 1))
        self._red += 1

    def decrement_blue(self):
        self.check_val((self._blue - 1))
        self._red -= 1

    @staticmethod
    def check_val(color):
        if not isinstance(color, int):
            raise TypeError("red, green and blue must be integers")
        if color > 255 or color < 0:
            raise ValueError("red, green and blue must be greater than 0 and less than 255")

    def __str__(self):
        return str("#" + str(str(hex(self._red))[2:]).zfill(2) + str(str(hex(self._green))[2:]).zfill(2) + str(str(hex(self._blue))[2:]).zfill(2))