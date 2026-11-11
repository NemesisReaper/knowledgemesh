import unittest

from packages.simulation import (
    Scenario, ScenarioStep, ScenarioRunner, ScenarioError,
    FailureModel, FailureType, sample_failure, apply_failure,
    NetworkModel, NetworkNode, NetworkEdge,
    Intervention, Counterfactual, CounterfactualSimulator,
)


class SimulationTests(unittest.TestCase):
    def test_scenario_dependencies(self):
        runner = ScenarioRunner({
            "start": lambda params, outputs: params["value"],
            "double": lambda params, outputs: outputs["one"] * 2,
        })
        scenario = Scenario("s1", "simple", (
            ScenarioStep("one", "start", {"value": 3}),
            ScenarioStep("two", "double", depends_on=("one",)),
        ))
        result = runner.run(scenario)
        self.assertTrue(result.succeeded)
        self.assertEqual(result.outputs["two"], 6)

    def test_scenario_cycle_rejected(self):
        with self.assertRaises(ScenarioError):
            Scenario("cycle", "cycle", (
                ScenarioStep("a", "x", depends_on=("b",)),
                ScenarioStep("b", "x", depends_on=("a",)),
            ))

    def test_seeded_failure(self):
        model = FailureModel("f1", FailureType.HIGH_LATENCY, 1.0,
                             parameters={"delay_ms": 50})
        event = sample_failure(model, seed=7)
        self.assertTrue(event.triggered)
        state = apply_failure({"latency_ms": 10}, event)
        self.assertEqual(state["latency_ms"], 60)

    def test_network_metrics_and_outage(self):
        net = NetworkModel()
        for node in ("a", "b", "c"):
            net.add_node(NetworkNode(node))
        net.add_edge(NetworkEdge("a", "b", latency_ms=10))
        net.add_edge(NetworkEdge("b", "c", latency_ms=20))
        snapshot = net.snapshot()
        self.assertEqual(snapshot.metrics.connected_components, 1)
        self.assertAlmostEqual(snapshot.metrics.average_shortest_path_latency_ms, 20)
        net.set_node_availability("b", False)
        self.assertEqual(net.snapshot().metrics.connected_components, 2)

    def test_counterfactual(self):
        simulator = CounterfactualSimulator(lambda state: state["capacity"] * 2)
        case = Counterfactual("cf1", "add capacity",
                              (Intervention("capacity", "add", 5),))
        result = simulator.run({"capacity": 10}, case)
        self.assertEqual(result.baseline_outcome, 20)
        self.assertEqual(result.intervention_outcome, 30)
        self.assertEqual(result.delta, 10)


if __name__ == "__main__":
    unittest.main()
