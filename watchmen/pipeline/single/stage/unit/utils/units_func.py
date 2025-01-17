from datetime import datetime
from decimal import Decimal

from watchmen.common.constants import parameter_constants, pipeline_constants
from watchmen.config.config import settings
from watchmen.topic.factor.factor import Factor
from watchmen.topic.topic import Topic

SPLIT_FLAG = ","

INSERT = "insert"
UPDATE = "update"
SEQUENCE = "sequence"

NUMBER = "number"
UNSIGNED = "unsigned"  # 0 & positive

TEXT = "text"
TIME = 'time'

# address
ADDRESS = "address"
CONTINENT = "continent"
REGION = "region"
COUNTRY = "country"
PROVINCE = "province"
CITY = "city"
DISTRICT = "district"
ROAD = "road"
COMMUNITY = "community"
FLOOR = "floor"
RESIDENCE_TYPE = "residence-type"
RESIDENTIAL_AREA = "residential-area"

EMAIL = "email"
PHONE = "phone"
MOBILE = "mobile"
FAX = "fax"

DATETIME = "datetime"  # YYYY - MM - DD
DATE = "date"  # YYYY - MM - DD
TIME = "time"  # HH: mm:ss
YEAR = "year"  # 4

HALF_YEAR = "half-year"  # 1: first

QUARTER = "quarter"  # 1 - 4
SEASON = "season"  # 1: spring, 2: summer, 3: autumn, 4: winter
MONTH = "month"  # 1 - 12
HALF_MONTH = "half-month"  # 1: first

TEN_DAYS = "ten-days"  # 1, 2, 3
WEEK_OF_YEAR = "week-of-year"  # 1 - 53
WEEK_OF_MONTH = "week-of-month"  # 1 - 6
HALF_WEEK = "half-week"  # 1: first

DAY_OF_MONTH = "day-of-month"  # 1 - 31, according

DAY_OF_WEEK = "day-of-week"  # 1 - 7
DAY_KIND = "day-kind"  # 1: workday, 2: weekend, 3: holiday
HOUR = "hour"  # 0 - 23
HOUR_KIND = "hour-kind"  # 1: work

MINUTE = "minute"  # 0 - 59
SECOND = "second"  # 0 - 59
AM_PM = "am-pm"  # 1, 2

# individual
GENDER = "gender"
OCCUPATION = "occupation"
DATE_OF_BIRTH = "date-of-birth"  # YYYY - MM - DD
AGE = "age"
ID_NO = "id-no"
RELIGION = "religion"
NATIONALITY = "nationality"

# organization
BIZ_TRADE = "biz-trade"
BIZ_SCALE = "biz-scale"

BOOLEAN = "boolean"

ENUM = "enum"

OBJECT = "object"
ARRAY = "array"


def check_condition(operator: str, left_value, right_value) -> bool:
    if operator == "equals":
        return left_value == right_value
    elif operator == "not-equals":
        return left_value != right_value
    elif operator == "less":
        return left_value < right_value
    elif operator == "less-equals":
        return left_value <= right_value
    elif operator == "more":
        return left_value > right_value
    elif operator == "more-equals":
        return left_value >= right_value
    elif operator == "empty":
        return left_value is None
    elif operator == "not-empty":
        return left_value is not None
    elif operator == "in":
        return left_value in __split_value(right_value)
    elif operator == "not-in":
        return left_value not in __split_value(right_value)
    else:
        raise Exception("NotImplemented:", operator)


def __split_value(value):
    if SPLIT_FLAG not in value:
        return [value]
    else:
        return value.split(SPLIT_FLAG)


def convert_factor_type(value, factor_type):
    if value is None:
        return None
    elif factor_type == TEXT:
        return str(value)
    elif factor_type == NUMBER:
        return Decimal(value)
    elif factor_type == DATETIME:
        if isinstance(value,datetime):
            return value
        else:
            return datetime.strptime(value, settings.TOPIC_DATE_FORMAT)
    elif factor_type == BOOLEAN:
        return bool(value)
    elif factor_type == SEQUENCE:
        return int(value)
    elif factor_type == YEAR:
        return int(value)
    elif factor_type == MONTH:
        return int(value)
    elif factor_type == TIME:
        return datetime.fromisoformat(value)
    else:
        return value


def build_factor_dict(topic: Topic):
    factor_dict = {}
    for factor in topic.factors:
        factor_dict[factor.factorId] = factor
    return factor_dict


def get_factor(factor_id, target_topic):
    # print(target_topic.json())
    for factor in target_topic.factors:
        if factor.factorId == factor_id:
            return factor


def get_factor_by_name(factor_name, target_topic):
    for factor in target_topic.factors:
        if factor.name == factor_name:
            return factor


def get_execute_time(start_time):
    time_elapsed = datetime.utcnow() - start_time
    execution_time = time_elapsed.microseconds / 1000
    return execution_time


def get_value(factor: Factor, data):
    if factor.name in data:
        value = data[factor.name]
        if value is None:
            return value
        else:
            return convert_factor_type(value, factor.type)
    elif factor.type == "number":
        return
    elif factor.type == "text":
        return None
    else:
        return None


def add_audit_columns(dictionary, audit_type):
    if audit_type == INSERT:
        dictionary[pipeline_constants.INSERT_TIME] = datetime.utcnow()
    elif audit_type == UPDATE:
        dictionary[pipeline_constants.UPDATE_TIME] = datetime.utcnow()
    else:
        raise Exception("unknown audit_type")


def add_trace_columns(dictionary, trace_type, pipeline_uid):
    dictionary[trace_type] = pipeline_uid


def process_variable(variable_name):
    if variable_name.startswith("{"):
        return "memory", variable_name.replace("{", "").replace("}", "")
    else:
        return parameter_constants.CONSTANT, variable_name
