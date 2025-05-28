# BMI Calculator
# This program calculates your Body Mass Index (BMI)

print("Welcome to the BMI Calculator!")
print()

# Get user's name
name = input("What is your name? ")

# Get weight from user
weight = float(input("Enter your weight in kg: "))

# Get height from user
height = float(input("Enter your height in meters: "))

# Calculate BMI
# BMI formula = weight / (height * height)
bmi = weight / (height * height)

# Round BMI to 2 decimal places
bmi = round(bmi, 2)

# Print the result
print()
print("Hello", name)
print("Your BMI is:", bmi)

# Tell user what their BMI means
if bmi < 18.5:
    print("You are underweight")
elif bmi >= 18.5 and bmi < 25:
    print("You have a normal weight")
elif bmi >= 25 and bmi < 30:
    print("You are overweight")
else:
    print("You are obese")

print()
print("Thank you for using the BMI Calculator!")