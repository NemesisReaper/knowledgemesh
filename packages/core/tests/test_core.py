from datetime import datetime, timezone
import pytest
from core import *

def test_ids_and_errors():
    assert new_id("claim").startswith("claim:")
    assert validate_id("node-1")=="node-1"
    with pytest.raises(ValueError): validate_id("../bad")

def test_config_validation():
    cfg=load_settings({"KNOWMESH_ENVIRONMENT":"test","KNOWMESH_MAX_PAGE_SIZE":"50"})
    assert cfg.environment=="test" and cfg.max_page_size==50
    with pytest.raises(ValueError): CoreSettings(default_page_size=101)

def test_canonical_serialization_and_hash():
    assert canonical_json({"b":2,"a":1})=='{"a":1,"b":2}'
    assert stable_hash({"a":1})==stable_hash({"a":1})
    with pytest.raises(ValueError): canonical_json({"time":datetime(2020,1,1)})

def test_event_bus_publish_unsubscribe():
    bus=InMemoryEventBus(); seen=[]
    remove=bus.subscribe("knowledge.created",seen.append)
    envelope=EventEnvelope(new_id("evt"),DomainEvent("knowledge.created","k1",{"x":1}))
    bus.publish(envelope); remove(); bus.publish(envelope)
    assert len(seen)==1

def test_pagination_and_result():
    page=paginate([1,2,3,4],PageRequest(limit=2,offset=1))
    assert page.items==(2,3) and page.has_next and page.next_offset==3
    assert Result(value=42).unwrap()==42
    assert Result(error="bad").is_err
    with pytest.raises(ValueError): Result()

def test_event_handler_exception_propagates():
    bus=InMemoryEventBus()
    bus.subscribe("*",lambda _: (_ for _ in ()).throw(RuntimeError("handler")))
    with pytest.raises(RuntimeError):
        bus.publish(EventEnvelope("e",DomainEvent("x","a",{})))
