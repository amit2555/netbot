from base import BaseOperation, register
from automation import tasks
from netbot.lib.common import passed, failed
import time
import re


THRESHOLD = 100


@register('TrafficDrain')
class TrafficDrain(BaseOperation):
    REGEX = []

    def __init__(self, utterance):
        super(TrafficDrain, self).__init__(utterance)
        self.intent = None

    def _guess_intent(self):
        SHIFT_AWAY = 'away|drain'
        SHIFT_BACK = 'back|return|restore'

        if re.search(SHIFT_AWAY, self.utterance):
            return 'away'
        if re.search(SHIFT_BACK, self.utterance):
            return 'back'

    def run(self, *args, **kwargs):
        if len(self.devices) > 1:
            return failed('Sorry, I cannot drain or return traffic from/to more than one device.')

        self.intent = self._guess_intent()
        if not self.intent:
            return failed('Sorry, I could not determine whether to drain traffic or not.')

        if self.intent == 'away':
            return self.shift_away(check_traffic_level=True)
        if self.intent == 'back':
            return self.shift_back()

    def _get_commands(self):
        commands = list()
        commands = ["router ospf 1"]

        if self.intent == "away":
            commands.append("max-metric router-lsa external-lsa include-stub summary-lsa")
        if self.intent == "back":
            commands.append("no max-metric router-lsa")

        commands.append("do copy running-config startup-config")
        return commands

    def shift_away(self, check_traffic_level=False):
        commands = self._get_commands()
        tasks.apply_config(self.devices[0], commands)

        if not check_traffic_level:
            return passed('Traffic drained from device {}', self.devices[0]) 
 
        count = 1
        while count <= 3:
            time.sleep(5)
            pps = tasks.get_device_traffic(self.devices[0])
            if pps > THRESHOLD:
                count += 1
            else:
                return passed('Traffic drained from device {} - currently {} packets/sec', self.devices[0], pps) 
        return failed('Traffic not drained from device {} - currently {} packets/sec.', self.devices[0], pps)
 
    def shift_back(self, check_traffic_level=False):
        commands = self._get_commands()
        tasks.apply_config(self.devices[0], commands)

        if not check_traffic_level:
            return passed('Traffic returned to device {}', self.devices[0]) 

        count = 1
        while count <= 3:
            time.sleep(5)
            pps = tasks.get_device_traffic(self.devices[0])
            if pps < THRESHOLD:
                count += 1
            else:
                return passed('Traffic restored to device {} - currently {} packets/sec.', self.devices[0], pps) 
        return failed('Traffic not restored to device {} - currently {} packets/sec.', self.devices[0], pps)

