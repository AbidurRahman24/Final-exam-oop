import random
from abc import ABC, abstractmethod

class User:
    accounts=[]
    mx_loan = 2
    transfer = {} 
    ac = 1000

    def __init__(self,name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type

        self.balance = 0
        self.account_number = self.random_ac_number()
        self.transaction_history = []
        self.loan = 0
        User.transfer[self.account_number] = self
        User.accounts.append(self)

    def random_ac_number(self):
        User.ac += 1
        return User.ac
    
    def deposit (self,amount):
        if amount >= 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited {amount}")
            print(f"\n--> Deposited {amount}. New balance: {self.balance}")
        else:
            print("\n--> Invalid deposit amount")
    
    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew {amount}")
            print(f"\nWithdrew {amount}. New balance: {self.balance}")
        else:
            print("\nWithdrawal amount exceeded")

    # @abstractmethod
    def checkBalance(self):
        print(f"Available balance: {self.balance}") 

    def view_transaction_history(self):
        print(f"transfer balance: {self.transaction_history}")
    
    def take_load(self,amount):
        if amount > 0 and self.loan < User.mx_loan:
            self.balance += amount
            self.transaction_history.append(f"Withdrew {amount}")
            self.mx_loan += 1
            print(f"Loan taken: {amount}")
        else:
            print(f'Invalid loan amount.')

    def transfer_amount(self, transfer_num, amount):
        if transfer_num in User.transfer:
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                tac = User.transfer[transfer_num]
                tac.balance += amount
                self.transaction_history.append({amount})
                tac.transaction_history.append({amount})
            else:
                print(f"insufficient balance.")
        else:
            print(f"Account does not exist.")


class saving(User):
    def __init__(self, name, email, address, account_type):
        super().__init__(name, email, address, account_type)
    
    def checkBalance(self):
        print(f"Balance: {self.balance}")


class Admin:
    admin=[]
    
    def __init__(self,name):
        self.name = name
        self.created_users = []  
    
    def create_user(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        self.created_users.append(user)
        return user
    
    def delete_user(self, account_number):
        for user in self.created_users:
            if user.account_number == account_number:
                self.created_users.remove(user)
                print(f"User account number {account_number} has been deleted.")
        print("User account not found. Deletion failed.")
    
    def view_user_accounts(self):
        return self.created_users
    
    def total_balance(self, account_number):
        for user in self.created_users:
            if str(user.account_number) == account_number:
                return user.balance
        return None
    
    def total_loan_amount(self):
        total_loan = 0
        for user in self.created_users:
            if user.balance < 0:
                total_loan += user.balance
        print(f"Total Loan: {total_loan}")

    def loan_feature(self):
        if User.mx_loan == 0:
            User.mx_loan = 2
            print("Loan feature has been turned on.")
        else:
            User.mx_loan = 0
            print("Loan feature has been turned off")
            
# Main program

currentUser=None


while(True):
    if currentUser==None:
        print("\n--> No user logged in !")
        ch=input("\n--> Register/Login (R/L) : ")
        if ch=="R":
            name= input("name: ")
            email = input("Email: ")
            address = input("address: ")
            account_type = input("account_type: ")
            a=input("Savings Account or special Account (U/A) :")
            if a=="U":
                currentUser = User(name,email,address,account_type)
            else:
                currentUser = Admin(name)
        elif ch == "L":
            ac_number = int(input("Account Number: "))
            for user in User.accounts:
                if user.account_number == ac_number:
                    currentUser = user
                    break
    else:
        print(f"\nWelcome {currentUser.name} !\n")
        if isinstance(currentUser, User):
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check balance")
            print("4. Transaction history")
            print("5. Loan")
            print("6. Transfer balance")
            print("7. Logout\n")

            op = int(input("Choose Option:"))

            if op == 1:
                amount = int(input("Enter withdrawal amount: "))
                currentUser.withdraw(amount)

            elif op == 2:
                amount = int(input("Enter deposit amount:"))
                currentUser.deposit(amount)

            elif op == 3:
                currentUser.checkBalance()

            elif op == 4:
                currentUser.view_transaction_history()

            elif op == 5:
                amount = int(input("Enter loan amount:"))
                currentUser.take_load(amount)

            elif op == 6:
                transfer_num = input("Enter the account number to transfer to:")
                amount = int(input("Enter transfer amount:"))
                currentUser.transfer_amount(transfer_num, amount)

            elif op == 7:
                currentUser = None

            else:
                print("Invalid Option")

        elif isinstance(currentUser, Admin):
            print("1. Create User")
            print("2. Delete User")
            print("3. View User Accounts")
            print("4. View Total Balance")
            print("5. View Total Loan Amount")
            print("6. Toggle Loan Feature")
            print("7. Logout\n")

            op = int(input("Choose Option:"))
            
            if op == 1:
                name = input("Name: ")
                email = input("Email: ")
                address = input("address: ")
                account_type = input("account_type: ")
                currentUser.create_user(name,email,address,account_type)

            elif op == 2:
                acc = input("Enter account number to delete:")
                result = currentUser.delete_user(acc)

            elif op == 3:
                acc = currentUser.view_user_accounts()
                print("User Accounts:")
                for user in acc:
                    print(f"Name: {user.name}, Account Number: {user.account_number}")

            elif op == 4:
                total_balance = currentUser.total_balance()

            elif op == 5:
                total_loan_amount = currentUser.total_loan_amount()

            elif op == 6:
                result = currentUser.loan_feature()

            elif op == 7:
                currentUser = None

            else:
                print("Invalid Option")



    
    

    
