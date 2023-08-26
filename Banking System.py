# -*- coding: utf-8 -*-
"""
Created on Thursday September 1 19:12:11 2022

@author: Jayesh
"""

import cx_Oracle
import pandas as pd
import random

con = cx_Oracle.connect('system/root@localhost')
cursor = con.cursor()



#LOGIN FUNCTIONS


def login():
    print("\n\n\t\t\tLOGIN")
    print("\tPress 1 to login as Manager.")
    print("\tPress 2 to login as Employee.")
    print("\tPress 3 to Login as Administrator.")
    
    log = int(input("\n\nEnter your choice: "))
    
    
    if log == 1:
        manager_login()
    elif log == 2:
        employee_login()
    elif log == 3:
        admin_login()
    else:
        print("\n\nInvalid Choice...")
        login()



def manager_login():
    man_ID = input("\n\nEnter your ID: ")
    man_pas = input("\n\nEnter your password: ")
    command = "select * from manager where ID = '" +man_ID +"' and password = '"+ man_pas+"'"

    cursor.execute(command)
    lst=cursor.fetchall()
 
    
    if lst == []:
        print("\n\nLogin Failed..")
        manager_login()
    else:
        print("\n\nLogin Successful..")
        man_fuc()
    
def employee_login():
    emp_ID = input("\n\nEnter your ID: ")
    emp_pas = input("\nEnter your password: ")
    command = "select * from employee where ID = '" +emp_ID +"' and password = '"+ emp_pas+"'"

    cursor.execute(command)
    lst=cursor.fetchall()
 
    
    if lst == []:
        print("\n\nLogin Failed..")
        employee_login()
    else:
        print("\n\nLogin Successful..\n\n")
        emp_fuc()
    
    
def admin_login():
        admin_ID = input("\n\nEnter your ID: ")
        admin_pas = input("\n\nEnter your password: ")
        command = "select * from admin where ID = '" +admin_ID +"' and password = '"+ admin_pas+"'"

        cursor.execute(command)
        lst=cursor.fetchall()
     
        
        if lst == []:
            print("\n\nLogin Failed..")
            admin_login()
        else:
            print("\n\nLogin Successful..")
            admin_func()
    
  
    
  
    
#EMPLOYEE FUNCTION

def emp_fuc():
    print("\n\n1. Open New Account.\n")
    print("2. Closing Existing Account\n")
    print("3. Show Details.\n")
    print("4. Cash Deposite.\n") 
    print("5. Cash Widrawl.\n")
    print("6. Log Out.")
    
    choice = int(input("\n\nEnter Your Choice: "))
    
    if choice == 1:
        new_acc()
    elif choice == 6: 
        login()
    elif choice == 2:
        close_acc()
    elif choice == 3:
        show_details()
    elif choice == 4:
        cash_depo()
    elif choice == 5:
        cash_wid()
    
    
    
def new_acc():
    cust_name = input("\n\nEnter Your Name: ")
    acc_no = "1010326"+str(random.randint(1,100))
    pin = int(input("Enter The Pin to the account: "))
    cash = int(input("Enter the Amount of Cash to be Deposited: "))
    
    if cash <= 5000:
        print("\n\nAmounnt should be Greater than 5000\n")
        cash = int(input("Re-enter the Amount of Cash to be Deposited: "))
        
    command = "select * from bank_acc where acc_no = "+acc_no
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        command1 = "insert into bank_acc values('"+cust_name+"',"+acc_no+","+str(pin)
        cursor.execute(command1)
        command2 = "insert into cash values("+acc_no+","+str(cash)+")"
        cursor.execute(command2)
        cursor.execute("commit")
    else:
        acc_no =str(int(acc_no) + 645616)
        command1 = "insert into bank_acc values("+acc_no+",'"+cust_name+"',"+str(pin)+")"
        cursor.execute(command1)
        command2 = "insert into cash values("+acc_no+","+str(cash)+")"
        cursor.execute(command2)
        cursor.execute("commit")
    print("\n'\nAccount Created Successfully...!!")    
    print("\n\nName: ",cust_name)
    print("Account Number: ",acc_no)
    print("Cash: ",cash)
    print("\n\n")
    emp_fuc()
    
 
