from tlapbot.integration_requests import send_integration
    
def send_milestone_integration(redeem, caller, action_id, points):
    send_integration(redeem, action_id, {"type": "milestone",
                                         "redeem": redeem,
                                         "caller": caller,
                                         "points": points})

def send_counter_integration(redeem, caller, action_id, points):
    send_integration(redeem, action_id, {"type": "counter",
                                         "redeem": redeem,
                                         "caller": caller,
                                         "points": points})

def send_list_integration(redeem, caller, action_id, points):
    send_integration(redeem, action_id, {"type": "list",
                                        "redeem": redeem,
                                        "caller": caller,
                                        "points": points})

def send_note_integration(redeem, caller, action_id, points, note):
    send_integration(redeem, action_id, {"type": "note",
                                         "redeem": redeem,
                                         "caller": caller,
                                         "points": points,
                                         "note": note})