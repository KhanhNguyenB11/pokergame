import socket

# Server address and port (replace with actual server IP if needed)
HOST = 'localhost'
PORT = 65432

def connect_and_join(room_id, name):
    """Connects to the server, sends room ID, and receives confirmation."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Send formatted message (room ID + message)
        message = f"JOIN {room_id} AS {name}"
        s.sendall(message.encode())
        # Receive confirmation message
        data = s.recv(1024).decode()
        print(data)  # Print confirmation message from server
        if data.find("host") != -1:
            message = input("Enter your message (or 'quit' to disconnect): ")
            if message.lower() == 'quit':
                return s
            formatted_message = f"{room_id} {name} {message}"
            s.sendall(formatted_message.encode())
        print("Waiting for others player turn...")
        # Game loop to maintain connection and send/receive messages
        while True:
            data = s.recv(1024).decode()
            if not data:
                continue
            print(f"{data}")
            if data.startswith(f"{name} TURN") or data == "Enter the amount":
                message = input("Enter your message (or 'quit' to disconnect): ")
                if message.lower() == 'quit':
                    return s
                # Send formatted message (room ID + sender + message)
                formatted_message = f"ACTION {name} {message}"
                s.sendall(formatted_message.encode())





if __name__ == '__main__':
    # Get room ID from user
    while True:
        try:
            name = input("Please enter your name: ")
            room_id = int(input("Enter room ID to join: "))
            break
        except ValueError:
            print("Invalid room ID. Please enter a number.")

    # Connect and join the room
    con = connect_and_join(room_id, name)
    con.close()

    # Close the socket when done
