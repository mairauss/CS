from typing import Any, List, Dict
import os
import unittest
from SQLiteHandler import SQLiteHandler


class TestingDBMethods(unittest.TestCase):
    def test_pathToDBFile(self):
        self.assertEqual(os.path.dirname(__file__) + "/data/data.db", os.path.dirname(__file__) + SQLiteHandler().pathToDBFile)

    def test_get_all_Resources(self):
        resources: List[Dict] = SQLiteHandler().get_all_Resources()
        self.assertEqual({'description': 'test1', 'id': 1, 'name': 'Ping-pong Table 1'}, resources[0])
        self.assertEqual({'description': 'test2','id': 2, 'name': 'Ping-pong Table 2'}, resources[1])
        self.assertEqual({'description': 'test3','id': 3, 'name': 'Ping-pong Table 3'}, resources[2])
        self.assertEqual({'description': 'test4','id': 4, 'name': 'Ping-pong Table 4'}, resources[3])
        self.assertEqual({'description': 'test5','id': 5, 'name': 'BBQ area 1'}, resources[4])
        self.assertEqual({'description': 'test6','id': 6, 'name': 'BBQ area 2'}, resources[5])
        self.assertEqual({'description': 'test7','id': 7, 'name': 'BBQ area 3'}, resources[6])
        self.assertEqual({'description': 'test8','id': 8, 'name': 'BBQ area 4'}, resources[7])

    def test_bookResource(self):
        pass
        # SQLiteHandler().bookResource(119607733, 101, '20.11.2019')

    def test_get_resources_by_user_id(self):
        resources1: List[Dict] = SQLiteHandler().get_resources_by_user_id(5)
        self.assertEqual(
            {
                'resourceId': 8,
                'name': 'BBQ area 4',
                'reservationId': 17,
                'date': '17.11.2019',
                'time': None
            }, resources1[0])
        self.assertEqual(
            {
                'resourceId': 8,
                'name': 'BBQ area 4',
                'reservationId': 18,
                'date': '18.11.2019',
                'time': None
            }, resources1[1])

        #For Sergey
        resources2: List[Dict] = SQLiteHandler().get_resources_by_user_id(
            1012086922)
        self.assertEqual(
            {
                'resourceId': 7,
                'name': 'BBQ area 3',
                'reservationId': 19,
                'date': '19.11.2019',
                'time': None
            }, resources2[0])
        self.assertEqual(
            {
                'resourceId': 6,
                'name': 'BBQ area 2',
                'reservationId': 20,
                'date': '20.11.2019',
                'time': None
            }, resources2[1])


if __name__ == '__main__':
    unittest.main()