class Bank:
    def __init__(self,name) -> None:
        self.name = name
        self.__users = {}
        self.__admins = {}
        self.__balance = 0
        self.__loan_status = True
        self.__loan_given = 0
        self.__is_bankrupt = False

    def deposit(self,amount):
        if amount > 0:
            self.__balance += amount
        else :
            print("Invalid Amount")

    def withdraw(self,amount):
        if amount > 0:
            self.__balance -= amount
        else :
            print("Invalid Amount")

    def loan_given(self,amount):
        self.__loan_given += amount
        self.__balance -= amount

    @property
    def balance(self):
        return self.__balance
    
    @property
    def users(self):
        return self.__users
    
    @property
    def admins(self):
        return self.__admins
    
    @property
    def loan_given_amount(self):
        return self.__loan_given
   
    @property
    def status(self):
        return self.__is_bankrupt
    
    @property
    def loan_status(self):
        return self.__loan_status
    
    def loan_status_update(self,status):
        self.__loan_status = status
    
    def status_update(self,status):
        self.__is_bankrupt = status

    def add_user(self,user):
        if user.typ == "Admin":
            admin_number = f'{len(self.__admins)+1}'
            self.__admins[admin_number] = user
            user.ac_number(admin_number)
        else:
            user_number = f'{len(self.__users)+1}'
            self.__users[user_number] = user
            user.ac_number(user_number)

    def delete_account(self,id):
        del self.__users[id]


    def transfer(self,ac_1,ac_2,amount,bank):
         if self.__users[ac_1].balance > amount :
             self.__users[ac_1].withdraw(amount,bank)
             self.__users[ac_2].deposit(amount,bank)
         else:
              print("Insufficient Balance")


        
class User:
    def __init__(self,name,email,address,ac_type,pas) -> None:
        self.name = name
        self.__email = email
        self.__address = address
        self.__ac_type = ac_type
        self.__loan = 0
        self.__own_balance = 0
        self.__balance = self.__loan + self.__own_balance
        self.__ac_number = None
        self.__transaction = {}
        self.loan_count = 0
        self.pas = pas

    def deposit(self,amount,bank):
        if amount<=0:
            print("Invalid Amount")
        else:
            self.__own_balance += amount
            bank.deposit(amount)

        t_no = f'{len(self.__transaction)+1}'
        self.__transaction[t_no] = amount
        print("Deposit Successful")

        self.__balance = self.__loan + self.__own_balance

    def withdraw(self,amount,bank):
        if amount<0:
            print("Unavailable")
        elif amount > self.__balance:
            print("Withdrawal amount exceeded")
        elif amount > bank.balance and bank.status == False:
            print("The bank is bankrupt")
            print(type(bank.status))
        else:
            self.__own_balance -= amount
            bank.withdraw(amount)
            print("Withdraw Successful")

        t_no = f'{len(self.__transaction)+1}'
        self.__transaction[t_no] = -amount

        self.__balance = self.__loan + self.__own_balance

    @property
    def balance(self):
        return self.__loan + self.__own_balance
    
    @property
    def tn_history(self):
        return self.__transaction
    
    @property
    def typ(self):
        return self.__ac_type
    
    def take_loan(self,amount,bank):
        if self.loan_count < 2:
            if bank.balance >= amount and bank.status == False and bank.loan_status == True:
                self.__loan += amount
                bank.loan_given(amount)
                self.loan_count+=1
                print("Taking Loan Successful")

                t_no = f'{len(self.__transaction)+1}'
                self.__transaction[t_no] = amount

            else:
                print("The bank is bankrupt")
        else:
            print("Can't take loan more than twice")

        self.__balance = self.__loan + self.__own_balance

    def ac_number(self,number):
        self.__ac_number = number



        
class Admin(User):
    def __init__(self, name, email, address, ac_type,pas) -> None:
        super().__init__(name, email, address, ac_type,pas)

    def delete_account(self, user_name, bank):
        for user_number, user in bank.users.items():
            if user.name == user_name:
                del bank.users[user_number]
                print("Successfully Deleted ")
                return
        print(f"User '{user_name}' not found.")
    
    def show_users(self,bank):
        for user in bank.users.values():
            print(user.name)

    def bank_balance(self,bank):
        print(bank.balance)

    def loan_amount(self,bank):
        print(bank.loan_given_amount)
    
    def loan_status_update(self,bank,status):
        bank.loan_status_update(status)

    

ab = Bank("AB")

