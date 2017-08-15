import re


class NoDevicesEntered(Exception):
    def __init__(self):
        Exception.__init__(self, 'User did not enter any device')


class BaseOperation(object):
    def __init__(self, devices):
        self.devices = devices
        if not self.devices_found:
            raise NoDevicesEntered

    def __call__(self):
        raise Exception('No function found')

    @property
    def devices_found(self):
        return False if not self.devices else True

    @classmethod
    def _sanitize_attributes(cls, user_attributes):
        sanitized_attributes = []
        if not user_attributes:
            return False
        for attribute in user_attributes:
            if attribute not in getattr(cls, 'REGEX'):
                continue
            if len(attribute.split()) > 1:
                attr = re.sub(' ', '_', attribute)
                sanitized_attributes.append(attr)
            else:
                sanitized_attributes.append(attribute)
        return sanitized_attributes
