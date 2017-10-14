import unittest
from models import Coordinate, Robot, Table
from simulator import ToyRobotSimulator
from random import randint


class TestCoordinate(unittest.TestCase):

    def setUp(self):
        self.coordinate1 = Coordinate(3,2)
        self.coordinate2 = Coordinate(0,4)
        self.coordinate3 = Coordinate(3,2)

    def testString(self):
        self.assertEqual('(3,2)', str(self.coordinate1))
        self.assertEqual('(0,4)', str(self.coordinate2))
        self.assertEqual('(3,2)', str(self.coordinate3))

    def testEqual(self):
        self.assertFalse(self.coordinate1 == self.coordinate2)
        self.assertTrue(self.coordinate1 == self.coordinate3)

    def testRepr(self):
        self.assertEqual('Coordinate(3,2)', repr(self.coordinate1))
        self.assertEqual('Coordinate(0,4)', repr(self.coordinate2))
        self.assertEqual('Coordinate(3,2)', repr(self.coordinate3))


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.robot1 = Robot('robot1')
        self.robot2 = Robot('robot2')
        self.robot3 = Robot('robot3')
        self.robot4 = Robot('robot4')
        self.robot5 = Robot('robot5')

    def testString(self):
        self.assertEqual('robot1', str(self.robot1))
        self.assertEqual('robot2', str(self.robot2))
        self.assertEqual('robot3', str(self.robot3))
        self.assertEqual('robot4', str(self.robot4))
        self.assertEqual('robot5', str(self.robot5))

    def testRepr(self):
        self.assertEqual('Robot("robot1")', repr(self.robot1))
        self.assertEqual('Robot("robot2")', repr(self.robot2))
        self.assertEqual('Robot("robot3")', repr(self.robot3))
        self.assertEqual('Robot("robot4")', repr(self.robot4))
        self.assertEqual('Robot("robot5")', repr(self.robot5))

    def test_set_coordinate_and_f(self):

        self.assertTrue(self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH'))
        self.assertEqual(Coordinate(0, 0), self.robot1.coordinate)
        self.assertEqual(Coordinate(0, 0), self.robot1.last_position)
        self.assertEqual('SOUTH', self.robot1.f)
        self.assertEqual(0, self.robot1.degree)

        self.assertTrue(self.robot2.set_coordinate_and_f(Coordinate(1, 1), 'NORTH'))
        self.assertEqual(Coordinate(1, 1), self.robot2.coordinate)
        self.assertEqual(Coordinate(1, 1), self.robot2.last_position)
        self.assertEqual('NORTH', self.robot2.f)
        self.assertEqual(180, self.robot2.degree)

        self.assertTrue(self.robot3.set_coordinate_and_f(Coordinate(2, 2), 'WEST'))
        self.assertEqual(Coordinate(2, 2), self.robot3.coordinate)
        self.assertEqual(Coordinate(2, 2), self.robot3.last_position)
        self.assertEqual('WEST', self.robot3.f)
        self.assertEqual(90, self.robot3.degree)

        self.assertTrue(self.robot4.set_coordinate_and_f(Coordinate(3, 3), 'EAST'))
        self.assertEqual(Coordinate(3, 3), self.robot4.coordinate)
        self.assertEqual(Coordinate(3, 3), self.robot4.last_position)
        self.assertEqual('EAST', self.robot4.f)
        self.assertEqual(270, self.robot4.degree)

        self.assertTrue(self.robot5.set_coordinate_and_f(Coordinate(4, 4), 'EAST'))
        self.assertEqual(Coordinate(4, 4), self.robot5.coordinate)
        self.assertEqual(Coordinate(4, 4), self.robot5.last_position)
        self.assertEqual('EAST', self.robot5.f)
        self.assertEqual(270, self.robot4.degree)

    def test_move_to(self):
        self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH')
        self.assertTrue(self.robot1.move_to(Coordinate(0, 1)))
        self.assertTrue(self.robot1.coordinate == Coordinate(0, 1))
        self.assertTrue(self.robot1.last_position == Coordinate(0, 0))

        self.robot2.set_coordinate_and_f(Coordinate(1, 1), 'NORTH')
        self.assertTrue(self.robot2.move_to(Coordinate(1, 0)))
        self.assertTrue(self.robot2.coordinate == Coordinate(1, 0))
        self.assertTrue(self.robot2.last_position == Coordinate(1, 1))

        self.robot3.set_coordinate_and_f(Coordinate(2, 2), 'WEST')
        self.assertTrue(self.robot3.move_to(Coordinate(2, 0)))
        self.assertTrue(self.robot3.coordinate == Coordinate(2, 0))
        self.assertTrue(self.robot3.last_position == Coordinate(2, 2))

        self.robot4.set_coordinate_and_f(Coordinate(3, 3), 'EAST')
        self.assertTrue(self.robot4.move_to(Coordinate(3, 0)))
        self.assertTrue(self.robot4.coordinate == Coordinate(3, 0))
        self.assertTrue(self.robot4.last_position == Coordinate(3, 3))

        self.robot5.set_coordinate_and_f(Coordinate(4, 4), 'EAST')
        self.assertTrue(self.robot5.move_to(Coordinate(4, 0)))
        self.assertTrue(self.robot5.coordinate == Coordinate(4, 0))
        self.assertTrue(self.robot5.last_position == Coordinate(4, 4))

    def test_turn_left(self):
        self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH')
        self.robot2.set_coordinate_and_f(Coordinate(1, 1), 'NORTH')
        self.robot3.set_coordinate_and_f(Coordinate(2, 2), 'WEST')
        self.robot4.set_coordinate_and_f(Coordinate(3, 3), 'EAST')
        self.robot5.set_coordinate_and_f(Coordinate(4, 4), 'EAST')
        self.assertTrue(self.robot1.turn_left())
        self.assertTrue(self.robot2.turn_left())
        self.assertTrue(self.robot3.turn_left())
        self.assertTrue(self.robot4.turn_left())
        self.assertTrue(self.robot5.turn_left())
        self.assertEqual('EAST', self.robot1.f)
        self.assertEqual('WEST', self.robot2.f)
        self.assertEqual('SOUTH', self.robot3.f)
        self.assertEqual('NORTH', self.robot4.f)
        self.assertEqual('NORTH', self.robot5.f)

        self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH')
        self.assertTrue(self.robot1.turn_left(180))
        self.assertEqual('NORTH', self.robot1.f)

    def test_turn_right(self):
        self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH')
        self.robot2.set_coordinate_and_f(Coordinate(1, 1), 'NORTH')
        self.robot3.set_coordinate_and_f(Coordinate(2, 2), 'WEST')
        self.robot4.set_coordinate_and_f(Coordinate(3, 3), 'EAST')
        self.robot5.set_coordinate_and_f(Coordinate(4, 4), 'EAST')
        self.assertTrue(self.robot1.turn_right())
        self.assertTrue(self.robot2.turn_right())
        self.assertTrue(self.robot3.turn_right())
        self.assertTrue(self.robot4.turn_right())
        self.assertTrue(self.robot5.turn_right())
        self.assertEqual('WEST', self.robot1.f)
        self.assertEqual('EAST', self.robot2.f)
        self.assertEqual('NORTH', self.robot3.f)
        self.assertEqual('SOUTH', self.robot4.f)
        self.assertEqual('SOUTH', self.robot5.f)

        self.robot1.set_coordinate_and_f(Coordinate(0, 0), 'SOUTH')
        self.assertTrue(self.robot1.turn_right(270))
        self.assertEqual('EAST', self.robot1.f)

    def test_get_f(self):
        self.assertEqual('SOUTH', self.robot1.get_f(0))
        self.assertEqual('WEST', self.robot1.get_f(90))
        self.assertEqual('NORTH', self.robot1.get_f(180))
        self.assertEqual('EAST', self.robot1.get_f(270))
        self.assertEqual(None, self.robot1.get_f(200))


class TestTable(unittest.TestCase):

    def setUp(self):
        self.table1 = Table('table1', 5, 5)
        self.table2 = Table('table1', 10, 10)
        self.table3 = Table('table1', 50, 50, {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': 1, 'TO_EAST': -1})
        self.table4 = Table('table1', 100, 100, {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': -1, 'TO_EAST': 1})

    def test_get_coordinate(self):
        self.assertTrue(Coordinate(3, 3) == self.table1.get_coordinate(3, 3))
        self.assertTrue(Coordinate(8, 9) == self.table2.get_coordinate(8, 9))
        self.assertTrue(Coordinate(34, 45) == self.table3.get_coordinate(34, 45))
        self.assertTrue(Coordinate(78, 88) == self.table4.get_coordinate(78, 88))


class TestToyRobotSimulator(unittest.TestCase):

    def setUp(self):
        self.trs = ToyRobotSimulator('trs1')
        self.table_params = [{'name': 'table1', 'dx': 5, 'dy': 5, 'rule': None},
                        {'name': 'table2', 'dx': 10, 'dy': 10, 'rule': None},
                        {'name': 'table3', 'dx': 50, 'dy': 50,
                         'rule': {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': 1, 'TO_EAST': -1}},
                        {'name': 'table4', 'dx': 100, 'dy': 100,
                         'rule': {'TO_SOUTH': 1, 'TO_NORTH': -1, 'TO_WEST': -1, 'TO_EAST': 1}},
                        ]
        self.robot_names = ['robot1', 'robot2', 'robot3', 'robot4', ]
        self.directions = ["SOUTH", "WEST", "NORTH", "EAST"]

    def test_deploy(self):
        self.assertTrue(self.trs.deploy(self.table_params, self.robot_names))

    def test_place(self):

        self.trs.deploy(self.table_params, self.robot_names)

        for robot, table in zip(self.trs.robots.values(), self.trs.tables.values()):
            self.assertTrue(self.trs.place(robot,
                                           table,
                                           randint(0, table.dx-1),
                                           randint(0, table.dy-1),
                                           self.directions[randint(0,3)]))
        """
        for k,v in self.trs.robot_on_table.items():
            print("%s,%s,%s  on  %s" % (k.coordinate.x, k.coordinate.y, k.f, repr(v)))
        """

    def test_perform(self):

        self.trs.deploy(self.table_params, self.robot_names)

        for robot, table in zip(self.trs.robots.values(), self.trs.tables.values()):

            self.trs.place(robot,
                           table,
                           randint(0, table.dx - 1),
                           randint(0, table.dy - 1),
                           self.directions[randint(0, 3)])

            print("Before move: %s" % robot.get_report())
            self.assertTrue(self.trs.perform(robot, 'MOVE'))
            print("After move: %s" % robot.get_report())

            print("Before turn left: %s" % robot.get_report())
            self.assertTrue(self.trs.perform(robot, 'LEFT'))
            print("After turn left: %s" % robot.get_report())

            print("Before turn right: %s" % robot.get_report())
            self.assertTrue(self.trs.perform(robot, 'RIGHT'))
            print("After turn right: %s" % robot.get_report())

            print("Perform report: ")
            print("Output: %s" % robot.get_report())

    def test_start(self):
        self.trs.start()


if __name__ == "__main__":
    unittest.main()
