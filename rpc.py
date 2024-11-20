#!/usr/bin/env python3
# extracted from https://github.com/HyperSine/ida-rpyc
import threading

import idaapi

import rpyc
import rpyc.utils.server
import rpyc.utils.authenticators

class IdaRPyCService(rpyc.SlaveService):

    def on_connect(self, conn: rpyc.Connection):
        super().on_connect(conn)

        def _handle_call(self, obj, args, kwargs = ()):
            retval = [None]

            def trampoline():
                retval[0] = obj(*args, **dict(kwargs))
                return 1

            idaapi.execute_sync(trampoline, idaapi.MFF_WRITE)

            return retval[0]

        def _handle_callattr(self, obj, name, args, kwargs = ()):
            obj = self._handle_getattr(obj, name)
            return _handle_call(obj, args, kwargs)

        conn._HANDLERS[rpyc.core.protocol.consts.HANDLE_CALL] = _handle_call
        conn._HANDLERS[rpyc.core.protocol.consts.HANDLE_CALLATTR] = _handle_callattr

    def on_disconnect(self, conn):
        pass


hostname="localhost"
port = 54444
server = rpyc.utils.server.ThreadedServer(IdaRPyCService, hostname = hostname, port = port)
server_thread = threading.Thread(target = server.start)
server_thread.start()
print(f"server started [{hostname}:{port}]")
