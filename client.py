import socket
import ssl

# Define the client key, certificate, server certificate, port, and hostname
client_key = 'client.key'
client_cert = 'client.crt'
server_cert = 'server.crt'
port = 8080
hostname = '127.0.0.1'

# Create an SSL context with the specified protocol and CA file
context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=server_cert)

# Load the client's certificate chain and private key
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.load_verify_locations(cafile=server_cert)

# Set the verification mode and disable older TLS versions
context.verify_mode = ssl.CERT_REQUIRED
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

# Create a socket connection to the specified hostname and port
with socket.create_connection((hostname, port)) as sock:
    # Wrap the socket with the SSL context
    with context.wrap_socket(sock, server_side=False, server_hostname=hostname) as ssock:
        # Print the SSL/TLS version
        print(ssock.version())

        # Prompt the user to enter a message
        message = input("Please enter your message: ")

        # Send the message to the server
        ssock.send(message.encode())

        # Receive and print the response from the server
        receives = ssock.recv(1024)
        print(receives)