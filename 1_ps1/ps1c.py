## 6.100A Pset 1: Part c
## Name: Abayo Joseph Desire
## Time Spent: 30 minutes
## Collaborators: N/A

##############################################
## Get user input for initial_deposit below ##
##############################################

initial_deposit = float(input("Enter the initial deposit: "))


#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################

lo = 0.0
hi = 1.0

r=(lo+hi)/2  # Average of the possible lowest and highest rates
months=36
total_cost_of_home = 800000
percent_down_payment=0.12
steps=0


##################################################################################################
## Determine the lowest rate of return needed to get the down payment for your dream home below ##
##################################################################################################

# Check is the initial_deposit is higher than the required down payment
if initial_deposit >= total_cost_of_home*percent_down_payment:
    r=0.0

# Check if it's possible to generate the required down payment given the rate 0% - 100%
elif initial_deposit*(1+1/12)**months < total_cost_of_home*percent_down_payment:
    r=None

# Otherwise run a bisection search
else:
    while abs(total_cost_of_home*percent_down_payment - initial_deposit*(1+r/12)**months) >= 100:
        if total_cost_of_home*percent_down_payment - initial_deposit*(1+r/12)**months > 100:
            lo=r
        else:
            hi=r
        r=(lo+hi)/2
        steps +=1

print("Best savings rate:", r)
print("Steps in bisection search:", steps)
