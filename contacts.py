#! /usr/bin/python3

import sqlite3

class Application():
    
    def main(self):
        self.data_base = DataBase()
        self.data_base.connect()
        while True:
            print('(s) Save new contact.')
            print('(r) Retrive one contact.')
            print('(q) Quit.')
            op = input('Enter your option and press ENTER: ')
            if op == 's':
                self.save_contact()
            elif op == 'r':
                self.retrieve_contact()
            elif op == 'q':
                break
            else:
                print()
                print('Invalid option!!!')
                print()
        self.data_base.disconnect()

    def save_contact(self):
        print()
        name = input('Name: ')
        phone_number = input('Phone Number: ')
        self.data_base.save_contact(name, phone_number)

    def retrieve_contact(self):
        print()
        name = input('Name: ')
        phone_number = self.data_base.retrieve_contact(name)
        if phone_number is None:
            print('Not found!')
            print()
            return
        print(f'Phone Number: {phone_number}')
        print()

class DataBase():

    def connect(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS contacts (name, phone_number)')

    def disconnect(self):
        self.connection.close()

    def save_contact(self, name, phone_number):
        self.cursor.execute('INSERT INTO contacts VALUES (?, ?)', (name, phone_number))
        self.connection.commit()

    def retrieve_contact(self, name):
        self.cursor.execute('SELECT * FROM contacts WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        
        if result is None:
            return None
        
        _, phone_number = result
        return phone_number

if __name__ == '__main__':
    application = Application()
    application.main()
