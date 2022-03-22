# -*- coding: utf-8 -*-
#
import datetime
import ipaddress
import logging
import os
import re
import time
import uuid
from collections import OrderedDict
from functools import wraps
from itertools import chain

import ipdb
from django.utils.translation import ugettext as _

UUID_PATTERN = re.compile(r'[0-9a-zA-Z\-]{36}')
ipip_db = None

DATE_FORMATS = [
    '%d-%b-%Y',                     # 02-jan-2000
    '%d.%m.%Y',                     # 02.02.2000
    '%d/%m/%Y',                     # 01/06/2011
    '%Y-%m-%d',                     # 2000-01-02
    '%Y.%m.%d',                     # 2000.01.02
    '%Y/%m/%d',                     # 2005/05/30
    'before %b-%Y',                 # before aug-1996
    '%Y.%m.%d %H:%M:%S',            # 2002.09.19 13:00:00
    '%Y%m%d %H:%M:%S',              # 20110908 14:44:51
    '%Y-%m-%d %H:%M:%S',            # 2011-09-08 14:44:51
    '%Y-%m-%d %H:%M:%S CLST',       # 2011-09-08 14:44:51 CLST CL
    '%Y-%m-%d %H:%M:%S.%f',       # 2011-09-08 14:44:51 CLST CL
    '%d.%m.%Y  %H:%M:%S',           # 19.09.2002 13:00:00
    '%d-%b-%Y %H:%M:%S %Z',         # 24-Jul-2009 13:20:03 UTC
    '%Y/%m/%d %H:%M:%S (%z)',       # 2011/06/01 01:05:01 (+0900)
    '%Y/%m/%d %H:%M:%S',            # 2011/06/01 01:05:01
    '%a %b %d %H:%M:%S %Z %Y',      # Tue Jun 21 23:59:59 GMT 2011
    '%a %b %d %Y',                  # Tue Dec 12 2000
    '%Y-%m-%dT%H:%M:%S',            # 2007-01-26T19:10:31
    '%Y-%m-%dT%H:%M:%SZ',           # 2007-01-26T19:10:31Z
    '%Y-%m-%dt%H:%M:%S.%fz',        # 2007-01-26t19:10:31.00z
    '%Y-%m-%dT%H:%M:%S%z',          # 2011-03-30T19:36:27+0200
    '%Y-%m-%dT%H:%M:%S.%f%z',       # 2011-09-08T14:44:51.622265+03:00
    '%Y-%m-%dt%H:%M:%S.%f',         # 2011-09-08t14:44:51.622265
    '%Y-%m-%dt%H:%M:%S',            # 2007-01-26T19:10:31
    '%Y-%m-%dt%H:%M:%SZ',           # 2007-01-26T19:10:31Z
    '%Y-%m-%dt%H:%M:%S.%fz',        # 2007-01-26t19:10:31.00z
    '%Y-%m-%dt%H:%M:%S%z',          # 2011-03-30T19:36:27+0200
    '%Y-%m-%dt%H:%M:%S.%f%z',       # 2011-09-08T14:44:51.622265+03:00
    '%Y%m%d',                       # 20110908
    '%Y. %m. %d.',                  # 2020. 01. 12.
    'before %b-%Y',                 # before aug-1996
    '%a %d %b %Y',                  # Tue 21 Jun 2011
    '%A %d %b %Y',                  # Tuesday 21 Jun 2011
    '%a %d %B %Y',                  # Tue 21 June 2011
    '%A %d %B %Y',                  # Tuesday 21 June 2011
    '%Y-%m-%d %H:%M:%S (%Z+0:00)',  # 2007-12-24 10:24:32 (gmt+0:00)
    '%B %d %Y',                     # January 01 2000
]


def str_to_date(text):
    text = text.strip().lower()

    if not text or text == 'not defined':
        return

    text = text.replace('(jst)', '(+0900)')
    text = re.sub('(\+[0-9]{2}):([0-9]{2})', '\\1\\2', text)
    text = re.sub('(\ #.*)', '', text)

    for format in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(text, format)
        except ValueError:
            pass

    raise Exception("Unknown date format: '%s'" % text)

def combine_seq(s1, s2, callback=None):
    for s in (s1, s2):
        if not hasattr(s, '__iter__'):
            return []

    seq = chain(s1, s2)
    if callback:
        seq = map(callback, seq)
    return seq


