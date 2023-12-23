import math

class Point2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class PRQuadtreeNode:
    def __init__(self, top_left=None, bot_right=None):
        self.top_left = top_left if top_left is not None else Point2D(0, 0)
        self.bot_right = bot_right if bot_right is not None else Point2D(0, 0)
        self.data = None
        self.is_leaf = True
        self.top_left_tree = None
        self.top_right_tree = None
        self.bot_left_tree = None
        self.bot_right_tree = None

    def insert(self, point):
        if self.in_boundary(point):
            if self.data is None:
                self.data = point
            else:
                if self.is_leaf:
                    self.is_leaf = False
                    self.subdivide()

                if self.top_left_tree.in_boundary(point):
                    self.top_left_tree.insert(point)
                elif self.top_right_tree.in_boundary(point):
                    self.top_right_tree.insert(point)
                elif self.bot_left_tree.in_boundary(point):
                    self.bot_left_tree.insert(point)
                elif self.bot_right_tree.in_boundary(point):
                    self.bot_right_tree.insert(point)

    def search(self, p):
        if not self.in_boundary(p):
            return None

        if self.is_leaf and self.data is not None:
            return self.data

        if self.top_left_tree is not None and self.top_left_tree.in_boundary(p):
            return self.top_left_tree.search(p)
        if self.top_right_tree is not None and self.top_right_tree.in_boundary(p):
            return self.top_right_tree.search(p)
        if self.bot_left_tree is not None and self.bot_left_tree.in_boundary(p):
            return self.bot_left_tree.search(p)
        if self.bot_right_tree is not None and self.bot_right_tree.in_boundary(p):
            return self.bot_right_tree.search(p)

    def in_boundary(self, p):
        return (
            p.x >= self.top_left.x
            and p.x <= self.bot_right.x
            and p.y >= self.top_left.y
            and p.y <= self.bot_right.y
        )

    def subdivide(self):
        x_mid = (self.top_left.x + self.bot_right.x) / 2
        y_mid = (self.top_left.y + self.bot_right.y) / 2

        self.top_left_tree = PRQuadtreeNode(Point2D(self.top_left.x, y_mid), Point2D(x_mid, self.bot_right.y))
        self.top_right_tree = PRQuadtreeNode(Point2D(x_mid, y_mid), self.bot_right)
        self.bot_left_tree = PRQuadtreeNode(self.top_left, Point2D(x_mid, y_mid))
        self.bot_right_tree = PRQuadtreeNode(Point2D(x_mid, self.top_left.y), Point2D(self.bot_right.x, y_mid))

class PRQuadtree:
    def __init__(self):
        self.root = None

    def __init__(self, points):
        self.root = None
        for point in points:
            self.insert(point)

    def insert(self, point):
        if self.root is None:
            self.root = PRQuadtreeNode(Point2D(0, 0), Point2D(100, 100))  # Altere os valores conforme necessário
        self.root.insert(point)

    def search(self, p):
        if self.root is not None:
            return self.root.search(p)

    def range_query(self, top_left, bot_right):
        result = []
        self._range_query(self.root, top_left, bot_right, result)
        return result

    def _range_query(self, node, top_left, bot_right, result):
        if node is None:
            return

        if node.in_boundary(top_left) and node.in_boundary(bot_right):
            if node.data is not None:
                result.append(node.data)

            if not node.is_leaf:
                self._range_query(node.top_left_tree, top_left, bot_right, result)
                self._range_query(node.top_right_tree, top_left, bot_right, result)
                self._range_query(node.bot_left_tree, top_left, bot_right, result)
                self._range_query(node.bot_right_tree, top_left, bot_right, result)

    def find_nearest_point_within_radius(self, center, radius):
        top_left = Point2D(center.x - radius, center.y + radius)
        bot_right = Point2D(center.x + radius, center.y - radius)

        possible_points = self.range_query(top_left, bot_right)
        min_distance = float('inf')
        nearest_point = None

        for point in possible_points:
            distance = math.sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_point = point

        return nearest_point, min_distance

# Exemplo de uso:
if __name__ == "__main__":
    points = [
        Point2D(10, 20),
        Point2D(5, 15),
        Point2D(30, 25),
        Point2D(40, 10),
        Point2D(25, 35)
    ]

    quadtree = PRQuadtree(points)

    center = Point2D(20, 20)
    radius = 15

    nearest_point, distance = quadtree.find_nearest_point_within_radius(center, radius)

    print(f"Centro do círculo: ({center.x}, {center.y})")
    print(f"Raio do círculo: {radius}")
    if nearest_point:
        print(f"Ponto mais próximo encontrado: ({nearest_point.x}, {nearest_point.y}) a uma distância de {distance}")
    else:
        print("Nenhum ponto encontrado dentro do raio.")
