from base import BaseOperation, register
from automation import tasks
from netbot.lib.common import passed, failed, IPADDRESS_RE
import re


@register('GetBGPParameters')
class GetBGPParameters(BaseOperation):
    REGEX = [r'asn', r'router id']

    def __init__(self, utterance):
        super(GetBGPParameters, self).__init__(utterance)
        self.bgp_config = []

    def run(self, *args, **kwargs):
        if not self.attributes:
            return failed('No BGP parameters given')

        try:
            for device in self.devices:
                bgp_config = tasks.get_bgp_config(device)
                self.bgp_config.append(bgp_config)
        except Exception, e:
            return failed(str(e))

        output = ''
        for index, bgp_config in enumerate(self.bgp_config):
            output += 'hostname: {} '.format(self.devices[index].upper())
            output += '\n'
            output += ' '.join('{}: {}'.format(
                attribute, bgp_config[attribute]) for attribute in self.attributes)
            output += '\n'

        return passed(output)


@register('GetBGPNeighbor')
class GetBGPNeighbor(BaseOperation):
    REGEX = [r'advertised', r'received', r'state', r'remote as(n)?', r'description', r'holdtime',
             r'keepalive', r'neighbor']

    def __init__(self, utterance):
        super(GetBGPNeighbor, self).__init__(utterance)
        self.neighbors = re.findall(IPADDRESS_RE, self.utterance)
        self.bgp_data = []

    def run(self, *args, **kwargs):
        if not self.attributes:
            return failed('No BGP parameters given')

        try:
            for device in self.devices:
                bgp_neighbors = tasks.get_bgp_neighbors_state(device, self.neighbors)
                self.bgp_data.append(bgp_neighbors)
        except Exception, e:
            return failed(str(e))
        
        output = ''
        for index, bgp_data in enumerate(self.bgp_data):
            output += 'hostname: {} '.format(self.devices[index].upper())
            output += '\n'
            for item in bgp_data:
                output += ' '.join('{}: {}'.format(
                    attribute, item[attribute]) for attribute in self.attributes)
                output += '\n'

        return passed(output)
