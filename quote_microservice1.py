import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5560")

print("Quote service running on port 5560...")

quotes = {
    "fitness": [
        "Results happen over time, not overnight. Work hard, stay hard.",
        "Sweat is just fat crying.",
        "Your mind is your strongest muscle."
    ],
    "productivity": [
        "Small progress is still progress.",
        "Discipline beats motivation.",
        "Focus on being productive, not busy."
    ],
    "gaming": [
        "Victory belongs to the persistent.",
        "Level up your mindset before your character.",
        "Every expert was once a beginner."
    ],
    "general": [
        "Stay consistent and trust the process.",
        "Success is built daily.",
        "Keep going. You’re closer than you think."
    ]
}

while True:
    request = socket.recv_json()

    action = request.get("action")

    if action == "random":
        all_quotes = [q for category in quotes.values() for q in category]
        quote = random.choice(all_quotes)
        socket.send_json({"status": "success", "quote": quote})

    elif action == "by_category":
        category = request.get("category")

        if category in quotes:
            quote = random.choice(quotes[category])
            socket.send_json({"status": "success", "quote": quote})
        else:
            socket.send_json({
                "status": "error",
                "message": "Invalid category"
            })

    else:
        socket.send_json({
            "status": "error",
            "message": "Invalid action"
        })