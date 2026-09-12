return { clamp = function(n, lo, hi) assert(type(n) == "number", "Expected a numeric resource"); return math.max(lo, math.min(hi, n)) end }
