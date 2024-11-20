import rpyc
conn = rpyc.connect('localhost', 54444, service = rpyc.MasterService)

current_ea = conn.modules.idc.here()
some_bytes = conn.modules.idaapi.get_bytes(current_ea, 4)
print('0x{:x}: {}'.format(current_ea, some_bytes))
