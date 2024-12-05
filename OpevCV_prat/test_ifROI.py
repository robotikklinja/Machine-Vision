import random

random_nr = random.choice([True, False])

print(random_nr)

if str(input("allow ROI to be? ")) == "Y" or random_nr:
    ROI = 0



if ROI in locals():
    pass
elif ROI in globals():
    pass
else:
    print("Something")



print(ROI)