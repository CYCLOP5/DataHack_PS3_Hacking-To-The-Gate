choice = input("Enter 1 for bicep.py, 2 for pushup.py, or 3 for app_squat.py: ")

if choice == "1":
    exec(open("/home/cyclops/Desktop/datahon/bicep.py").read())
elif choice == "2":
    exec(open("/home/cyclops/Desktop/datahon/pushup.py").read())
elif choice == "3":
    exec(open("/home/cyclops/Desktop/datahon/app_squat.py").read())
else:
    print("Invalid choice. Please enter 1, 2, or 3.")



