n = 5  # Number of steps in the staircase

step = [0] * (n + 2)  # Number of steps + 2 array of 0 elements
step[0] = 1  # Step 1
step[1] = 1  # Step 2
step[2] = 2  # Step 3

for i in range(3, n + 1):
    # Counting how many ways can run up
    step[i] = step[i - 1] + step[i - 2] + step[i - 3]
print(step[n])
