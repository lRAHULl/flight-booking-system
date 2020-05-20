import os
import json
from datetime import datetime
from send_email import sendMail
from utils import FileIOUtils

class BookingSystem:
    """
        @Author Rahul
        
        A Simple Flight Booking System
        ==============================
        Methods
        -------
        1. getAllFlights
        2. getFlights
        3. getFlightsById
        4. bookAFlight
        5. showBookedFlights
        6. cancelBooking
    """

    def __init__(self):
        self.file = FileIOUtils()


    def getAllFlights(self):
        """
            Get All Flights available
        """

        self.flights = []
        flightsPath = 'data/flights.json'

        out = self.file.readJsonFile(flightsPath)

        if out['status'] == 200:
            self.flights = out['data']
        else:
            print(out['data'])


        # if os.path.exists(flightsPath):
        #     with open(flightsPath) as flightsFile:
        #         try:
        #             self.flights = json.load(flightsFile)
        #         except json.decoder.JSONDecodeError:
        #             print('JSON error')
        #         except:
        #             print('something went wrong!')
        # else:
        #     print('No Flight-registry found - No Flights available')
    
    def getFlights(self, source: str, destination: str, display = False):
        """
            Get Flights with source and destination
        """

        if not source or not destination:
            print('Not a valid Input')

        self.getAllFlights()

        availableFlights = dict()
        for flight in self.flights:
            if flight['source'].lower() == source.lower() and flight['destination'].lower() == destination.lower():
                availableFlights[flight['id']] = flight

        if display and availableFlights:
            print()
            print("------------------------------------ Available Flights -------------------------------------------")
            print('id\t\tsource\t\tdestination\t\tdate\t\tavailable')
            for flightId, flight in availableFlights.items():
                print(f'{flight["id"]}\t\t{flight["source"]}\t\t{flight["destination"]}\t\t{flight["date"]}\t\t{flight["available"]}')
            print("-------------------------------------------------------------------------------------------------")

        if display and not availableFlights:
            print(" --  No Flights Available -- ")
        return (self.flights, availableFlights)

    def getFlightById(self, source: str, destination: str, flightId: int):
        """
            Get Flight that has the give source, destination and id
        """
        (_, availableFlights) = self.getFlights(source, destination)

        if flightId not in availableFlights:
            return None

        flight = availableFlights[flightId]
        return flight

    def bookAFlight(self, userEmail: str):
        """
            Book a flight for a given user
        """
        source = input("Enter the source: ")
        destination = input("Enter the destination: ")

        if not source or not destination:
            print("Invalid Inputs")
            return

        allFlights, availableFlights = self.getFlights(source, destination, display=True)

        if not availableFlights:
            return
        flightId = input("Enter the Flight Id: ")
        if not flightId.isdigit(): 
            print("invalid Input")
            return

        flightId = int(flightId)

        flight = self.getFlightById(source, destination, flightId)

        if not flight:
            print('No Flight with the given id found!')
            return

        if flight["available"] <= 0:
            print("No Seats Available -- Try another Flight")
            return

        bookingsPath = 'data/bookings.json'
        flightsPath = 'data/flights.json'
        bookingId = f'{userEmail}-{flight["id"]}-{flight["date"]}'

        bookings = []

        out = self.file.readJsonFile(bookingsPath)

        if out['status'] == 200:
            bookings = out['data']
        # if os.path.exists(bookingsPath):
        #     with open(bookingsPath) as bookingsFile:
        #         try:
        #             bookings = json.load(bookingsFile)
        #             if not bookings:
        #                 bookings = []
        #         except json.decoder.JSONDecodeError:
        #             print('JSON error')
        #         except:
        #             print('something went wrong!')
        # else:
        #     print('No Booking-registry found - No Bookings available')

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


        for flight in allFlights:
            if flight["id"] == flightId:
                flight["available"] -= 1

        
        writeBookings = self.file.writeJsonFile(bookingsPath, bookings)

        writeFlights = self.file.writeJsonFile(flightsPath, allFlights)        
        # with open(bookingsPath, 'w') as bookingsFile:
        #     json.dump(bookings, bookingsFile, indent=4)

        # with open(flightsPath, 'w') as flightsFile:
        #     json.dump(allFlights, flightsFile, indent=4)

        if writeBookings['status'] == 200 and writeFlights['status'] == 200:
            print('Activating Mail Service')
            sendMail(userEmail, bookingId, flight, True)
            print("Booking Successful")
            print()
        else:
            print('something went wrong')

    def showBookedFlights(self, userEmail: str, display = False, methodCall=False):
        """
            Show Booked flights for a given user
        """
        bookingsPath = 'data/bookings.json'
        bookings = []

        out = self.file.readJsonFile(bookingsPath)

        if out['status'] == 200:
            bookings = out['data']
        else:
            if not methodCall:
                print(out['data'])
        # if os.path.exists(bookingsPath):
        #     with open(bookingsPath) as bookingsFile:
        #         try:
        #             bookings = json.load(bookingsFile)
        #             if not bookings:
        #                 bookings = []
        #         except json.decoder.JSONDecodeError:
        #             print('JSON error')
        #         except:
        #             print('something went wrong!')
        # else:
        #     if not methodCall:
        #         print('No Booking-registry found - No Bookings available')

        userBookings = []
        for booking in bookings:
            if booking["email"] == userEmail and booking["isActive"]:
                # print(booking)
                userBookings.append(booking)

        if not userBookings:
            print(" -- No Bookings Found for the user -- ")

        if display and userBookings:
            print("------------------------------------ Your Bookings -------------------------------------------")
            print('id\t\tBooking Code\t\t\tsource\t\tdestination\t\tdate\t\tFlight Number')
            print("----------------------------------------------------------------------------------------------")
            for booking in userBookings:
                print(f'{booking["id"]}\t\t{booking["bookingId"]}\t\t\t{booking["flight"]["source"]}\t\t{booking["flight"]["destination"]}\t\t{booking["flight"]["date"]}\t\tflight-{booking["flight"]["id"]}')

        return (bookings, userBookings)

    def cancelBooking(self, userEmail: str, bookingId: int):
        """
            Cancel a flight for a given user
        """
        allBookings, userBookings = self.showBookedFlights(userEmail, methodCall=True)

        dateFormat = "%d-%m-%Y"
        notFound = True
        cancelledBooking = None
        for booking in allBookings:
            if booking["email"] == userEmail and booking["id"] == bookingId and booking["isActive"]:
                departureDate = datetime.strptime(booking["flight"]["date"], dateFormat).date()
                todayDate = datetime.now().date()
                notFound = False
                if departureDate <= todayDate:
                    print('Cannot cancel the booking, because the departure date is too close.')
                    return
                booking["isActive"] = False
                cancelledBooking = booking
        if notFound:
            print('Not a valid bookingId')
            return

        bookingsPath = 'data/bookings.json'
        if cancelledBooking:
            writeBookings = self.file.writeJsonFile(bookingsPath, allBookings)
            # with open(bookingsPath, 'w') as bookingsFile:
            #     json.dump(allBookings, bookingsFile, indent=4)
            print('Activating Mail Service')
            sendMail(userEmail, cancelledBooking["bookingId"], cancelledBooking["flight"], False)
            print(" -- Flight Cancellation successful -- ")

