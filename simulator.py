import sys
from random import randint
from models import Coordinate, Robot, Table


class ToyRobotSimulator(object):

    """
    This toy robot simulator will create robots and place to table and perform some actions like move, turn left and turn right.
    """
    tables = {} # store tables in dictionary e.g. {'table1': table1}
    robots = {} # store robots in dictionary e.g. {'robot1': robot1}
    robot_on_table = {}   # store robots in tables e.g. {robot1: table1, robot2: table2}
    actions = ['PLACE', 'MOVE', 'LEFT', 'RIGHT', 'REPORT', 'END']

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return "Simulator(%s)" % self.name

    # deploying the simulator and create robots and tables
    def deploy(self, table_params=[{}], robot_names=[]):
        if table_params and robot_names:
            for t in table_params:
                if set(Table.attributes) <= set(t):
                    self.tables[t['name']] = Table(t['name'],t['dx'],t['dy'],t['rule'])
                else:
                    print('Table parameters "%s" not valid!' % t)

            for name in robot_names:
                self.robots[str(name)] = Robot(str(name))

            return True

        else:
            print("No valid data for creating tables and robots!")
            return False

    # placing robots to tables
    def place(self, robot, table, x, y, f):
        if not isinstance(robot, Robot):
            raise TypeError("The robot must be Robot instance")

        if not isinstance(table, Table):
            raise TypeError("The table must be Table instance")

        if f not in Robot.facing_directions.keys():
            print("Cannot set robot facing to %s, please choose one from %s" % (f, Robot.facing_directions))
            return False

        if self.robots and self.tables:
            coord = table.get_coordinate(x,y)
            if coord is not None:
                robot.set_coordinate_and_f(coord,f)
                self.robot_on_table[robot] = table
                return True
            else:
                print("Cannot place %s on %s at Coordinate(%s,%s)" % (robot.name, table.name, x,y))
                return False
        else:
            print("No tables or robots created yet! Please use method deploy() to create some")
            return False

    # take actions to robot
    def perform(self, robot, action):
        if action and isinstance(action, str) and robot and isinstance(robot, Robot):
            if not robot.is_placed():
                print("Please place the robot on table before perform other actions")
                return False
            if action in self.actions:
                if action == 'MOVE':
                    table = self.robot_on_table[robot]
                    # get move steps including direction
                    move_step = table.STEP_CAL_RULE["TO_%s" % robot.f]
                    new_coordinate = None
                    if robot.f in table.x_axis:
                        new_coordinate = table.get_coordinate(robot.coordinate.x + move_step,
                                                           robot.coordinate.y)
                    elif robot.f in table.y_axis:
                        new_coordinate = table.get_coordinate(robot.coordinate.x,
                                                           robot.coordinate.y + move_step)

                    if new_coordinate is not None:
                        robot.move_to(new_coordinate)
                        return True
                    else:
                        print("Cannot move further!")
                        return False

                elif action == 'LEFT':
                    return robot.turn_left()
                elif action == 'RIGHT':
                    return robot.turn_right()
                elif action == 'REPORT':
                    print("Output: %s" % (robot.get_report()))
                    return True


        print("Failed to perform action: %s, please choose action from %s" % (action, self.actions))
        return False

    # start simulation
    def start(self):
        """
        for demonstration here using standard input stream from terminal
        """
        counter = 0
        while True:
            # maximum 10 invalid times to try
            if counter >= 10:
                print("End simulator!")
                sys.exit()

            print("Please choose robot and table from below to start and input using format: robot,table")
            print("Robots: %s" % self.robots.keys())
            print("Tables: %s" % self.tables.keys())
            if sys.version_info[0] < 3:
                rt = raw_input()
            else:
                rt = input()
            if len(rt) == 0:
                counter += 1
            else:
                rts = rt.split(',')
                if len(rts) >= 2:
                    robot = self.robots[rts[0]] if rts[0] in self.robots.keys() else None
                    table = self.tables[rts[1]] if rts[1] in self.tables.keys() else None
                else:
                    counter += 1
                    continue

                if robot and table:
                    print("Start %s on %s with moving rule %s:" % (repr(robot), repr(table), table.STEP_CAL_RULE))
                    while True:
                        if sys.version_info[0] < 3:
                            action_str = raw_input()
                        else:
                            action_str = input()

                        action_values = action_str.split()
                        if action_values and len(action_values) > 0:
                            if action_values[0] == 'PLACE':
                                # use random x,y,f for demonstration example
                                '''
                                self.place(robot,
                                           table,
                                           randint(0,table.dx-1),
                                           randint(0,table.dy-1),
                                           ["SOUTH", "WEST", "NORTH", "EAST"][randint(0,3)])
                                '''
                                if len(action_values) > 1:
                                    values = action_values[1].split(',')
                                    if len(values) >= 3:
                                        self.place(robot,
                                                   table,
                                                   int(values[0]),
                                                   int(values[1]),
                                                   values[2])
                                    else:
                                        print("Please input data using format: PLACE 0,0,NORTH")
                                else:
                                    print("Please input data using format: PLACE 0,0,NORTH")

                            elif action_values[0] == 'END':
                                print("End %s:" % repr(robot))
                                break
                            else:
                                self.perform(robot,action_values[0])


if __name__ == "__main__":


    # uncomment to try some more here
    # create tables using parameters
    table_params = [{'name': 'table1', 'dx': 5, 'dy': 5, 'rule': None},
                        {'name': 'table2', 'dx': 10, 'dy': 10, 'rule': None},
                        {'name': 'table3', 'dx': 50, 'dy': 50,
                         'rule': {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': 1, 'TO_EAST': -1}},
                        {'name': 'table4', 'dx': 100, 'dy': 100,
                         'rule': {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': -1, 'TO_EAST': 1}},
                        ]

    # create robots using parameters
    robot_params = ['robot1', 'robot2', 'robot3', 'robot4', ]


    trs = ToyRobotSimulator("trs")
    trs.deploy(table_params,robot_params)
    trs.start()


