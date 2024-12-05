import unittest
import networkx as nx
from modules.graph_utils import build_graph, compute_all_pairs_shortest_paths, create_distance_matrix
from geopy.distance import geodesic
import numpy as np

class TestGraphUtils(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [
            {
                "routeName": "route1",
                "position_1": "Tarjan's Home",
                "position1_streetName": "Yeouido",
                "position1_coordinates": [37.52389, 126.92667],
                "position_2": "Relative_8",
                "position2_streetName": "Bukhan-ro",
                "position2_coordinates": [37.5800, 126.9844],
                "travel_mode": "bus",
                "travel_speed": 40,
                "cost_per_km": 2
            }
        ]
    
    def test_build_graph(self):
        G = build_graph(self.sample_data, 'time')
        self.assertTrue(G.has_node("Tarjan's Home"))
        self.assertTrue(G.has_node("Relative_8"))
        self.assertTrue(G.has_edge("Tarjan's Home", "Relative_8"))
        edge_data = G.get_edge_data("Tarjan's Home", "Relative_8")
        self.assertEqual(edge_data['travel_mode'], 'bus')
        expected_distance = geodesic((37.52389, 126.92667), (37.5800, 126.9844)).kilometers
        self.assertAlmostEqual(edge_data['distance'], expected_distance, places=2)
        self.assertAlmostEqual(edge_data['time'], expected_distance / 40, places=2)
        self.assertAlmostEqual(edge_data['cost'], expected_distance * 2, places=2)
    
    def test_compute_all_pairs_shortest_paths(self):
        G = build_graph(self.sample_data, 'time')
        all_pairs = compute_all_pairs_shortest_paths(G)
        self.assertIn("Tarjan's Home", all_pairs)
        self.assertIn("Relative_8", all_pairs["Tarjan's Home"])
        edge_data = G.get_edge_data("Tarjan's Home", "Relative_8")
        self.assertAlmostEqual(all_pairs["Tarjan's Home"]["Relative_8"], edge_data['time'])
    
    def test_create_distance_matrix(self):
        G = build_graph(self.sample_data, 'time')
        all_pairs = compute_all_pairs_shortest_paths(G)
        distance_matrix, index, nodes = create_distance_matrix(G, all_pairs)
        self.assertEqual(distance_matrix.shape, (2, 2))
        self.assertEqual(index["Tarjan's Home"], 0)
        self.assertEqual(index["Relative_8"], 1)
        self.assertAlmostEqual(distance_matrix[0][1], all_pairs["Tarjan's Home"]["Relative_8"])
        self.assertAlmostEqual(distance_matrix[1][0], all_pairs["Relative_8"]["Tarjan's Home"])

if __name__ == '__main__':
    unittest.main()
