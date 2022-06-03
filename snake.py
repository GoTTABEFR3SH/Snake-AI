from enum import Enum
from queue import Queue


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class snake:
    length = None
    direction = None
    body = None
    block_size = None
    color = (0, 0, 225)
    bounds = None
    last_direction = None
    d_queue = Queue(maxsize=0)

    def __init__(self, block_size, bounds, INTIAL_SNAKE_SPEED):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()
        self.speed = INTIAL_SNAKE_SPEED
        self.timer = 1.0 / self.speed

    def respawn(self):
        self.length = 3
        self.body = [(360, 1605), (360, 180), (360, 200)]
        self.direction = Direction.DOWN

    def draw(self, game, window):
        for segment in self.body:
            game.draw.rect(window, self.color, (segment[0], segment[1], self.block_size, self.block_size))

    def move(self):

        curr_head = self.body[-1]

        self.timer += 1.0 / self.speed

        if self.direction == Direction.DOWN:
            next_head = (curr_head[0], curr_head[1] + self.block_size)
            self.body.append(next_head)

        elif self.direction == Direction.UP:
            next_head = (curr_head[0], curr_head[1] - self.block_size)
            self.body.append(next_head)

        elif self.direction == Direction.RIGHT:
            next_head = (curr_head[0] + self.block_size, curr_head[1])
            self.body.append(next_head)

        elif self.direction == Direction.LEFT:
            next_head = (curr_head[0] - self.block_size, curr_head[1])
            self.body.append(next_head)

        if self.length < len(self.body):
            self.body.pop(0)

    def steer(self, direction):
        if self.direction == Direction.DOWN and direction != Direction.UP:
            self.d_queue.put(Direction.DOWN)
            self.direction = direction
        elif self.direction == Direction.UP and direction != Direction.DOWN:
            self.d_queue.put(Direction.UP)
            self.direction = direction
        elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
            self.d_queue.put(Direction.LEFT)
            self.direction = direction
        elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
            self.d_queue.put(Direction.RIGHT)
            self.direction = direction
        print(self.direction)

    def eat(self):
        self.length += 1

    def check_for_food(self, food):
        head = self.body[-1]
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            return True
        else:
            return False

    def check_bounds(self):
        head = self.body[-1]
        if head[0] >= self.bounds[0]:
            return True
        if head[1] >= self.bounds[1]:
            return True

        if head[0] < 0:
            return True
        if head[1] < 0:
            return True

        return False

    def check_if_eaten_ourselfs(self):
        head = self.body[-1]
        has_eaten_tail = False

        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                has_eaten_tail = True

        return has_eaten_tail

    def get_snake_head(self):
        head = self.body[-1]
        return head[0] / self.block_size, head[1] / self.block_size

    def get_snake_body(self):
        filled_positions = []
        for i in range(len(self.body)):
            segment = self.body[i]
            filled_positions.append(((segment[0] / self.block_size), (segment[1] / self.block_size)))
        return filled_positions

    def AI_Steer(self, path):
        head = path[0]
        next_move = path[1]

        if head[0] != next_move[0]:  # x increases as we go left and y increases as we go down
            if head[0] < next_move[0]:
                self.direction = Direction.RIGHT
            else:
                self.direction = Direction.LEFT
        elif head[1] != next_move[1]:
            if head[1] < next_move[1]:
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP
        del path[0]
