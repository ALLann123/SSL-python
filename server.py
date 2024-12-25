import socket
import ssl

# Paths to certificates and keys
client_cert = 'client.crt'
server_key = 'server.key'
server_cert = 'server.crt'

# Server port
port = 8080

# Create an SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile=client_cert)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)

# Restrict to secure protocols
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

# Create a TCP socket and bind it
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('', port))
    sock.listen(1)
    print(f"Server listening on port {port}...")

    # Wrap the socket with SSL
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            print("Waiting for a connection...")
            conn, addr = ssock.accept()
            print(f"Connection established with {addr}")

            try:
                # Receive message
                message = conn.recv(1024).decode()
                print(f"Received: {message}")

                # Process and send a response
                capitalized_message = message.upper()
                conn.send(capitalized_message.encode())
                print(f"Sent: {capitalized_message}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                # Close the connection
                conn.close()
                print(f"Connection with {addr} closed.")
