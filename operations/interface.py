from base import BaseOperation, register
from automation import tasks
from netbot.lib.common import passed, failed, INTERFACE_RE
from functools import partial
import re


@register('InterfaceShutdown')
class InterfaceShutdown(BaseOperation):
    REGEX = [INTERFACE_RE]

    def __init__(self, utterance):
        super(InterfaceShutdown, self).__init__(utterance)
        self.interfaces = re.findall('|'.join(InterfaceShutdown.REGEX), self.utterance)

    def run(self, *args, **kwargs):
        if not len(self.devices) == 2:
            return failed('Incorrect number of devices entered: {}', len(self.devices))

        intent = re.search(r'enable|up', self.utterance)
        return self.link_status(intent)

    @staticmethod
    def _get_neighbors(device, interfaces):
        return tasks.get_interface_neighbors(device, interfaces)

    @staticmethod
    def _find_neighbor_match(neighbor_device, x):
        if x.neighbor.lower() == neighbor_device:
            return x.local_interface

    def link_status(self, intent):
        if intent:
            return self._link_enable() 
        else:
            return self._link_disable()

    @staticmethod
    def _prepare_commands(intent, intf):
        return ['interface {}'.format(intf), '{}shutdown'.format('' if intent else 'no ')]

    def _link_disable(self):
        if len(self.interfaces) > 1:
            return failed('Incorrect number of interfaces entered: {}', len(self.interfaces))

        a_device_neighbor = filter(partial(self._find_neighbor_match, self.devices[1]),
                                    self._get_neighbors(self.devices[0], self.interfaces))
        b_device_neighbor = filter(partial(self._find_neighbor_match, self.devices[0]),
                                    self._get_neighbors(self.devices[1], self.interfaces))

        if not a_device_neighbor or not b_device_neighbor:
            return failed('Devices {} are not neighbors on any interfaces', ', '.join(self.devices))

        if len(a_device_neighbor) > 1 or len(b_device_neighbor) > 1:
            return failed('Devices {} are neighbors on more than one interface', ', '.join(self.devices))

        a_end_interface = a_device_neighbor[0].local_interface
        b_end_interface = b_device_neighbor[0].local_interface
        a_commands = self._prepare_commands(True, a_end_interface)
        b_commands = self._prepare_commands(True, b_end_interface)

        try:
            tasks.apply_config(self.devices[0], a_commands)
            tasks.apply_config(self.devices[1], b_commands)
        except Exception, e:
            return failed(str(e))

        if any([self._get_neighbors(self.devices[0], [a_end_interface]),
                self._get_neighbors(self.devices[1], [b_end_interface])]):
            return failed('Failed to disable interfaces {}, {} on {}', a_end_interface,
                                                                       b_end_interface,
                                                                       ', '.join(self.devices))

        return passed('Interface {} on {} and interface {} on {} were successfully disabled',
                      a_end_interface, self.devices[0],
                      b_end_interface, self.devices[1])

    def _link_enable(self):
        if not len(self.interfaces) == 2:
            return failed('Incorrect number of interfaces entered: {}', len(self.interfaces))

        a_end_interface, b_end_interface = self.interfaces[0], self.interfaces[1]

        a_commands = self._prepare_commands(False, a_end_interface)
        b_commands = self._prepare_commands(False, b_end_interface)

        try:
            tasks.apply_config(self.devices[0], a_commands)
            tasks.apply_config(self.devices[1], b_commands)
        except Exception, e:
            return failed(str(e))

        if all([self._get_neighbors(self.devices[0], [a_end_interface]),
                self._get_neighbors(self.devices[1], [b_end_interface])]): 
            return passed('Interface {} on {} and interface {} on {} were successfully enabled',
                           a_end_interface, self.devices[0],
                           b_end_interface, self.devices[1])

        return failed('Failed to enable interfaces {}, {} on {}', a_end_interface,
                                                                  b_end_interface,
                                                                  ', '.join(self.devices))

