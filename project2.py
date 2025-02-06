import random
n = random.randint(1,100)
a=-1
guess = 1
while(a!=n): 
    a = int(input("Enter your guess:"))
    if(a>n):
        print("Too high")
        guess+=1
    elif(a<n):
        print("Too low")
        guess+=1
print(f"You have guessed the number {n} correctly in {guess} gusses")
