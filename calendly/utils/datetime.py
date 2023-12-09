from pytz import timezone, BaseTzInfo, UnknownTimeZoneError
from calendly.misc.exceptions import UnknownTimezoneException

def read_data_from_file(file_path: str) -> str:
    with open(file_path) as fd:
        return fd.read()

def overwrite_data_to_file(file_path: str, data: str):
    with open(file_path, "w") as fd:
        fd.write(data)

def tz_str_to_tz_obj(tz: str) -> BaseTzInfo:
    try:
        tz_obj = timezone(tz)
    except UnknownTimeZoneError as e:
        raise UnknownTimezoneException(f"Encountered unknown timezone f{timezone}. Error: {e}")

    return tz_obj


def tz_obj_to_tz_str(tz: BaseTzInfo) -> str:
    return str(tz)
