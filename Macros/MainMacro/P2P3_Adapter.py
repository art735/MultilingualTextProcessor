# -*- coding: utf-8 -*-

import PyVerUtils
import http_client

try:
    # Python 2
    import UnoUtils
except ImportError:
    # Python 3
    UnoUtils = None




# multilingualTextProcessorPathsImporter = MultilingualTextProcessorPathsImporter()
# multilingualTextProcessorPathsImporter.import_paths()

# from ZMQClient import ZMQClient

class P2P3_Adapter:
    def __init__(self):
        # self.client = zmqclient.ZMQClient()
        self.t0_TranscriptionProcessorsController = None

    def process_transcriptions(self, data, lang):
        if PyVerUtils.is_python2():
            # UnoUtils.show_messagebox("Info", 'Python2 is detected')
            # method_name = inspect.currentframe().f_code.co_name
            # result = P3_Runner.run_python3_script(method_name)
            result = http_client.process_transcriptions(data, lang)

            # Если сервер не ответил или он просто не запущен
            if "error" in result:
                UnoUtils.show_messagebox('Error', 'No response from the http-server. Probably it is not started.')
                return None

        else:
            from T0_TranscriptionProcessorsController import T0_TranscriptionProcessorsController
            if self.t0_TranscriptionProcessorsController is None:
                self.t0_TranscriptionProcessorsController = T0_TranscriptionProcessorsController()
            result = self.t0_TranscriptionProcessorsController.process_transcriptions(data, lang)
        return result


if __name__ == '__main__':
    p2p3_Adapter = P2P3_Adapter()
    data = [("[kæt]", ["[kæt]"])]
    lang = 'deu'
    res = p2p3_Adapter.process_transcriptions(data, lang)
    print(res)
