class SymbolTable:

    def __init__(self, bucket_count: int = 257):
        self._bucket_count = max(17, int(bucket_count))
        self._buckets = [[] for _ in range(self._bucket_count)]  # Each bucket: list[lexeme]

    def _hash(self, lexeme: str) -> int:
        # Polynomial rolling hash: h = (h * 131 + byte) mod bucket_count
        h = 0
        for ch in lexeme:
            h = (h * 131 + ord(ch)) % self._bucket_count
        return h

    def insert(self, lexeme: str) -> tuple:
        """Insert lexeme if absent and return (bucket, position) tuple."""
        b = self._hash(lexeme)
        bucket = self._buckets[b]

        # Lookup in bucket
        for pos, stored_lexeme in enumerate(bucket):
            if stored_lexeme == lexeme:
                return (b, pos)

        # Not found -> append to bucket and return position
        pos = len(bucket)
        bucket.append(lexeme)
        return (b, pos)

    def dump(self):
        """Return all entries with their (bucket, position) identifiers."""
        result = []
        for bucket_idx, bucket in enumerate(self._buckets):
            for pos, lexeme in enumerate(bucket):
                result.append({
                    "bucket": bucket_idx,
                    "position": pos,
                    "lexeme": lexeme
                })
        return result


