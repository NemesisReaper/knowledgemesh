import unittest

from packages.knowledge_graph import (
    GraphBuilder, GraphNode, GraphEdge, KnowledgeGraph, NodeType, EdgeType,
    GraphQuery, QueryEngine, breadth_first, depth_first, shortest_path,
    all_paths, KnowledgeGraphEngine,
)


class KnowledgeGraphTests(unittest.TestCase):
    def setUp(self):
        report = GraphBuilder().build(
            claims=[
                {"id": "c1", "text": "First claim"},
                {"id": "c2", "text": "Second claim"},
                {"id": "c3", "text": "Third claim"},
            ],
            evidence=[{"id": "s1", "title": "Source one", "claim_id": "c1"}],
            relations=[
                {"source": "claim:c1", "target": "claim:c2", "type": "related_to", "weight": 2},
                {"source": "claim:c2", "target": "claim:c3", "type": "related_to", "weight": 1},
                {"source": "claim:c1", "target": "claim:c3", "type": "related_to", "weight": 5},
            ],
        )
        self.graph = report.graph

    def test_builder_and_validation(self):
        self.assertEqual(len(self.graph.nodes()), 4)
        self.assertEqual(len(self.graph.edges()), 4)
        self.assertEqual(self.graph.validate(), ())

    def test_traversals(self):
        bfs = breadth_first(self.graph, "claim:c1", direction="out")
        dfs = depth_first(self.graph, "claim:c1", direction="out")
        self.assertEqual(bfs.nodes[0].id, "claim:c1")
        self.assertGreaterEqual(len(dfs.nodes), 3)

    def test_shortest_path(self):
        path = shortest_path(self.graph, "claim:c1", "claim:c3")
        self.assertEqual([node.id for node in path],
                         ["claim:c1", "claim:c2", "claim:c3"])
        self.assertEqual(len(all_paths(self.graph, "claim:c1", "claim:c3")), 2)

    def test_query(self):
        result = QueryEngine(self.graph).execute(
            GraphQuery(node_types=("claim",), label_contains="claim")
        )
        self.assertEqual(len(result.nodes), 3)

    def test_stats_diff_snapshot(self):
        engine = KnowledgeGraphEngine(self.graph)
        self.assertEqual(engine.stats().node_count, 4)
        snapshot = engine.snapshot()
        snapshot.add_node(GraphNode("concept:x", NodeType.CONCEPT, "Concept X"))
        diff = engine.diff(snapshot)
        self.assertEqual(diff.added_nodes, ("concept:x",))


if __name__ == "__main__":
    unittest.main()
