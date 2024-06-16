import rpyc

def main():
    user_choice = None
    second_input = None
    welcome_message = """
        Welcome to the MyGoogle Search server!

        Please choose one of the options below by typing the corresponding number:

        1. Upload files to be indexed for future searches;
        2. Remove a file from the system;
        3. List all inserted files;
        4. Perform a keyword search;
   
        Enter the number of the desired option and press Enter:
    """
    print(welcome_message)

    # Get user choice
    user_choice = input("Your choice: ")

    # Check if the user choice is valid
    if user_choice in ['1', '2', '4']:
        # Ask for a second input based on the choice
        if user_choice == '1':
            second_input = input("Enter the file path to upload: ")
            print(f"File path to upload: {second_input}")
        elif user_choice == '2':
            second_input = input("Enter the file path to remove: ")
            print(f"File path to remove: {second_input}")
        elif user_choice == '4':
            second_input = input("Enter the keyword to search: ")
            print(f"Keyword to search: {second_input}")
    elif user_choice == '3':
        print("Listing all inserted files...")
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")


    slave_service = f"MASTER"
    c2 = rpyc.connect_by_service(slave_service)
    print("\n\n\n")
    print(c2.root.find(user_choice, second_input))

if __name__ == "__main__":
    main()
