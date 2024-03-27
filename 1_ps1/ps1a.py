## 6.100A Pset 1: Part a
## Name: Abayo Joseph Desire
## Time Spent: 180 minutes
## Collaborators: Prince(Teaching Assistant)

##################################################################################
## Get user input for annual_salary, percent_saved and total_cost_of_home below ##
##################################################################################
annual_salary=float(input("Enter your annual salary: "))
percent_saved=float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost_of_home=float(input("Enter the cost of your dream home: "))


#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################

percent_down_payment=0.12
amount_saved=0
r=0.06
months=0

###############################################################################################
## Determine how many months it would take to get the down payment for your dream home below ##
###############################################################################################

# Check if the amount_saved is still below the required down payment
while amount_saved < total_cost_of_home * percent_down_payment:

    # Formula: amount_saved*r/12 equals the interest added every month
    # Formula: annual_salary*percent/12 is the percentage of the monthly salary that is saved
    amount_saved += amount_saved*r/12 + annual_salary*percent_saved/12
    months+=1

print("Number of months:", months)
