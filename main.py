from booking import BookingSystem
from user import User

user = None
u = User()
b = BookingSystem()
while True:
    print()
    print("-------------------------- Flight Booking System ---------------------------")
    print()
    if not user:
        print('1. Login\n2. Sign Up\n3. Exit\n')
        choice = input('Enter the Choice: ')
        
        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user = u.login(email, password)       
        elif choice == '2':
            newUser = {}
            newUser["name"] = input("Enter your Full name: ")
            newUser["email"] = input("Enter your email: ")
            newUser["password"] = input("Enter your password: ")
            user = u.signup(newUser)

        else:
            break

    else:
        print(f'Hello {user["name"]}({user["email"]})')
        print()
        print('1. Get Flights\n2. Book Flight\n3. Get Bookings\n4. Cancel Bookings\n5. Logout\n6. Exit\n')
        choice = input('Enter the Choice: ')
        
        if choice == '1':
            source = input('Enter the pickup city: ')
            destination = input('Enter the Destination city: ')
            if not source or not destination:
                print("Invalid Input")
                continue
            b.getFlights(source, destination, display=True)
        elif choice == '2':
            b.bookAFlight(user["email"])
        elif choice == '3':
            b.showBookedFlights(user["email"], True)
        elif choice == '4':
            bookingId = input('Enter the bookingId: ')
            if not bookingId.isdigit():
                print("inValid input")
                continue
            bookingId = int(bookingId)
            b.cancelBooking(user["email"], bookingId)
        elif choice == '5':
            user = None
            print("Successfully Logged Out")
        else:
            break
        