class Bank:
    default_ac = 5000
    user_details = []
    def __init__(self) -> None:
        Bank.default_ac += 1
        

class User:
    def __init__(self, name, address, gender, email, password, account_type) -> None:
        self.name = name
        self.address = address
        self.gender = gender
        self.email = email
        self.password = password
        self.account_type = account_type
        Bank.default_ac += 1
        self.balance = 0
        self.account_number = Bank.default_ac
        self.transactions = []
        self.loan_count = 0
        
    def create_account(self):
        user_info = {
            'name': self.name,
            'address': self.address,
            'gender': self.gender,
            'email': self.email,
            'password': self.password,
            'account_type': self.account_type,
            'account_number' : self.account_number,
            'balance': self.balance,
            'transactions': self.transactions,
            'loan_count': self.loan_count
        }
        Bank.user_details.append(user_info)
        print("\nAccount created successfully.")
     
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            transaction = f"Deposited {amount}"
            self.transactions.append(transaction)

            for user_info in Bank.user_details:
                if user_info['account_number'] == self.account_number:
                    user_info['balance'] = self.balance
                    user_info['transactions'] = self.transactions
                    break
            print(f"Deposited {amount}. Current balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded!")
        else:
            self.balance -= amount
            transaction = f"Withdrew {amount}"
            self.transactions.append(transaction)

            for user_info in Bank.user_details:
                if user_info['account_number'] == self.account_number:
                    user_info['balance'] = self.balance
                    user_info['transactions'] = self.transactions
                    break
            print(f"Withdrew {amount}. Current balance: {self.balance}")

    def check_balance(self):
        print(f"Your current balance is {self.balance}")
        

    def show_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transactions:
            if transaction.startswith("Deposited"):
                print("Deposit:", transaction.split(" ")[1])
            elif transaction.startswith("Withdrew"):
                print("Withdrawal:", transaction.split(" ")[1])
            elif transaction.startswith("Loan"):
                print("Loan:", transaction.split(" ")[1])
                
                
    def take_loan(self):
        if self.loan_count < 2:
            #default loan amount
            loan_amount = 10000
            self.balance += loan_amount
            transaction = f"Loan Taken: {loan_amount}"
            self.transactions.append(transaction)
            self.loan_count += 1

            admin_instance = None
            for user in admin.user_list:
                if user.account_number == self.account_number:
                    admin_instance = admin
                    break

            if admin_instance:
                admin_instance.total_loan_amount += loan_amount

            print(f"Loan taken: {loan_amount}. Current balance: {self.balance}")
        else:
            print("You have already taken the maximum allowed loans.")
   
    def transfer_money(self, recipient_account, amount):
        if amount > 0:
            if recipient_account not in Bank.user_details:
                print("Error: Account does not exist.")
            else:
                for user_info in Bank.user_details:
                    if user_info['account_number'] == recipient_account:
                        recipient_user = user_info
                        break

                if self.balance >= amount:
                    self.balance -= amount
                    recipient_user['balance'] += amount

                    transaction = f"Transferred {amount} to Account {recipient_account}"
                    self.transactions.append(transaction)

                    transaction = f"Received {amount} from Account {self.account_number}"
                    recipient_user['transactions'].append(transaction)

                    print(f"Transferred {amount} to Account {recipient_account}. Current balance: {self.balance}")
                else:
                    print("Error: Insufficient balance.")
        else:
            print("Error: Invalid amount for transfer.")

        
        
class Admin:
    def __init__(self):
        self.user_list = []
        self.total_loan_amount = 0

    def create_user_account(self, name, address, gender, email, password, account_type):
        user = User(name, address, gender, email, password, account_type)
        user.create_account()
        self.user_list.append(user) 
        return user
    
    def delete_account(self, account_number):
        found_user = None

        for user_info in Bank.user_details:
            if user_info['account_number'] == account_number:
                found_user = user_info
                break

        if found_user:
            self.user_list = [user for user in self.user_list if user.account_number != account_number]
            Bank.user_details.remove(found_user)
            print(f"Account of {found_user['name']} (Account Number: {account_number}) has been deleted from the admin's user list.")
        else:
            print("Error: Account not found in the admin's user list.")
            
    def view_all_user_account_list(self):
        if self.user_list:
            print("List of All User Accounts:")
            for user in self.user_list:
                print(f"Name: {user.name}, Account Number: {user.account_number}")
        else:
            print("No user accounts found.")
            
    def check_total_balance_of_bank(self):
        total_balance = sum(user['balance'] for user in Bank.user_details)
        print(f"Total Balance of the Bank: {total_balance}")
        
    def check_total_loan_amount(self):
        print(f"Total Loan Amount in the Bank: {self.total_loan_amount}")
        
    def on_off_loan_of_bank(self, enable_loan):
        if enable_loan:
            self.loan_feature_enabled = True
            print("Loan feature is enabled for the bank.")
        else:
            self.loan_feature_enabled = False
            print("Loan feature is disabled for the bank.")


