#coding=utf8
from gjeasy.models.base import metadata, mysql_db


def create_table(table_names):
    need_tables = []
    for table in metadata.sorted_tables:
        if table.name in table_names:
            need_tables.append(table)

    metadata.create_all(mysql_db, need_tables)

if __name__ == "__main__":
    #from gjeasy.models.account import Account
    from gjeasy.models.account_setting import AccountSetting
    create_table("account")
    create_table("account_setting")