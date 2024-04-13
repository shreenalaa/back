from flask import jsonify
from app import app

from app import db
from models import LostItem, FoundItem
from notifications import send_sms

def match_items():
    # Retrieve all lost and found items from the database
    lost_items = LostItem.query.all()
    found_items = FoundItem.query.all()

    # Compare each lost item with each found item
    for lost_item in lost_items:
        for found_item in found_items:
            # Compare items based on their attributes (e.g., description, category, date, location)
            if (lost_item.category == found_item.category and
                lost_item.description == found_item.description and
                lost_item.date == found_item.date and
                lost_item.location == found_item.location):
                # Notify the user associated with the lost item
                recipient_number = lost_item.user.phone_number
                message = f"Your lost item ({lost_item.description}) has been found!"
                send_sms(recipient_number, message)

                # Optionally, update the database to mark the found item as matched
                found_item.matched = True
                db.session.commit()

# Call the match_items function to perform item matching
match_items()
