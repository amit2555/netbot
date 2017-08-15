from base import BaseOperation
from automation import tasks 
from netbot.lib.common import passed, failed


class GetFacts(BaseOperation):
    REGEX = [r'hostname', r'uptime', r'image', r'version', r'model', r'serial number', r'chassis']

    def __init__(self, devices):
        super(GetFacts, self).__init__(devices) 
        self.facts = []

    def __call__(self, attributes=None):
        attributes = self._sanitize_attributes(attributes)

        try:
            for device in self.devices:
                device_facts = tasks.get_facts(device)
                self.facts.append(device_facts)
        except Exception, e:
            return failed(str(e))

        output = ''
        for fact in self.facts:
            output += 'hostname: {} '.format(fact['hostname'])
            if attributes:
                output += ' '.join('{}: {}'.format(
                    attribute,
                    fact[attribute]) for attribute in attributes)
            else:
                output = ' '.join('{}: {} '.format(item, value) for item, value in fact.iteritems())
            output += '\n' 
        return passed(output)

