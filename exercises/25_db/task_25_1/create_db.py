from task_25_1 import DBHandler

try:
    DBHandler('dhcp_snooping.db')
    DBHandler('dhcp_snooping.db', create=True)
except:
    DBHandler('dhcp_snooping.db', create=True).create_schema(from_file='dhcp_snooping_schema.sql')