# Create an admin account
admin = Admin()
#create an admin default password
admin_password = "admin123"  
admin.create_user_account("admin", "admin Address", "M", "admin@example.com", admin_password, "admin")

# Create an instance of the Bank
bnk = Bank()

# creating a replica for this project

while True:
    print("Press 1 for login.")
    option = int(input())  

    if option == 1:
        # Ask for user or admin login
        print("Choose login type:")
        print("Press 1 for User login.")
        print("Press 2 for Admin login.")
        login_choice = int(input())

        if login_choice == 1:
            # User login
            print("Enter your account number: ")
            account_number = int(input())
            found_user = None

            for user_info in Bank.user_details:
                if user_info['account_number'] == account_number:
                    found_user = User(
                        user_info['name'],
                        user_info['address'],
                        user_info['gender'],
                        user_info['email'],
                        user_info['password'],
                        user_info['account_type'],
                    )
                    found_user.account_number = account_number
                    found_user.balance = user_info['balance']
                    found_user.transactions = user_info['transactions']
                    found_user.loan_count = user_info['loan_count']
                    break

            if found_user:
                print(f"Welcome, {found_user.name}!")
                while True:
                    print("\n\nChoose below options:")
                    print("Press 1 to deposit.")
                    print("Press 2 to withdraw.")
                    print("Press 3 to check balance.")
                    print("Press 4 to show transaction history.")
                    print("Press 5 to take a loan.")
                    print("Press 6 to transfer money.")
                    print("Press 7 to log out.\n")

                    user_choice = int(input())

                    if user_choice == 1:
                        amount = float(input("Enter the amount to deposit: "))
                        found_user.deposit(amount)
                    elif user_choice == 2:
                        amount = float(input("Enter the amount to withdraw: "))
                        found_user.withdraw(amount)
                    elif user_choice == 3:
                        found_user.check_balance()
                    elif user_choice == 4:
                        found_user.show_transaction_history()
                    elif user_choice == 5:
                        found_user.take_loan()
                    elif user_choice == 6:
                        recipient_account = int(input("Enter the recipient's account number: "))
                        amount = float(input("Enter the amount to transfer: "))
                        found_user.transfer_money(recipient_account, amount)
                    elif user_choice == 7:
                        break

            else:
                print("Account not found. Please check your account number.")
        

        elif login_choice == 2:
        # Admin login
            admin_psw = input("Enter admin password: ")  
            if admin_psw == admin_password:  
                print("Admin login successful.")

                while True:
                    print("\n\nAdmin Menu:")
                    print("Press 1 to create a user account.")
                    print("Press 2 to delete a user account.")
                    print("Press 3 to view all user accounts list.")
                    print("Press 4 to check the total available balance of the bank.")
                    print("Press 5 to check the total loan amount.")
                    print("Press 6 to turn the loan feature on/off.")
                    print("Press 7 to log out as admin.\n")

                    admin_choice = int(input())

                    if admin_choice == 1:
                        # Create a user account
                        name = input("Enter user's name: ")
                        address = input("Enter user's address: ")
                        gender = input("Enter user's gender: ")
                        email = input("Enter user's email: ")
                        password = input("Enter user's password: ")
                        account_type = input("Enter user's account type: ")

                        new_user = admin.create_user_account(name, address, gender, email, password, account_type)
                        print(f"User {new_user.name} (Account Number: {new_user.account_number}) created successfully.")

                    elif admin_choice == 2:
                        # Delete a user account
                        account_number_to_delete = int(input("Enter the account number to delete: "))
                        admin.delete_account(account_number_to_delete)


                    elif admin_choice == 3:
                        admin.view_all_user_account_list()

                    elif admin_choice == 4:
                        admin.check_total_balance_of_bank()

                    elif admin_choice == 5:
                        admin.check_total_loan_amount()

                    elif admin_choice == 6:
                        enable_loan = input("Enable loan feature? (yes/no): ").strip().lower()
                        if enable_loan == "yes":
                            admin.on_off_loan_of_bank(True)
                        elif enable_loan == "no":
                            admin.on_off_loan_of_bank(False)
                        else:
                            print("Invalid input. Use 'yes' to enable or 'no' to disable.")

                    elif admin_choice == 7:
                        break

            else:
                print("Admin login failed. Incorrect password.")



        
        






