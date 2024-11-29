def get_optimization_criteria():
    print("Select optimization criteria:")
    print("1. Shortest travel time")
    print("2. Least cost")
    print("3. Minimal number of transfers")
    choice = input("Enter the number of your choice (1-3): ")

    if choice == '1':
        criteria = 'time'
    elif choice == '2':
        criteria = 'cost'
    elif choice == '3':
        criteria = 'transfers'
    else:
        print("Invalid choice. Defaulting to shortest travel time.")
        criteria = 'time'

    return criteria
