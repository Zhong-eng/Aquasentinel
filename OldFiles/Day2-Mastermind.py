import random

# Generate random number
num = str(random.randint(0, 9999))

# Add zeroes to the beginning of number if the number is less than 4 digits
for i in range(4 - len(num)):
    num = "0" + num

# Create list of Xs
x_list = ["X", "X", "X", "X"]

# Define number of User's turns
turns = 0

# Check if user has less than 6 turns left
while turns < 10:
    # Check if there are still any digits left to guess
    if "X" not in x_list:
        break

    # Get user input
    user_input = input("Enter your number: ")

    for i in list(user_input):
        index = user_input.index(i)
        if num[index] == i:
            x_list[index] = i
    print(" ".join(x_list))
    turns += 1

if "X" in x_list:
    print(f"You lose\nThe number was {num}")
else:
    print("You win")
