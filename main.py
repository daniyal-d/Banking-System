import sqlite3
import re

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def create_table():
    cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')


create_table()

from random import randint
import math
identification = 0


account = ""
random_number = "400000"
random_pin = ""


def credit_update():
    global random_number
    global random_pin
    global account
    

    cur.execute(f"SELECT balance FROM card WHERE number = {account}")
    balance_amount = int(str(cur.fetchone()).replace("(","").replace(")","").replace(",",""))


    choice = input("""1. View Balance
2. Add Money
3. Transfer Money
4. Delete Account
5. Log Out
0. Exit
  """)

    random_number = ""
    random_pin = ""

    if choice == "1":
        print(balance_amount)
        credit_update()

    elif choice == "2":
        money_add = float(input("Input how much you would like to deposit: "))
        balance_amount += money_add
        cur.execute(f'UPDATE card SET balance = {balance_amount} WHERE number = {account}')
        conn.commit()
        print("Money successfully deposited")
        credit_update()


    elif choice == "3":
        card_number = input("Which number would you like to transfer to?: ")
        cur.execute(f"SELECT * FROM card WHERE number={card_number}")

        if cur.fetchone() is None and luhn_check(card_number) == True:
          print("That card number does not exist.")
          credit_update()

        elif card_number == account:
          print("You can't transfer money to the same account")

        elif luhn_check(card_number):
          # All works except this. Work on retrieving balance and transfering
           transfer_amount = int(input("Enter much would you like to tranfer: "))
           if transfer_amount > balance_amount:
             print("Not enough money!")
             credit_update()
           else:
             giving_away_balance = balance_amount - transfer_amount
             receiving_amount = transfer_amount
             cur.execute(f'UPDATE card SET balance = {giving_away_balance} WHERE number = {account}')
             conn.commit()
             cur.execute(f"UPDATE card SET balance = balance + {receiving_amount} WHERE number = {card_number}")
             conn.commit()
             print("Money succesfully transferred")
             credit_update()

        else:
          print("You most likely made a mistake while typing the the card number. Please try again!")
          credit_update()


    elif choice == "4":
        cur.execute(f"DELETE from card WHERE number = {account}")
        conn.commit()
        print("Account successfully deleted!")
        credit()

    elif choice == "5":
        account = ""
        balance_amount = 0
        print("You have successfully logged out!")
        credit()

    elif choice == "0":
        print("Bye!")


def credit():
    global random_number
    global random_pin
    global identification
    global account

    checksum = 0

    choice = input("""1. Create an account
2. Log into account
0. Exit
  """)

    if choice == "1":
        random_number = "400000"
        random_pin = ""
        for i in range(9):
            random_number = random_number + str(randint(0, 9))
        for j in range(4):
            random_pin = random_pin + str(randint(0, 9))

        random_number_checker = [int(x) for x in str(random_number)]

        for i, j in enumerate(random_number_checker):
            if i % 2 == 0:
                random_number_checker[i] = j * 2

        for item, number in enumerate(random_number_checker):
            if number > 9:
                random_number_checker[item] = number - 9

        for ele in range(0, len(random_number_checker)):
            checksum = checksum + random_number_checker[ele]

        checksum2 = int(math.ceil(checksum / 10.0)) * 10
        real_checksum = checksum2 - checksum

        strings = [str(integer) for integer in random_number]
        a_string = "".join(strings)
        random_number = int(a_string)
        random_number = str(random_number) + str(real_checksum)
        identification += 1
        balance_amount = 0

        cur.execute("INSERT INTO card VALUES (?,?,?,?)", (identification, random_number, random_pin, balance_amount))
        conn.commit()
        cur.execute("SELECT * FROM card")
        conn.commit()

        print(f"Your card number: \n{random_number}")
        print(f"Your card PIN: \n{random_pin}")
        credit()

    elif choice == "2":
        validate_number = input("Enter your card number: ")
        validate_pin = input("Enter your PIN: ")

        validate = cur.execute(f"SELECT * FROM card WHERE number={validate_number} and pin={validate_pin}")
        validation2 = cur.fetchone()

        if validation2 is None:
          print("Wrong card number or PIN!")
          credit()
        else:
          account = validate_number
          print("You have successfully logged in!")
          credit_update()

    elif choice == "0":
        print("Bye!")

    else:
        print("Error, please select a valid option.")
        credit()


def luhn_check(card_number: str) -> bool:
  card_true = 0
  bool_check = 0
  card_list = list(card_number)
  card_ending = card_list[-1]
  card_list.pop(-1)

  card_list = [int(i) for i in card_list]
  card_ending = int(card_ending)

  for i, j in enumerate(card_list):
    if i % 2 == 0:
      card_list[i] = j * 2
  for item, number in enumerate(card_list):
    if number > 9:
      card_list[item] = number - 9
  for i in card_list:
    card_true += i
  card_true += card_ending

  if card_true % 2 == 0:
    bool_check = 1

  return bool(bool_check)


credit()
conn.close()