def get_logger(name=None):
    return logging.getLogger('jumpserver.%s' % name)


def timesince(dt, since='', default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days, 5 hours.
    """

    if since is '':
        since = datetime.datetime.utcnow()

    if since is None:
        return default

    diff = since - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s" % (period, singular if period == 1 else plural)
    return default


def setattr_bulk(seq, key, value):
    def set_attr(obj):
        setattr(obj, key, value)
        return obj

    return map(set_attr, seq)


def set_or_append_attr_bulk(seq, key, value):
    for obj in seq:
        ori = getattr(obj, key, None)
        if ori:
            value += " " + ori
        setattr(obj, key, value)


def capacity_convert(size, expect='auto', rate=1000):
    """
    :param size: '100MB', '1G'
    :param expect: 'K, M, G, T
    :param rate: Default 1000, may be 1024
    :return:
    """
    rate_mapping = (
        ('K', rate),
        ('KB', rate),
        ('M', rate ** 2),
        ('MB', rate ** 2),
        ('G', rate ** 3),
        ('GB', rate ** 3),
        ('T', rate ** 4),
        ('TB', rate ** 4),
    )

    rate_mapping = OrderedDict(rate_mapping)

    std_size = 0  # To KB
    for unit in rate_mapping:
        if size.endswith(unit):
            try:
                std_size = float(size.strip(unit).strip()) * rate_mapping[unit]
            except ValueError:
                pass

    if expect == 'auto':
        for unit, rate_ in rate_mapping.items():
            if rate > std_size / rate_ > 1:
                expect = unit
                break

    if expect not in rate_mapping:
        expect = 'K'

    expect_size = std_size / rate_mapping[expect]
    return expect_size, expect


def sum_capacity(cap_list):
    total = 0
    for cap in cap_list:
        size, _ = capacity_convert(cap, expect='K')
        total += size
    total = '{} K'.format(total)
    return capacity_convert(total, expect='auto')


def get_short_uuid_str():
    return str(uuid.uuid4()).split('-')[-1]


def is_uuid(seq):
    if isinstance(seq, uuid.UUID):
        return True
    elif isinstance(seq, str) and UUID_PATTERN.match(seq):
        return True
    elif isinstance(seq, (list, tuple)):
        all([is_uuid(x) for x in seq])
    return False


def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')

    if x_forwarded_for and x_forwarded_for[0]:
        login_ip = x_forwarded_for[0]
    else:
        login_ip = request.META.get('REMOTE_ADDR', '')
    return login_ip


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        pass
    return False


def with_cache(func):
    cache = {}
    key = "_{}.{}".format(func.__module__, func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        cached = cache.get(key)
        if cached:
            return cached
        res = func(*args, **kwargs)
        cache[key] = res
        return res

    return wrapper


def random_string(length):
    import string
    import random
    charset = string.ascii_letters + string.digits
    s = [random.choice(charset) for i in range(length)]
    return ''.join(s)


logger = get_logger(__name__)


def timeit(func):
    def wrapper(*args, **kwargs):
        logger.debug("Start call: {}".format(func.__name__))
        now = time.time()
        result = func(*args, **kwargs)
        using = (time.time() - now) * 1000
        msg = "Call {} end, using: {:.1f}ms".format(func.__name__, using)
        logger.debug(msg)
        return result

    return wrapper


def get_ip_city(ip):
    global ipip_db
    if ipip_db is None:
        ipip_db_path = os.path.join(os.path.dirname(__file__), 'ipip/ipipfree.ipdb')
        ipip_db = ipdb.City(ipip_db_path)
    info = list(set(ipip_db.find(ip, 'CN')))
    if '' in info:
        info.remove('')
    return ' '.join(info)


def write_login_log(*args, **kwargs):
    from authentication.models import UserLoginLog
    default_city = _("Unknown")
    ip = kwargs.get('ip', '')

    logger.debug("write_login_log {}".format(ip))

    if not (ip and validate_ip(ip)):
        ip = ip[:15]
        city = default_city
    else:
        city = get_ip_city(ip) or default_city
    kwargs.update({'ip': ip, 'city': city})
    UserLoginLog.objects.create(**kwargs)

def list_pageger(list,page):
    """列表分頁切割
    :param list: LIST
    :param page: 20
    :return:
    """
    return [list[i:i+page] for i in range(0, len(list), page)]