def close_acc():
    acc_no = input("\n\nEnter the Account Number to be Deleted: ")
    command = "select * from bank_acc where acc_no = "+acc_no
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nAccount Does Not Exist..!")
        print("\n\tTry Again - ")
        close_acc()
    else:
        command1 = "delete from bank_acc where acc_no ="+acc_no
        command2 = "delete from cash where acc_no ="+acc_no
        commit = "commit"
        cursor.execute(command1)
        cursor.execute(command2)
        cursor.execute(commit)
        print("\n\nAccount Deleted Successfully..!")
        emp_fuc()


def show_details():
    
    acc_no = input("Enter the Account Number: ")
    command = "select * from bank_acc where acc_no = "+acc_no
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nAccount Does Not Exist..!")
        print("\n\tTry Again - ")
        show_details()
    else:
        command = "select bank_acc.acc_no , name , cash from bank_acc, cash where bank_acc.acc_no = cash.acc_no and cash.acc_no ="+acc_no
        df=cursor.execute(command)
        details = pd.DataFrame(df,index = [[""]*len(df)],columns =['Acc_no','Name','Balance'])
        print("\n\nAccount Details Are:\n\n")
        print(details)
        print("\n\n\n")
        emp_fuc()



def cash_depo():
    acc_no = input("Enter the Account Number: ")
    depo = int(input("Enter amount to be Deposited: "))
    command = "select * from bank_acc where acc_no = "+acc_no
    
    if cursor.execute(command) == []:
        print("\n\nAccount Does Not Exist..!")
        print("\n\tTry Again - ")
        cash_depo()
    else:
        command = "update cash set cash = cash + "+str(depo)+" where acc_no = "+acc_no
        commit = "commit"
        cursor.execute(command)
        cursor.execute(commit)
        print("\n\nAmount deposited Successfully..!")
        emp_fuc()


def cash_wid():
    acc_no = input("Enter the Account Number: ")
    widl = int(input("Enter amount to be widrawn: "))
    command = "select * from bank_acc where acc_no = "+acc_no
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nAccount Does Not Exist..!")
        print("\n\tTry Again - ")
        cash_depo()
    else:
        command = "update cash set cash = cash - "+str(widl)+" where acc_no = "+acc_no
        commit = "commit"
        cursor.execute(command)
        cursor.execute(commit)
        print("\n\nAmount Widrawn Successfully..!")
        emp_fuc()



#ADMIN FUNCTION

def admin_func():
    print("\n\n1. Add New Manager.\n")
    print("2. Add New Employee\n")
    print("3. Delete Existing Manager.\n")
    print("4. Delete Existing Employee.\n")
    print("5. Login as Employee.\n")
    print("6. Login as Manager.\n") 
    print("7. show details of Manager.\n")
    print("8. show details of Employee.\n")
    print("9. Log Out.")
    
    choice = int(input("\n\nEnter Your Choice: "))
    
    if choice == 1:
        new_man()
    elif choice == 9:
        login()
    elif choice == 5:
        emp_fuc()
    elif choice == 2:
        new_emp("a")
    elif choice == 3:
        del_man()
    elif choice == 4:
        del_emp()
    elif choice == 7:
        detail_man()
    elif choice == 8:
        detail_emp()
    elif choice == 6:
        man_fuc()



def new_man():
    name = input("Enter the name of the Manager: ")
    ID = name[0:3]+str(random.randint(100, 151654601))
    pin = input("Enter the Password: ")
    command = "select * from manager where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        command1= "insert into manager values('"+ID+"','"+pin+"')"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nManager Successfully Added..!\n\n")
        print("\nManager ID : ",ID)
        admin_func()
        
    else:
        ID.replace(ID[-1:-3],str(random.randint(10,99)))
        command1= "insert into manager values('"+ID+"','"+pin+"')"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nManager Successfully Added..!\n\n")
        print("\nManager ID : ",ID)
        admin_func()
    
