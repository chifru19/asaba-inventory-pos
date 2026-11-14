import os

path = "app/templates/owner_dashboard.html"
if os.path.exists(path):
    with open(path, "r") as f:
        print(f.read())
else:
    print("owner_dashboard.html does not exist!")
