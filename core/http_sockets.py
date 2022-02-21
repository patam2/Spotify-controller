import socket
import ssl
import json


def CallBack():
    sock = socket.socket()
    sock.bind(('localhost', 8888))
    sock.listen()
    c, a = sock.accept()
    recv = c.recv(1024)

    return recv.split(b'/callback?code=')[1].split(b' HTTP/1.1')[0].decode()

class SocketClient:
    def __init__(self, token: str, host: str) -> None:
        self.host = host
        self.token = token
        self.socket_sess = self.create_sock()

    def _apply_headers(self, method, data):
        return (
            f"Host: {self.host}\r\n"
            f'Authorization: {self.token}\r\n'
            "Accept: application/json\r\n"
            "Content-Type: %s"
            f"Content-Length: {0 if not data else len(json.dumps(data))}\r\n" % ("application/x-www-form-urlencoded\r\n" if method == 'POST' and self.host == 'accounts.spotify.com' else 'application/json\r\n')
        )

    def create_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = ssl.create_default_context().wrap_socket(
            sock,
            server_side=False,
            server_hostname=self.host,
            do_handshake_on_connect=True,
        )
        sock.connect((self.host, 443))
        return sock


    def request(self, method, url, data=None):
        self.socket_sess.sendall(
            str.encode(
                "%s %s HTTP/1.1\r\n%s\r\n%s\r\n\r\n"
                % (method, url, self._apply_headers(method, data), (json.dumps(data) if data else ""))
            )
        )

        data, recv = self.socket_sess.recv(4096).split(b'\r\n\r\n', 1)

        content_length = int(data.split(b'Content-Length: ')[1].split(b'\r\n')[0])
        while len(recv) < content_length:
            recv += self.socket_sess.recv(4096)

        if b'HTTP/1.1 303' in data:
            return data.split(b'location: ')[1].split(b'\r\nset-cookie')[0]

        try:
            return json.loads(recv.decode()) if recv else True
        except:
            return False
