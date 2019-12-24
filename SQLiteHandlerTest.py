from typing import Any, List, Dict
import unittest
from SQLiteHandler import SQLiteHandler


class TestingDBMethods(unittest.TestCase):
    def test_pathToDBFile(self):
        self.assertEqual("./data/data.db", SQLiteHandler().pathToDBFile)

    def test_getAllResources(self):
        resources: List[Dict] = SQLiteHandler().getAllResources()
        self.assertEqual({'id': 1, 'name': 'Ping-pong Table 1'}, resources[0])
        self.assertEqual({'id': 2, 'name': 'Ping-pong Table 2'}, resources[1])
        self.assertEqual({'id': 3, 'name': 'Ping-pong Table 3'}, resources[2])
        self.assertEqual({'id': 4, 'name': 'Ping-pong Table 4'}, resources[3])
        self.assertEqual({'id': 5, 'name': 'BBQ area 1'}, resources[4])
        self.assertEqual({'id': 6, 'name': 'BBQ area 2'}, resources[5])
        self.assertEqual({'id': 7, 'name': 'BBQ area 3'}, resources[6])
        self.assertEqual({'id': 8, 'name': 'BBQ area 4'}, resources[7])

    def test_bookResource(self):
        SQLiteHandler().bookResource(119607733, 101, '20.11.2019')

    def test_getResourcesByUserId(self):
        resources1: List[Dict] = SQLiteHandler().getResourcesByUserId(5)
        self.assertEqual(
            {
                'resourceId': 8,
                'name': 'BBQ area 4',
                'reservationId': 17,
                'date': '17.11.2019'
            }, resources1[0])
        self.assertEqual(
            {
                'resourceId': 8,
                'name': 'BBQ area 4',
                'reservationId': 18,
                'date': '18.11.2019'
            }, resources1[1])

        #For Sergey
        resources2: List[Dict] = SQLiteHandler().getResourcesByUserId(
            1012086922)
        self.assertEqual(
            {
                'resourceId': 7,
                'name': 'BBQ area 3',
                'reservationId': 19,
                'date': '19.11.2019'
            }, resources2[0])
        self.assertEqual(
            {
                'resourceId': 6,
                'name': 'BBQ area 2',
                'reservationId': 20,
                'date': '20.11.2019'
            }, resources2[1])


if __name__ == '__main__':
    unittest.main()