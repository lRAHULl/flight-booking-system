import os
import json
from utils import FileIOUtils

class User:
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
        # if os.path.exists(usersPath):
        #     with open(usersPath) as usersFile:
        #         try:
        #             users = json.load(usersFile)
        #         except json.decoder.JSONDecodeError:
        #             print('JSON error')
        #         except:
        #             print('something went wrong!')
        # else:
        #     if not signupcheck:
        #         print('No User Found.. Sign Up')
        #     return

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
        # if os.path.exists(usersPath):
        #     with open(usersPath) as usersFile:
        #         try:
        #             users = json.load(usersFile)
        #         except json.decoder.JSONDecodeError:
        #             print('JSON error')
        #         except:
        #             print('something went wrong!.. Check and correct the data/users.json file')

        users.append(user)

        writeUsers = self.file.writeJsonFile(usersPath, users)

        # with open(usersPath, 'w') as usersFile:
        #     json.dump(users, usersFile, indent=4)
        if writeUsers['status'] == 200:
            print()
            print(" -- Signup Successful -- ")
        return user




