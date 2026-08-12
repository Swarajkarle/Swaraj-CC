from copy import deepcopy

GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start
        self.h = self.heuristic()  # Misplaced tiles
        self.f = self.g + self.h

    def heuristic(self):
        """Number of misplaced tiles (excluding blank)."""
        count = 0

        for i in range(3):
            for j in range(3):
                if (
                    self.state[i][j] != 0
                    and self.state[i][j] != GOAL[i][j]
                ):
                    count += 1

        return count

    def __lt__(self, other):
        return self.f < other.f

    def get_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def generate_children(self):
        children = []

        x, y = self.get_blank()

        moves = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dx, dy in moves:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = deepcopy(self.state)

                # Swap blank tile
                new_state[x][y], new_state[nx][ny] = (
                    new_state[nx][ny],
                    new_state[x][y]
                )

                children.append(
                    Node(new_state, self, self.g + 1)
                )

        return children


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def print_solution(node):
    path = []

    while node is not None:
        path.append(node)
        node = node.parent

    path.reverse()

    print("\nSolution Path:\n")

    for step, n in enumerate(path):
        print("Step:", step)

        for row in n.state:
            print(row)

        print("g =", n.g, " h =", n.h, " f =", n.f)
        print()


def a_star(initial_state):
    start = Node(initial_state)

    open_list = [start]
    closed_set = set()

    while open_list:
        open_list.sort(key=lambda x: x.f)
        current = open_list.pop(0)

        if current.state == GOAL:
            print("Goal Reached!")
            print("Total Moves =", current.g)
            print_solution(current)
            return

        closed_set.add(state_to_tuple(current.state))

        children = current.generate_children()

        for child in children:
            child_tuple = state_to_tuple(child.state)

            if child_tuple in closed_set:
                continue

            found = False

            for node in open_list:
                if (
                    node.state == child.state
                    and node.f <= child.f
                ):
                    found = True
                    break

            if not found:
                open_list.append(child)

    print("No Solution Found.")


# Initial State
initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

print("Initial State:")

for row in initial_state:
    print(row)

# Run A* algorithm
a_star(initial_state)
