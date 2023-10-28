
import os

choice = input("Enter your choice (1 for pushup, 2 for squat, 3 for biceps): ")

if choice == "1":
    os.system('python /path/to/pushup.py')
elif choice == "2":
    os.system('python /path/to/app_squat.py')
elif choice == "3":
    os.system('python /path/to/bicep.py')
else:
    print("Invalid choice")
