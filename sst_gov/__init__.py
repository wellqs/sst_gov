"""
Configura PyMySQL como substituto de MySQLdb para evitar a necessidade de compilar mysqlclient.
"""

import pymysql

pymysql.install_as_MySQLdb()