while True:
    print("Welcome to AB Bank")
    print("Login as a :")
    print("1. User")
    print("2. Admin")
    a=int(input())

    if a==1:
        print("1. New Account")
        print("2. Existing Account")
        a=int(input())

        if a==1:
            name = input("Enter your UserName : ")
            email = input("Enter Email : ")
            address = input("Enter Your Address : ")
            t = input("Enter Account Type : 1. Savings 2. Current : ")
            if int(t)==1:
                ty_pe = "Savings"
            else:
                ty_pe = "Current"
            pas = input("Type Password : ")
            usr = User(name,email,address,ty_pe,pas)
            ab.add_user(usr)
            print("Account Opening Successful . Log in again to access account : ")
        elif a==2:
            name = input("Enter your UserName : ")
            pas = input("Type Password : ")

            for user_number, user in ab.users.items():
                if user.name == name and user.pas == pas :
                    print ("Login Successful")
                    
                    while True:
                        print("What do you want to do ? ")
                        print("1. Check Balance")
                        print("2. Deposit")
                        print("3. Withdraw")
                        print("4. Take Loan")
                        print("5. Show Transaction History")
                        print("6. Transfer Balance To Other Account")
                        print("7. Log Out")

                        a=int(input())

                        if a==1:
                            print(f'Your Balance : {user.balance}')

                        elif a==2:
                            amount = int(input("Enter Amount : "))
                            user.deposit(amount,ab)

                        elif a==3:
                            amount = int(input("Enter Amount : "))
                            user.withdraw(amount,ab)

                        elif a==4:
                            amount = int(input("Enter Amount : "))
                            user.take_loan(amount,ab)

                        elif a==5:
                            for key,value in user.tn_history.items():
                                print(f'Transaction No : {key}  Amount : {value}')

                        elif a==6:
                            name_2 = input("Enter Transfer Acount User Name : ")
                            flag = 1

                            for user_number_2, user_2 in ab.users.items():
                                if user_2.name == name_2 :
                                    amount = int(input("Enter amount to transfer : "))
                                    ab.transfer(user_number,user_number_2,amount,ab)
                                    flag = 2
                            if flag ==1:
                                print("Account does not exist")
                            elif flag == 2 :
                                pass

                        elif a==7:
                            break

                else:
                    print("Invalid Login Info")


    elif a==2:
        print("1. New Account")
        print("2. Existing Account")
        a=int(input())

        if a==1:
            name = input("Enter your UserName : ")
            email = input("Enter Email : ")
            address = input("Enter Your Address : ")
            ty_pe = "Admin"
            pas = input("Type Password : ")

            ad = Admin(name,email,address,ty_pe,pas)
            ab.add_user(ad)

            print("Admin Account Opening Successful . Log in again to access account : ")

        elif a==2:
            name = input("Enter your UserName : ")
            pas = input("Type Password : ")

            for user_number, admin in ab.admins.items():
                if admin.name == name and admin.pas == pas :
                    print ("Login Successful")
                    
                    while True:
                        print("What do you want to do ? ")
                        print("1. Delete User Account")
                        print("2. See All User Account List")
                        print("3. Total Available Balance of the Bank")
                        print("4. Total Given Loan Amount of Bank")
                        print("5. Update Loan Status")
                        print("6. Log Out")

                        a=int(input())

                        if a==1:
                            print("Enter UserName of that Account")
                            name = input()
                            admin.delete_account(name,ab)

                        elif a==2:
                            admin.show_users(ab)

                        elif a==3:
                            print("Total Available Balance of the Bank : ")
                            admin.bank_balance(ab)

                        elif a==4:
                            print("Total Given Loan Amount of Bank : ")
                            admin.loan_amount(ab)

                        elif a==5:
                            print("Select option : ")
                            print("1. Turn On Loan")
                            print("2. Turn Off Loan")
                            a=int(input())

                            if a==1 :
                                admin.loan_status_update(ab,True)
                            if a==2 :
                                admin.loan_status_update(ab,False)

                        elif a==6:
                            break
    else:
        pass
    





# ad = Admin("ad","a","a","ad")

# arpan = User("Arpan", "a@g.com", "Ng", "savings")
# ab.add_user(arpan)
# barpan = User("barpan", "a@g.com", "Ng", "savings")
# ab.add_user(barpan)
# carpan = User("cArpan", "a@g.com", "Ng", "savings")
# ab.add_user(carpan)

# ad.delete_account("Arpan", ab)

# arpan.deposit(1000,ab)
# arpan.take_loan(800,ab)
# arpan.take_loan(500,ab)

# print(ab.balance)
# print(arpan.balance)
# ad.show_users(ab)

