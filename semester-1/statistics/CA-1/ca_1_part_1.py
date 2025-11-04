import math

# A retail store accepts product returns, and they found that 10% of the items sold in a month 
# are returned due to defects. 

# If 25 items are randomly selected from a month's sales records, calculate the following:

    #(i) The expected number of items returned due to defects.
        # Probability of return = 0.10
        # randomly selected items = 25
        # Binomial distribution = (25 * 0.1) = 2.5

    #(iii) The probability that four or more items are returned.   
        # P(x > 4) = 0.236408643

    # (iv) Using python, confirm your answers in questions (i)-(iii).

def binomial_pmf(n, k, p):
    # Probability Mass Function for Binomial Distribution
    # P(X = k) = C(n, k) * p^k * (1-p)^(n-k)
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

def binomial_cdf(n, k_max, p):
    # Cumulative Distribution Function for Binomial Distribution
    # P(X <= k_max) = sum of P(X = k) for k = 0 to k_max
    return sum(binomial_pmf(n, k, p) for k in range(0, k_max + 1))

def main():
    n = 25
    p = 0.10

    # (i) Expected number of returned items
    # Binomial distribution = (25 * 0.1) = 2.5
    expected = n * p
    print(f"Expected number returned (n*p): {expected}")

    # (iii) Probability 4 or more returned = 1 - P(X <= 3)
    part_3 = 1.0 - binomial_cdf(n, 3, p)
    print(f"P(X >= 4): {part_3:.9f}")
    
    
if __name__ == "__main__":
    main()