from flask import current_app
from tlapbot.db import get_db
from tlapbot.owncast_requests import send_chat, send_system_message
from tlapbot.redeems import (add_to_redeem_queue, add_to_counter, add_to_milestone, 
        check_apply_milestone_completion, milestone_complete, is_redeem_active)
from tlapbot.owncast_helpers import use_points, read_users_points, remove_emoji
from tlapbot.integration_helpers import (send_counter_integration, 
        send_list_integration, send_milestone_integration, send_note_integration)

def handle_redeem(message, user_id, user_name, authenticated):
    split_message = message[1:].split(maxsplit=1)
    redeem = split_message[0]
    if len(split_message) == 1:
        note = None
    else:
        note = split_message[1]

    if redeem not in current_app.config['REDEEMS']:
        # bypassed - if it's not a real redeem, don't answer at all.
        # send_chat("Can't redeem, redeem not found.")
        return
    if not is_redeem_active(redeem):
        # bypassed - if it's not active, don't even acknowledge it.
        # send_chat("Can't redeem, redeem is currently not active.")
        return
    if not authenticated:
        send_chat(f"You must be authenticated to use channel actions!")
        return

    db = get_db()
    redeem_type = current_app.config['REDEEMS'][redeem]["type"]
    redeem_action_id = current_app.config['REDEEMS'][redeem].get("action_id") #guard from missing action_ids
    points = read_users_points(db, user_id)

    # handle milestone first because it doesn't have a price
    if redeem_type == "milestone":
        if milestone_complete(db, redeem):
            send_chat(f"Can't redeem {redeem}, that milestone was already completed!")
        elif not note:
            send_chat(f"Cannot redeem {redeem}, no amount of points specified.")
        elif not note.isdigit():
            send_chat(f"Cannot redeem {redeem}, amount of points is not an integer.")
        elif int(note) > points:
            send_chat(f"Can't redeem {redeem}, you're donating more points than you have.")
        elif add_to_milestone(db, user_id, redeem, int(note)):
            send_chat(f"**{user_name}** succesfully donated to the **{redeem}** milestone!")
            if redeem_action_id is not None:
                send_milestone_integration(redeem, user_name, redeem_action_id, int(note))
            if check_apply_milestone_completion(db, redeem):
                send_chat(f"Milestone goal {redeem} complete!")
        else:
            send_chat(f"Redeeming milestone {redeem} failed.")
        return
    
    # handle redeems with price argument
    price = current_app.config['REDEEMS'][redeem]["price"]
    if not points or points < price:
        send_chat(f"Can't redeem {redeem}, you don't have enough points.")
        return

    if redeem_type == "counter":
        if add_to_counter(db, redeem) and use_points(db, user_id, price):
            send_system_message(f"**{user_name}** redeemed **{redeem}** for {price} points.")
            if redeem_action_id is not None:
                send_counter_integration(redeem, user_name, redeem_action_id, price)
        else:
            send_chat(f"Redeeming {redeem} failed.")
    elif redeem_type == "list":
        if (add_to_redeem_queue(db, user_id, redeem) and
                use_points(db, user_id, price)):
            send_system_message(f"**{user_name}** redeemed **{redeem}** for {price} points.")
            if redeem_action_id is not None:
                send_list_integration(redeem, user_name, redeem_action_id, price)
        else:
            send_chat(f"Redeeming {redeem} failed.")
    elif redeem_type == "note":
        if not note:
            send_chat(f"Cannot redeem {redeem}, no note included.")
            return
        if (add_to_redeem_queue(db, user_id, redeem, remove_emoji(note)) and
                use_points(db, user_id, price)):
            send_system_message(f"**{user_name}** redeemed **{redeem}** for {price} points.")
            if redeem_action_id is not None:
                send_note_integration(redeem, user_name, redeem_action_id, price, note)
        else:
            send_chat(f"Redeeming {redeem} failed.")
    else:
        send_chat(f"{redeem} not redeemed, type of redeem not found.")
