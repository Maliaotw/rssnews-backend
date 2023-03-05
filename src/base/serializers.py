import datetime

from django.utils.dateparse import parse_datetime
from rest_framework import serializers, ISO_8601
from rest_framework.settings import api_settings
from rest_framework.utils import humanize_datetime


class CustomDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        input_formats = getattr(self, 'input_formats', api_settings.DATETIME_INPUT_FORMATS)

        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            self.fail('date')

        if isinstance(value, datetime.datetime):
            return self.enforce_timezone(value)

        for input_format in input_formats:
            if input_format.lower() == ISO_8601:
                try:
                    parsed = parse_datetime(value)
                    if parsed is not None:
                        return self.enforce_timezone(parsed)
                except (ValueError, TypeError):
                    pass
            else:
                try:
                    parsed = self.datetime_parser(value, input_format)
                    return self.enforce_timezone(parsed)
                except (ValueError, TypeError):
                    pass
                except OverflowError:
                    parsed = datetime.datetime.now()
                    return self.enforce_timezone(parsed)
        humanized_format = humanize_datetime.datetime_formats(input_formats)
        self.fail('invalid', format=humanized_format)
