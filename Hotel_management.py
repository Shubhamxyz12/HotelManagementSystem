import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass@word1",
    database="hotel_db"
)

cursor = db.cursor()

#CREATE Guest
def add_guest(name, phone, email):
    cursor.execute("INSERT INTO guests (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
    db.commit()
    print("✅ Guest added!")

# CREATE Room
def add_room(room_type, price):
    cursor.execute("INSERT INTO rooms (room_type, price) VALUES (%s, %s)", (room_type, price))
    db.commit()
    print("✅ Room added!")

# CREATE Booking
def book_room(guest_id, room_id, check_in, check_out):
    cursor.execute("SELECT is_available FROM rooms WHERE room_id = %s", (room_id,))
    if cursor.fetchone()[0]:
        cursor.execute("INSERT INTO bookings (guest_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)",
                       (guest_id, room_id, check_in, check_out))
        cursor.execute("UPDATE rooms SET is_available = FALSE WHERE room_id = %s", (room_id,))
        db.commit()
        print("✅ Booking confirmed!")
    else:
        print("❌ Room not available.")

# READ Bookings
def view_bookings():
    cursor.execute("SELECT * FROM bookings")
    for row in cursor.fetchall():
        print(row)

# UPDATE Booking Dates
def update_booking(booking_id, new_check_in, new_check_out):
    cursor.execute("UPDATE bookings SET check_in = %s, check_out = %s WHERE booking_id = %s",
                   (new_check_in, new_check_out, booking_id))
    db.commit()
    print("🔄 Booking updated!")

# DELETE Booking
def cancel_booking(booking_id):
    cursor.execute("SELECT room_id FROM bookings WHERE booking_id = %s", (booking_id,))
    room_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
    cursor.execute("UPDATE rooms SET is_available = TRUE WHERE room_id = %s", (room_id,))
    db.commit()
    print("🗑️ Booking cancelled.")

# MENU
def menu():
    while True:
        print("\n📋 Hotel Booking System")
        print("1. Add Guest")
        print("2. Add Room")
        print("3. Book Room")
        print("4. View Bookings")
        print("5. Update Booking")
        print("6. Cancel Booking")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Guest Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            add_guest(name, phone, email)
        elif choice == "2":
            room_type = input("Room Type: ")
            price = int(input("Price: "))
            add_room(room_type, price)
        elif choice == "3":
            guest_id = int(input("Guest ID: "))
            room_id = int(input("Room ID: "))
            check_in = input("Check-in Date (YYYY-MM-DD): ")
            check_out = input("Check-out Date (YYYY-MM-DD): ")
            book_room(guest_id, room_id, check_in, check_out)
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            booking_id = int(input("Booking ID: "))
            new_check_in = input("New Check-in Date (YYYY-MM-DD): ")
            new_check_out = input("New Check-out Date (YYYY-MM-DD): ")
            update_booking(booking_id, new_check_in, new_check_out)
        elif choice == "6":
            booking_id = int(input("Booking ID to cancel: "))
            cancel_booking(booking_id)
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice!")

menu()
cursor.close()
db.close()
