import pytest
from knowledge_dna import *

def test_identity_and_fingerprint():
    ident = KnowledgeIdentity("c1", "research")
    assert ident.qualified_id == "research:c1"
    assert identity_fingerprint({"b": 2, "a": 1}) == identity_fingerprint({"a": 1, "b": 2})

def test_mutations_do_not_mutate_input():
    source = {"meta": {"score": 2}, "tags": ["a"]}
    result = apply_mutation(source, Mutation(MutationKind.INCREMENT, ("meta","score"), 1))
    assert result.payload["meta"]["score"] == 3
    assert source["meta"]["score"] == 2
    with pytest.raises(KeyError):
        apply_mutation(source, Mutation(MutationKind.REMOVE, ("missing",)))

def test_split_and_merge_conflict():
    split = split_knowledge("parent", {"items": [1,2,3], "topic": "x"},
                            partition_key="items", partitions={"left":[1], "right":[2,3]})
    assert split.children["right"]["items"] == [2,3]
    merged = merge_knowledge({"a":{"x":1}, "b":{"y":2}})
    assert merged.successful and merged.payload["x"] == 1
    conflict = merge_knowledge({"a":{"x":1}, "b":{"x":2}})
    assert not conflict.successful and conflict.conflicts[0].path == ("x",)

def test_lineage():
    graph = LineageGraph()
    graph.add(LineageEvent("e1", "k1", LineageRelation.CREATED))
    graph.add(LineageEvent("e2", "k1", LineageRelation.UPDATED, parents=("e1",)))
    assert [e.event_id for e in graph.ancestors("e2")] == ["e1"]
    assert graph.descendants("e1")[0].event_id == "e2"

def test_history_hash_chain():
    history = KnowledgeHistory("k1")
    history.record({"v": 1})
    history.record({"v": 2}, change_note="update")
    assert history.verify()
    assert history.get(1).payload == {"v": 1}
    assert history.latest.revision == 2
