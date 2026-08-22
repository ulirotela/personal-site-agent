import time
from app.cache import ResponseCache

cache = ResponseCache(ttl_seconds=3)  # Short TTL for demo

print('=== CACHE DEMO ===')
print()

# Miss
result = cache.get('What is Python?')
print(f'1. First lookup: {result}  (miss - nothing cached yet)')

# Store
cache.set('What is Python?', 'Python is a programming language.')
print(f'2. Stored response in cache')

# Hit
result = cache.get('What is Python?')
print(f'3. Second lookup: {result}  (HIT!)')

# Case insensitive
result = cache.get('what is python?')
print(f'4. Lowercase lookup: {result}  (HIT - case insensitive!)')

# Different query = miss
result = cache.get('What is JavaScript?')
print(f'5. Different query: {result}  (miss)')

# Stats
print(f'6. Stats: {cache.stats}')

# Wait for TTL
print(f'7. Waiting 4 seconds for TTL expiration...')
time.sleep(4)

result = cache.get('What is Python?')
print(f'8. After TTL: {result}  (miss - expired!)')
print(f'9. Final stats: {cache.stats}')