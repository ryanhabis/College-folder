import scipy.stats as stats

#  Analysis of a sample of 60 faulty products found that the average length of time taken for them to be returned was 15 days.
#  Using the population data in part (b), test the claim that the average length of time taken for faulty products to be returned is 10 days. 
#  Conduct the test at a 0.05 level of significance.

mean = 10
std = 3

# (i)  Determine the proportion of products which take between 6 and 17 days to be returned to retailer.
p = stats.norm.cdf(17, mean, std) - stats.norm.cdf(6, mean, std)
print("Proportion between 6 and 17 days:", p)

# (ii)  Find the number of days within which 95% of faulty products are returned.
days = stats.norm.ppf(0.95, mean, std)
print("Number of days for 95% returns:", days)


