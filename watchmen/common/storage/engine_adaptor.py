from watchmen.config.config import settings

MYSQL = "mysql"
MONGO = "mongo"
ORACLE = "oracle"


def find_template():
    if settings.STORAGE_ENGINE == MONGO:
        from watchmen.common.mongo import mongo_new_template
        return mongo_new_template
    elif settings.STORAGE_ENGINE == MYSQL:
        from watchmen.common.mysql import mysql_template
        return mysql_template
    elif settings.STORAGE_ENGINE == ORACLE:
        raise Exception("do not support Oracle")
