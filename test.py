import os, json

class BookingSystem:
    """
        Hello World
    """


    def getAllFlights(self):
        """
            Get Flights
        """

        self.flights = []
        flightsPath = 'data/flights.json'

        if os.path.exists(flightsPath):
            with open(flightsPath) as flightsFile:
                try:
                    self.flights = json.load(flightsFile)
                    # print(self.flights)
                except json.decoder.JSONDecodeError:
                    print('JSON error')
                except:
                    print('something went wrong!')
        else:
            print('No Flight-registry found - No Flights available')
    
    def getFlights(self, source: str, destination: str, display = False):
        """
            Get Flights with source and destination
        """

        if not source or not destination:
            print('Not a valid Input')

        self.source = source
        self.destination = destination

        self.getAllFlights()

        availableFlights = dict()
        for flight in self.flights:
            if flight['source'].lower() == source.lower() and flight['destination'].lower() == destination.lower():
                availableFlights[flight['id']] = flight

        if display and availableFlights:
            print('id\t\tsource\t\tdestination\t\tdate\t\tavailable')
            for flightId, flight in availableFlights.items():
                print(f'{flight["id"]}\t\t{flight["source"]}\t\t{flight["destination"]}\t\t{flight["date"]}\t\t{flight["available"]}')

        return availableFlights

    
    def getFlightById(self, flightId):
        """

        """
        availableFlights = self.getFlights(self.source, self.destination)

        if flightId not in availableFlights:
            return None

        flight = availableFlights[flightId]
        print(flight)
        return flight

    def bookAFlight(self, userEmail, flightId):
        """

        """
        flight = self.getFlightById(flightId)

        if not flight:
            print('No Flight with the given id found!')
            return None

        bookingsPath = 'data/bookings.json'
        bookingId = f'{userEmail}-{flight["id"]}-{flight["date"]}'

        bookings = []
        if os.path.exists(bookingsPath):
            with open(bookingsPath) as bookingsFile:
                try:
                    bookings = json.load(bookingsFile)
                    if not bookings:
                        bookings = []
                except json.decoder.JSONDecodeError:
                    print('JSON error')
                except:
                    print('something went wrong!')
        else:
            print('No Booking-registry found - No Bookings available')

        id = 1
        if bookings:
            id = bookings[-1]['id'] + 1

        newBooking = dict()

        newBooking['id'] = id
        newBooking['bookingId'] = bookingId
        newBooking['flight'] = flight
        newBooking['email'] = userEmail
        newBooking['isActive'] = True

        bookings.append(newBooking)

        with open(bookingsPath, 'w') as bookingsFile:
            json.dump(bookings, bookingsFile, indent=4)

    def showBookedFlights(self, userEmail):
        bookingsPath = 'data/bookings.json'
        bookings = []
        if os.path.exists(bookingsPath):
            with open(bookingsPath) as bookingsFile:
                try:
                    bookings = json.load(bookingsFile)
                    if not bookings:
                        bookings = []
                except json.decoder.JSONDecodeError:
                    print('JSON error')
                except:
                    print('something went wrong!')
        else:
            print('No Booking-registry found - No Bookings available')

        userBookings = []
        for booking in bookings:
            if booking["email"] == userEmail and booking["isActive"]:
                print(booking)
                userBookings.append(booking)

        return userBookings

    def cancelBooking(self, userEmail, flightId):
        bookingsPath = 'data/bookings.json'
        bookings = []
        if os.path.exists(bookingsPath):
            with open(bookingsPath) as bookingsFile:
                try:
                    bookings = json.load(bookingsFile)
                    if not bookings:
                        bookings = []
                except json.decoder.JSONDecodeError:
                    print('JSON error')
                except:
                    print('something went wrong!')
        else:
            print('No Booking-registry found - No Bookings available')

        for booking in bookings:
            if booking["email"] == userEmail and booking["flight"]["id"] == flightId:
                booking["isActive"] = False

        with open(bookingsPath, 'w') as bookingsFile:
            json.dump(bookings, bookingsFile, indent=4)

    












# class Flights:
#     def __init__(self, flights):
#         self.flights = []
#         for flight in flights:
#             if isinstance(flight, {}.__class__):
#                 self.flights.append(Flight(**flight))

# class Flight:
#     def __init__(self, id, source, destination, date, available):
#         self.id = id;
#         self.source = source
#         self.destination = destination
#         self.date = date
#         self.available = available

# class Booking:
#     def __init__(self, id, flight, date, passenger):
#         self.id = id
#         self.flight = flight
#         self.date = date
#         self.passenger = passenger

# flightsFile = open('data/flights.json')
# d = list(**json.load(flightsFile))
# print(d)
# flightsFile.close()