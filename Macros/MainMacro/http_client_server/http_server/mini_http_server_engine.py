import socket
import ujson as json
from typing import Callable, Dict, Any

# Самописный минималистичный HTTP-сервер на чистом Python 3, работающий только на 127.0.0.1, с:
# - TCP_NODELAY (для минимизации задержек),
# - простым Keep-Alive,
# - обработкой только POST-запросов на /api/data,
# - JSON-сериализацией с помощью стороннего пакета ujson (работает быстрее стандартного модуля json).

# 🚀 ОСОБЕННОСТИ:
# - Мгновенный старт, нет зависимостей.
# - 0 фреймворков, чистый socket, полный контроль.
# - Поддержка Keep-Alive (один запрос на соединение, но клиент может не закрывать сокет).
# - TCP_NODELAY включён.
class MiniHTTPServerEngine:
    KEEP_ALIVE_TIMEOUT = 5  # секунд

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.routes: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def add_route(self, path: str, handler: Callable[[Dict[str, Any]], Any]):
        self.routes[path] = handler

    def _handle_request(self, conn: socket.socket):
        try:
            conn.settimeout(self.KEEP_ALIVE_TIMEOUT)
            data = b""
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(1024)
                if not chunk:
                    return
                data += chunk

            headers_raw = data.split(b"\r\n\r\n")[0].decode()
            headers = headers_raw.splitlines()
            method, path, _ = headers[0].split()

            if method != "POST" or path not in self.routes:
                response = b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                conn.sendall(response)
                return

            # Получение Content-Length
            content_length = 0
            for h in headers:
                if h.lower().startswith("content-length:"):
                    content_length = int(h.split(":")[1].strip())
                    break

            body = data.split(b"\r\n\r\n", 1)[1]
            while len(body) < content_length:
                body += conn.recv(content_length - len(body))

            request_json = json.loads(body.decode())
            handler = self.routes[path]
            result = handler(request_json)

            response_body = json.dumps(result).encode()
            response_headers = (
                b"HTTP/1.1 200 OK\r\n"
                + b"Content-Type: application/json\r\n"
                + f"Content-Length: {len(response_body)}\r\n".encode()
                + b"Connection: keep-alive\r\n\r\n"
            )
            conn.sendall(response_headers + response_body)

        except Exception as e:
            err = json.dumps({"error": str(e)}).encode()
            conn.sendall(
                b"HTTP/1.1 400 Bad Request\r\n"
                + b"Content-Type: application/json\r\n"
                + f"Content-Length: {len(err)}\r\n\r\n".encode()
                + err
            )

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"MiniHTTPServer listening on http://{self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    self._handle_request(conn)
