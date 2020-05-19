from test import BookingSystem

# email = 
b = BookingSystem()
while True:
    print('1. Get Flights\n2. Book Flight\n3. Get Bookings\n4. Cancel Bookings\n5. Exit\n')
    inp = input('Enter the Choice: ')

    if inp == '1':
        source = input('Enter the pickup city: ')
        destination = input('Enter the Destination city: ')
        b.getFlights(source, destination, display=True)
    elif inp == '2':
        email = input('Enter your email: ')
        flightId = int(input('Enter the flightId: '))
        b.bookAFlight(email, flightId)
    elif inp == '3':
        email = input('Enter your email: ')
        b.showBookedFlights(email)
    elif inp == '4':
        email = input('Enter your email: ')
        flightId = int(input('Enter the flightId: '))
        b.cancelBooking(email, flightId)
    else:
        break
        