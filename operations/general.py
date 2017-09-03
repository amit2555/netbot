from base import BaseOperation, register
from automation import tasks 
from netbot.lib.common import passed, failed, IPADDRESS_RE
from netbot.lib.helpers import indent
import re


@register('GetFacts')
class GetFacts(BaseOperation):
    REGEX = [r'hostname', r'uptime', r'image', r'version', r'model', r'serial number', r'chassis']

    def __init__(self, utterance):
        super(GetFacts, self).__init__(utterance) 
        self.facts = []

    def run(self, *args, **kwargs):
        try:
            for device in self.devices:
                device_facts = tasks.get_facts(device)
                self.facts.append(device_facts)
        except Exception, e:
            return failed(str(e))

        output = ''
        for fact in self.facts:
            output += 'hostname: {} '.format(fact['hostname'])
            output += '\n'
            if self.attributes:
                output += ' '.join('{}: {}'.format(
                    attribute,
                    fact[attribute]) for attribute in self.attributes)
            else:
                output = ' '.join('{}: {} '.format(item, value) for item, value in fact.iteritems())
            output += '\n'
        return passed(indent(output))


@register('CheckConnectivity')
class CheckConnectivity(BaseOperation):
    REGEX = []

    def __init__(self, utterance):
        super(CheckConnectivity, self).__init__(utterance)
        self.destinations = re.findall(IPADDRESS_RE, self.utterance)

    def run(self, *args, **kwargs):
        if len(self.devices) != 1:
            return failed('You entered {} devices, required 1.', len(self.devices))

        output = ''
        output += 'Hostname: {}'.format(self.devices[0])
        output += '\n'
        for destination in self.destinations:
            response = tasks.check_connectivity(self.devices[0], destination)
            output += 'Destination: {} '.format(destination)
            output += response
            output += '\n'

        return passed(output)
