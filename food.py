import random
from random import choice


class Food:
    block_size = None
    color = (0, 225, 0)
    x = 340
    y = 320
    bounds = None

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds

    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self, snake, grid_size, column_blks, row_blks):
        blocks_in_x = (self.bounds[0] / self.block_size)
        blocks_in_y = (self.bounds[1] / self.block_size)
        open_slots = self.get_filled_slots(snake, grid_size, column_blks, row_blks)
        random_slot = random.choice(open_slots)
        self.x = random_slot[0] * self.block_size
        self.y = random_slot[1] * self.block_size


    # self.x = random.randint(0, blocks_in_x - 1) * self.block_size
    # self.y = random.randint(0, blocks_in_y - 1) * self.block_size

    def get_filled_slots(self, snake, grid_size, column_blks, row_blks):
        open_positions = []
        filled_positions = []
        for i in range(len(snake.body)):
            segment = snake.body[i]
            filled_positions.append(((segment[0] / self.block_size), (segment[1] / self.block_size)))
        for x in range(int(column_blks) - 1):
            # print("Here 1")
            for y in range(int(row_blks) - 1):
                # print("here 2")
                t = 0
                match = False
                if len(filled_positions) != 0:
                    while t < len(filled_positions) and match is False:
                      #  print("here 3")
                        temp = filled_positions[t]
                        if x == temp[0] and y == temp[1]:
                            match = True
                            del filled_positions[t]
                        t += 1
                    if match is False:
                        open_positions.append((x, y))
                else:
                    open_positions.append((x, y))

        return open_positions

    def get_food_position(self):
        return self.x / self.block_size, self.y / self.block_size
