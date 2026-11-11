from datetime import datetime, timezone, timedelta
import pytest
from federation import *

def test_peer_registry_and_discovery():
    registry=PeerRegistry()
    registry.register(Peer("b","https://b.example",status=PeerStatus.ACTIVE,
                           capabilities=("read","verify"),regions=("ap-south",),latency_ms=20))
    registry.register(Peer("c","https://c.example",status=PeerStatus.UNAVAILABLE,
                           capabilities=("read",)))
    result=discover_peers(registry,DiscoveryQuery(required_capabilities=("verify",),
                           regions=("ap-south",)))
    assert [p.peer_id for p in result.peers] == ["b"]
    assert result.examined == 2

def test_capability_intersection_and_routing():
    a=CapabilitySet.from_names(["read","verify"])
    b=CapabilitySet.from_names(["read","write"])
    assert a.intersect(b).names() == {"read"}
    peers=[Peer("slow","https://slow",status=PeerStatus.ACTIVE,capabilities=("read",),latency_ms=500),
           Peer("fast","https://fast",status=PeerStatus.ACTIVE,capabilities=("read",),latency_ms=10)]
    assert Router().select(peers,required_capabilities=("read",)).peer.peer_id == "fast"

def test_sync_planning_and_receipt():
    plan=plan_sync("s1","a","b",{"same":"x","new":"1","changed":"a"},{"same":"x","old":"2","changed":"b"})
    actions={i.artifact_id:i.action for i in plan.items}
    assert actions == {"changed":"conflict","new":"push","old":"pull","same":"unchanged"}
    done=apply_sync_receipt(plan,{"new":"success","old":"success"})
    assert done.state == SyncState.SUCCEEDED

def test_sync_receipt_partial():
    plan=plan_sync("s","a","b",{"x":"1","y":"2"},{})
    assert apply_sync_receipt(plan,{"x":"success"}).state == SyncState.PARTIAL

def test_retry_and_breaker():
    policy=RetryPolicy(max_attempts=4,initial_delay_seconds=.5,multiplier=2,max_delay_seconds=2)
    assert [policy.delay_for(i) for i in (1,2,3,4)] == [.5,1,2,2]
    breaker=CircuitBreaker(failure_threshold=2,reset_timeout_seconds=10)
    now=datetime.now(timezone.utc)
    breaker.record_failure(now); assert breaker.allow_request(now)
    breaker.record_failure(now); assert breaker.state == CircuitState.OPEN
    assert not breaker.allow_request(now)
    assert breaker.allow_request(now+timedelta(seconds=11))
    assert breaker.state == CircuitState.HALF_OPEN
    breaker.record_success(); assert breaker.state == CircuitState.CLOSED
