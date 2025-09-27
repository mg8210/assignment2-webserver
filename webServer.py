# import socket module #
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  serverSocket.bind(("", port))
  serverSocket.listen(1)

  while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
      message = connectionSocket.recv(1024).decode()
      if not message:
        connectionSocket.close()
        continue

      # Parse the request line safely
      request_line = message.splitlines()[0] if message else ""
      parts = request_line.split()
      if len(parts) < 2:
        connectionSocket.close()
        continue

      path = parts[1]
      if path == "/":
        path = "/index.html"

      # Read file body as bytes
      with open(path[1:], "rb") as f:
        body = f.read()

      # ---- Build 200 OK response (status line first, then headers) ----
      headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=UTF-8",
        f"Content-Length: {len(body)}",
        "Server: SimplePythonServer/1.0",
        "Connection: close",
      ]
      response = ("\r\n".join(headers) + "\r\n\r\n").encode() + body

      # Single send: headers + body
      connectionSocket.send(response)
      connectionSocket.close()

    except FileNotFoundError:
      body = (b"<html><head><title>404 Not Found</title></head>"
              b"<body><h1>404 Not Found</h1>"
              b"<p>The requested file was not found.</p></body></html>")
      headers = [
        "HTTP/1.1 404 Not Found",
        "Content-Type: text/html; charset=UTF-8",
        f"Content-Length: {len(body)}",
        "Server: SimplePythonServer/1.0",
        "Connection: close",
      ]
      response = ("\r\n".join(headers) + "\r\n\r\n").encode() + body
      connectionSocket.send(response)
      connectionSocket.close()
    except Exception:
      # On any other error, close cleanly
      connectionSocket.close()

  #serverSocket.close()
  #sys.exit()

if __name__ == "__main__":
  webServer(13331)
