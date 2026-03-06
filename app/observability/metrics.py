from collections import defaultdict

total_requests = 0
llm_calls = 0
cache_hits = 0

actions = defaultdict(int)

latencies = []


def record_request():
    global total_requests
    total_requests += 1


def record_llm_call():
    global llm_calls
    llm_calls += 1


def record_cache_hit():
    global cache_hits
    cache_hits += 1


def record_decision(action, latency_ms):

    actions[action] += 1

    if latency_ms:
        latencies.append(latency_ms)


def get_metrics():

    avg_latency = 0

    if latencies:
        avg_latency = sum(latencies) / len(latencies)

    return {
        "total_requests": total_requests,
        "llm_calls": llm_calls,
        "cache_hits": cache_hits,
        "action_distribution": dict(actions),
        "avg_latency_ms": avg_latency
    }