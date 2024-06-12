import socket
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 20000        # Port to listen on (non-privileged ports are > 1023)
JSON_FILE = 'scores.json'

def update_scores(player_name, score):
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            scores = data['scores']
    except FileNotFoundError:
        scores = []

    # Check if the player already exists and update the score
    player_exists = False
    for entry in scores:
        if entry['name'] == player_name:
            entry['score'] = score
            player_exists = True
            break

    # If player does not exist, add a new entry
    if not player_exists:
        scores.append({'name': player_name, 'score': score})

    # Save the updated scores back to the JSON file
    with open(JSON_FILE, 'w') as file:
        json.dump({'scores': scores}, file, indent=2)

def handle_client(conn, addr):
    print(f'Connected by {addr}')

    # Receive data from client
    player_name = conn.recv(1024).decode().strip()
    score = str(conn.recv(1024).decode().strip())
    score = int(score)
    # Update scores
    update_scores(player_name, score)

    # Send confirmation to client
    conn.sendall(b'Score updated successfully')

    # Close connection
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)
