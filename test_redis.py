from upstash_redis import Redis

redis = Redis(
    url="https://calm-salmon-15962.upstash.io",
    token="AT5aAAIncDEyYmFkZjlhN2QxYzE0MWI3ODQ3YWE5NDk2Zjg2ZTE0MXAxMTU5NjI",
)

redis.set("foo1", "bar1")
value = redis.get("foo1")
print(value)
