import os
import json
from utils import FileIOUtils

class User:
    """
        @author Rahul
        This Class handles all the user operations.
        ==========================================

        Methods
        -------

        1. Login
        2. Signup
    """
    def __init__(self):
        self.file = FileIOUtils()
    def login(self, email: str, password: str, signupcheck=False):
        usersPath = 'data/users.json'
        users = []

        out = self.file.readJsonFile(usersPath)

        if out['status'] == 200:
            users = out['data']
        else:
            if not signupcheck:
                print(out['data'])
            return

        userFound = False
        for user in users:
            if user["email"] == email:
                if user["password"] == password:
                    userFound = True
                    if not signupcheck and userFound:
                        print(" -- Login Successful -- ")
                    return user
                else:
                    if not signupcheck:
                        print('Wrong Password.. Try Again')
                    return False
        if not userFound and not signupcheck:
                print('User with the email doesnt exist.. Signup')
        return 

    def signup(self, user: dict):
        foundUser = self.login(user["email"], user["password"], True)

        if foundUser != None:
            print("User Exists.. Try Logging In")
            return

        usersPath = 'data/users.json'
        users = []

        out = self.file.readJsonFile(usersPath)

        if out['status'] == 200:
            users = out['data']

        users.append(user)

        writeUsers = self.file.writeJsonFile(usersPath, users)

        if writeUsers['status'] == 200:
            print()
            print(" -- Signup Successful -- ")
        return user




