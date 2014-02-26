import hashlib
from gjeasy.utils.coding_str import str2utf8


def cal_key(content):
    return hashlib.md5(str2utf8(content)[0]).hexdigest()