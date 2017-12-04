class Production:

    def __init__(self, left_side, right_side):
        self.__left_side = left_side
        self.__right_side = tuple(right_side)

    def get_left_side(self):
        return self.__left_side

    def get_right_side(self):
        return self.__right_side

    def __str__(self):
        return self.__left_side + "-->" + "".join(self.__right_side)