def new_emp(check):
    name = input("Enter the name of the Employee: ")
    ID = name[0:3]+str(random.randint(100, 151654601))
    pin = input("Enter the Password: ")
    salary = input("Enter the Salary of the Employee: ")
    command = "select * from employee where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        command1= "insert into employee values('"+ID+"','"+pin+"',"+salary+",default,default)"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nEmployee Successfully Added..!\n\n")
        print("\nEmployee ID : ",ID)
        if check =="a":
            admin_func()
        else:
            man_fuc()
        
    else:
        ID.replace(ID[-1:-3],str(random.randint(10,99)))
        command1= "insert into employee values('"+ID+"','"+pin+"',"+salary+",default,default)"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nEmployee Successfully Added..!\n\n")
        print("\nEmployee ID : ",ID)
        if check =="a":
            admin_func()
        else:
            man_fuc()
        
def del_emp():
    ID = input("Enter the ID of the Employee: ")
    command = "select * from employee where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nEmployee Does Not exist, Re-Try...")
        del_emp()
        
    else:
        command1= "delete from employee where ID = '"+ID+"'"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nEmployee Successfully Deleted..!\n\n")
        admin_func()
        
        
def del_man():
    ID = input("Enter the ID of the Manager: ")
    command = "select * from Manager where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nManager Does Not exist, Re-Try...")
        del_man()
        
    else:
        command1= "delete from Manager where ID = '"+ID+"'"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nManager Successfully Deleted..!\n\n")
        admin_func()
        

def detail_man():
    command = "select * from manager"
    df=cursor.execute(command)
    details = pd.DataFrame(df,index = [[""]*len(df)],columns =['ID','Password'])
    print("\n\nManager Details Are:\n\n")
    print(details)
    print("\n\n\n")
    admin_func()     
        
def detail_emp():
    command = "select * from employee"
    df=cursor.execute(command)
    details = pd.DataFrame(df,index = [[""]*len(df)],columns =['ID','Password'])
    print("\n\nEmployee Details Are:\n\n")
    print(details)
    print("\n\n\n")
    admin_func()
    
    
#MANAGER FUNCTION

def man_fuc():
    print("\n\n1. Hire New Employee.\n")    
    print("2. Fire An Employee.\n")
    print("3. ADD Bonus.\n")
    print("4. Show all the details of all employees.\n")
    print("5. Grant Leave.\n")
    print("6. Change Salary.\n")
    print("7. Log Out.\n\n")
    
    a = int(input("\nEnter your Choice: "))
    
    if a == 1:
        new_emp("m")
    elif a == 2:
        del_emp()
    elif a == 3:
        add_bonus()
    elif a == 4:
        detail_emp()
    elif a == 7:
        login()
    elif a ==5:
        grant_leave()
    elif a ==6:
        change_sal()


def add_bonus():
    ID = input("Enter the ID of the Employee: ")
    command = "select * from employee where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nEmployee Does Not exist, Re-Try...")
        add_bonus()
        
    else:
        bonus = input("Enter the Additional Bonus Amount: ")
        command1= "update employee SET bonus = bonus +"+bonus+" where ID = '"+ID+"'"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nBonus Updated Successfully..!\n\n")
        man_fuc()

def grant_leave():
    ID = input("Enter the ID of the Employee: ")
    command = "select * from employee where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nEmployee Does Not exist, Re-Try...")
        grant_leave()
        
    else:
        leave = input("Enter Number of Leave days: ")
        try:
            command1= "update employee SET leave = leave +"+leave+" where ID = '"+ID+"'"
            cursor.execute(command1)
            cursor.execute("commit")
            print("\n\nLeave Granted..!\n\n")
            grant_leave()
            
        except cx_Oracle.IntegrityError :
            print("\n\nEmployee can take only 20 Leaves in a Year.\n")
            grant_leave()
        
        
        
        
def change_sal():
    ID = input("Enter the ID of the Employee: ")
    command = "select * from employee where ID = '"+ID+"'"
    cursor.execute(command)
    lst = cursor.fetchall()
    if lst == []:
        print("\n\nEmployee Does Not exist, Re-Try...")
        change_sal()
    
    else:
        salary = input("Enter the New Salary of the Employee: ")
        command1= "update employee SET salary = "+salary+" where ID = '"+ID+"'"
        cursor.execute(command1)
        cursor.execute("commit")
        print("\n\nSalary Changed..!\n\n")
        change_sal()
        
        
login()
    
