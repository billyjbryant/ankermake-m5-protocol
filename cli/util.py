import click
import json


def json_key_value(str):
    if "=" not in str:
        raise ValueError("Invalid 'key=value' argument")
    key, value = str.split("=", 1)
    try:
        return key, int(value)
    except ValueError:
        try:
            return key, float(value)
        except ValueError:
            return key, value


class EnumType(click.ParamType):
    def __init__(self, enum):
        self.__enum = enum

    def get_missing_message(self, param):
        return "Choose number or name from:\n{choices}".format(
            choices="\n".join(f"{e.value:10}: {e.name}" for e in sorted(self.__enum))
        )

    def convert(self, value, param, ctx):
        try:
            return self.__enum(int(value))
        except ValueError:
            try:
                return self.__enum[value]
            except KeyError:
                self.fail(self.get_missing_message(param), param, ctx)


class FileSizeType(click.ParamType):

    name = "filesize"

    def convert(self, value, param, ctx):
        value = value.lower().rstrip("b")
        try:
            num = int(value[:-1])
            if value.endswith("k"):
                return num * 1024**1
            elif value.endswith("m"):
                return num * 1024**2
            elif value.endswith("g"):
                return num * 1024**3
            elif value.endswith("t"):
                return num * 1024**4
            else:
                raise ValueError()
        except ValueError:
            self.fail("Invalid file size: use {kb,gb,mb,tb} suffix (examples: 1337kb, 42mb, 17gb)", param, ctx)


def parse_json(msg):
    if isinstance(msg, dict):
        for key, value in msg.items():
            msg[key] = parse_json(value)
    elif isinstance(msg, str):
        try:
            msg = parse_json(json.loads(msg))
        except ValueError:
            pass

    return msg


def pretty_json(msg):
    return json.dumps(parse_json(msg), indent=4)


def pretty_mac(mac):
    parts = []
    while mac:
        parts.append(mac[:2])
        mac = mac[2:]
    return ":".join(parts)


def pretty_size(size):
    for unit in ["", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:3.2f}{unit}"
