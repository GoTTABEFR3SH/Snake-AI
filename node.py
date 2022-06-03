import heapq


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

        # defining greater than for purposes of heap queue

    def __gt__(self, other):
        return self.f > other.f


def astar(num_rows, num_collumns, target_position, start_position, walls, game, window):
    open_list = []
    closed_list = []

    heapq.heapify(open_list)

    start_node = Node()
    start_node.position = (start_position[0], start_position[1])
    start_node.g = start_node.f = start_node.h = 0

    heapq.heappush(open_list, start_node)
    while len(open_list) > 0:
        print("start")
        current_node = heapq.heappop(open_list)
        #  current_index = 0

        # for index, item in enumerate(open_list):
        #   print("Looking through open list...")
        #    print(len(open_list))
        #   if item.f < current_node.f:
        #       current_node = item
        #      current_index = index
        #     print("f")

        closed_list.append(current_node)
        walls.append((current_node.position[0], current_node.position[1]))
        game.draw.rect(window, (225, 0, 0),
                       (int(current_node.position[0] * 20), int(current_node.position[1] * 20), 20, 20))
        game.display.flip()

        # print("Closed list = ", len(closed_list))

        if current_node.position[0] == target_position[0] and current_node.position[1] == target_position[1]:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []

        for new_position in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > num_collumns or node_position[0] < 0 or node_position[1] > num_rows or node_position[
                1] < 0:
                continue
            match = False
            t = 0
            while t < len(walls) and match is False:
                #  print("here 3")
                temp = walls[t]
                if node_position[0] == temp[0] and node_position[1] == temp[1]:
                    match = True

                t += 1
            if match is True:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            # print(len(children))
            print("looking through children")

            if len([closed_child for closed_child in closed_list if
                    closed_child.position[0] == child.position[0] and closed_child.position[1] == child.position[
                        1]]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = ((abs(child.position[0] - target_position[0]) * 2) + (
                    abs(child.position[1] - target_position[1]) * 2))
            # print("The H value: ", child.h)
            child.f = child.g + child.h
            game.draw.rect(window, (255, 255, 255),
                           (int(child.position[0] * 20), int(child.position[1] * 20), 20, 20))
            game.display.flip()
            print(len(open_list))

            if child in open_list:
                t = open_list.index(child)
                if child.g < open_list[t].g:
                    open_list[t].g = child.g
                    open_list[t].h = child.h
                    open_list[t].f = child.f
            else:
                print("appending child to open list...")
                heapq.heappush(open_list, child)
                game.draw.rect(window, (0, 0, 225),
                               (int(child.position[0] * 20), int(child.position[1] * 20), 20, 20))
                game.display.flip()

        # yo = open_list[-1]
        # print(yo.position)


def ham(start, bounds, block_size):
    path = [start]
    it = 1
    max = ((bounds[0] / block_size) * (bounds[1] / block_size))
    safe_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while len(path) < max:
        for next_move in safe_moves:
            node_position = (path[it][0] + next_move[0], path[it][1] + next_move[1])
            for visited_node in path:  # check to see if we already have the node in the list
                if node_position == visited_node:
                    continue

            if node_position[0] > max[0] or node_position[0] < 0 or node_position[1] > max[1] or node_position[
                1] < 0:  # are we in bounds
                continue

            path.append(node_position)
            it += 1
            break

