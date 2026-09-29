
from T0_TranscriptionProcessorsController import T0_TranscriptionProcessorsController
from mini_http_server_engine import MiniHTTPServerEngine

# Обёртка вокруг самописного движка. Сосредоточена на импорте бизнес-логики и вызове бизнес-методов.
class OfficeMacroHTTPServer:
    def __init__(self):
        self.server_engine = MiniHTTPServerEngine()
        self.transcriptionProcessorsController = T0_TranscriptionProcessorsController()

        self._register_routes()
        self._warm_up()

    def _register_routes(self):
        self.server_engine.add_route("/api/data", self.process_transcriptions)
        # Можно добавлять ещё обработчики
        # self.server.add_route("/ping", self.ping)

    # def ping(self, _):
    #     return {"pong": True}

    def _warm_up(self):
        """Прогрев контроллера для устранения задержек первого вызова."""
        print("[Server] 🔥 Прогрев контроллера...")
        try:
            dummy_data = {
                "data": [
                    ["[kæt]", ["[kæt]"]]  # кортеж (в json - список) из paragraph и списка его text_portions
                ],
                "lang": "deu"
            }
            _ = self.process_transcriptions(dummy_data)
            # res = self.process_transcriptions(dummy_data)
            # print(res)
            print("[Server] ✅ Прогрев завершён")
        except Exception as e:
            print(f"[Server] ⚠️ Прогрев не удался: {e}")

    def process_transcriptions(self, request_json):
        data = request_json.get("data")
        lang = request_json.get("lang")
        if data is None or lang is None:
            return {"error": "Missing 'data' or 'lang' in request"}, 400
        # Движок автоматиески сериализует результат в json
        return self.transcriptionProcessorsController.process_transcriptions(data, lang)

    def run(self):
        self.server_engine.run()


if __name__ == '__main__':
    server = OfficeMacroHTTPServer()
    server.run()
