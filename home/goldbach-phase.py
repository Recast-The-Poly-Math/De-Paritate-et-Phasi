"""Reproduce the Research Home note with Python 3.9 or later."""

from functools import cache
from math import isqrt


LIMIT = 1_000_000
SAMPLE_TARGETS = (128, 1_000, 10_000, LIMIT)
SAMPLE_DIVISORS = (3, 5, 7, 11)


def prime_flags(limit):
    flags = bytearray(b"\x01") * (limit + 1)
    flags[:2] = b"\x00\x00"
    for divisor in range(2, isqrt(limit) + 1):
        if flags[divisor]:
            start = divisor * divisor
            flags[start::divisor] = b"\x00" * ((limit - start) // divisor + 1)
    return flags


@cache
def is_prime_by_trial_division(value):
    return value >= 2 and all(
        value % divisor != 0 for divisor in range(2, isqrt(value) + 1)
    )


def odd_splits(target):
    for a in range(3, target // 2 + 1, 2):
        yield a, target - a


def passes_phase_checks(a, b, divisors):
    # cos(2*pi*x/q) == 1 is tested by the exact remainder x % q.
    return all(
        (a == q or a % q != 0) and (b == q or b % q != 0)
        for q in divisors
    )


def main():
    flags = prime_flags(LIMIT)
    odd_primes = [value for value in range(3, LIMIT + 1, 2) if flags[value]]

    print("Target | Odd splits | Survive 3, 5, 7, 11 | Prime pairs")
    for target in SAMPLE_TARGETS:
        split_count = survivor_count = prime_pair_count = 0
        for a, b in odd_splits(target):
            split_count += 1
            survivor_count += passes_phase_checks(a, b, SAMPLE_DIVISORS)
            prime_pair_count += bool(flags[a] and flags[b])
        print(f"{target:,} | {split_count:,} | {survivor_count:,} | {prime_pair_count:,}")

    for target in range(6, 2_001, 2):
        cutoff = isqrt(target - 3)
        divisors = [prime for prime in odd_primes if prime <= cutoff]
        for a, b in odd_splits(target):
            survives = passes_phase_checks(a, b, divisors)
            is_prime_pair = is_prime_by_trial_division(a) and is_prime_by_trial_division(b)
            if survives != is_prime_pair:
                raise RuntimeError(f"Phase and trial division disagree for {a} + {b}")
    print("Full phase filter matches trial division on every odd split through 2,000.")

    if not (flags[2] and is_prime_by_trial_division(2)):
        raise RuntimeError("Failed to verify 4 = 2 + 2")
    for target in range(6, LIMIT + 1, 2):
        for a in odd_primes:
            if a > target // 2:
                raise RuntimeError(f"No prime pair found for {target}")
            b = target - a
            if flags[b]:
                if not (is_prime_by_trial_division(a) and is_prime_by_trial_division(b)):
                    raise RuntimeError(f"Independent verification failed for {a} + {b}")
                break
        else:
            raise RuntimeError(f"Prime search exhausted for {target}")

    count = LIMIT // 2 - 1
    print(f"Verified a prime pair for all {count:,} even targets from 4 to {LIMIT:,}.")


if __name__ == "__main__":
    main()
