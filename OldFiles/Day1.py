a = "a"
b = "b"
print(a + b)
print(a * 2)

f1 = 0.10
f2 = 0.20
print(f1 + f2)
print(f1 / f2)
print(f1 * f2)
print(f1 - f2)

t = True
f = False
print(t + f)
print(t - f)
print(t * f)
print(f / t)

colors = ["red", "green", "blue"]
print(colors)
colors[0] = "white"
print(colors)
colors.append('black')
print(colors)

tuple = (1, 2, 3, 4, 5)
print(tuple[2])
print(len(tuple))

months = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30}
print(months)
months["May"] = 31
print(months)
months["Feb"] = 29
print(months)

for num in range(1, 11):
    if num == 3:
        print("Fizz")
    elif num == 5:
        print("Buzz")
    else:
        print(num)

fruits_and_veggies = [["Apple", "Banana", "Orange"], ["Broccoli", "Peas", "Carrots"]]
for sublist in fruits_and_veggies:
    for item in sublist:
        print(item)

a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9, 10]
for i in a:
    b[a.index(i)] += i
print(b)