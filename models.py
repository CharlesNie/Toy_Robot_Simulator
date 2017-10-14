"""
There are three models in this toy robot simulator, which are Coordinate model,
Robot model and Table model.
"""


class Coordinate(object):
    """
    Coordinate model contains the x, y coordinates for positioning robot on table
    """

    def __init__(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y
        else:
            raise TypeError('Coordinate x,y must be int')

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Coordinate(%s,%s)" % (self.x, self.y)


class Robot(object):
    """
    Robot model represents the robot which will perform the behavior of move, turn left and turn right.
    A robot instance will be inited when place command executed with parameters X,Y,F. In this model,
    using degree to represent facing directions is for easily expanding purpose, e.g. facing direction of SouthWest
    will has degree in the degree range from 1 to 89
    """

    # facing derections degree gives each direction a degree value, default 0 degree is SOUTH here,
    # these values can be custom and expanded. e.g. add SOUTH-WEST degree value 45 if you want the robot
    # can face SOUTH-WEST
    facing_directions = {"SOUTH": 0, "WEST": 90, "NORTH": 180, "EAST": 270}

    # LEFT = -1 here means anticlockwise turning, while RIGHT = 1 means clockwise turning
    turn_directions = {"LEFT": -1, "RIGHT": 1}

    # the default turning degree of robot
    turn_degree = 90

    def __init__(self, name):
        if name:
            self.name = str(name)
        else:
            raise AttributeError('Name cannot be None or empty string')
        self.last_position = None
        self.coordinate = None
        self.f = None
        self.degree = None

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return 'Robot("%s")' % self.name

    # assign the position and facing direction to robot when placing it to table
    def set_coordinate_and_f(self, coordinate, f):
        if coordinate and f:
            if isinstance(coordinate, Coordinate):
                # the coordinate of positioning robot
                self.coordinate = coordinate
                # the last position the robot located
                self.last_position = coordinate
                self.f = str(f)  # robot facing direction
                self.degree = self.facing_directions[f] if f in self.facing_directions.keys() else 0
                return True
            else:
                raise TypeError('The coordinate parameter must be Coordinate instance')
        else:
            raise AttributeError('Coordinate and f cannot be None or empty string')

    # detect self is placed or not
    def is_placed(self):
        if self.coordinate and self.f:
            return True
        return False

    # move robot to coordinate
    def move_to(self, coordinate):
        if self.is_placed() and coordinate:
                self.last_position = self.coordinate
                self.coordinate = coordinate
                if self.last_position != self.coordinate:
                    return True
        return False

    # turn robot in different dicrections
    def turn(self, direction, degree):
        if self.is_placed() and direction in self.turn_directions.keys():
            # make the degree value always between 0 to 360(not include 360)
            _degree = degree if degree is not None else self.turn_degree
            self.degree = (self.degree + self.turn_directions[direction] * _degree) % 360
            self.f = self.get_f(self.degree)
            return True
        return False

    # make robot can turn left
    def turn_left(self, degree=None):
        return self.turn('LEFT', degree)

    # make robot can turn right
    def turn_right(self, degree=None):
        return self.turn('RIGHT', degree)

    # get_f cast degree to facing direction
    def get_f(self, degree):
        for k, v in self.facing_directions.items():
            if degree == v:
                return k
        return self.f

    # get current situation report
    def get_report(self):
        return "%s,%s,%s" % (self.coordinate.x, self.coordinate.y, self.f)


class Table(object):
    """
    Table model is for placing robot on and moving robot on.
    """

    # movement step calculation rules based on origin point, default origin point is at SOUTH WEST most corner with
    # Coordinate(0,0), then move to south will be x - 1, while to north is x + 1, and move to west will be y - 1, while
    # move to east will be y + 1. This can be custom when creating table instance.
    STEP_CAL_RULE = {'TO_SOUTH': -1, 'TO_NORTH': 1, 'TO_WEST': -1, 'TO_EAST': 1}
    y_axis = ['SOUTH','NORTH']
    x_axis = ['WEST', 'EAST']

    attributes = ['name', 'dx', 'dy', 'rule']

    def __init__(self, name, dx, dy, new_step_cal_rule=None):
        self.name = str(name)
        if isinstance(dx, int) and isinstance(dy, int):
            self.dx = dx  # dimension x
            self.dy = dy  # dimension y
        else:
            raise TypeError('Dimension dx,dy must be int')
        if new_step_cal_rule is not None:
            self.STEP_CAL_RULE = new_step_cal_rule

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return 'Table("%s",%s,%s)' % (self.name,self.dx, self.dy)

    def get_coordinate(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('x,y must be int')
        # limit coordinate x,y within dx,dy
        if 0 <= x < self.dx and 0 <= y < self.dy:
            return Coordinate(x, y)
        else:
            # raise ValueError('x,y must be less than dx, dy in table')
            return None
