import json
import logging as log

from datetime import datetime, timedelta

from ..lib.service import Service
from .. import app

from libflagship.pppp import P2PCmdType, PktClose, Duid, Type, Xzyh, Aabb
from libflagship.ppppapi import AnkerPPPPAsyncApi, PPPPState


class PPPPService(Service):

    def api_command(self, commandType, **kwargs):
        cmd = {
            "commandType": commandType,
            **kwargs
        }
        return self._api.send_xzyh(
            json.dumps(cmd).encode(),
            cmd=P2PCmdType.P2P_JSON_CMD
        )

    def worker_start(self):
        config = app.config["config"]

        deadline = datetime.now() + timedelta(seconds=2)

        with config.open() as cfg:
            printer = cfg.printers[0]

        api = AnkerPPPPAsyncApi.open_lan(Duid.from_string(printer.p2p_duid), host=printer.ip_addr)
        # _pppp_dumpfile(api, dumpfile)

        log.info("Trying connect over pppp")

        api.connect_lan_search()

        while api.state != PPPPState.Connected:
            try:
                msg = api.recv(timeout=(deadline - datetime.now()).total_seconds())
                api.process(msg)
            except StopIteration:
                raise ConnectionRefusedError("Connection rejected by device")

        log.info("Established pppp connection")
        self._api = api

    def _recv_aabb(self, fd):
        data = fd.read(12)
        aabb = Aabb.parse(data)[0]
        p = data + fd.read(aabb.len + 2)
        aabb, data = Aabb.parse_with_crc(p)[:2]
        return aabb, data

    def worker_run(self, timeout):
        msg = self._api.poll(timeout=timeout)
        if not msg or msg.type != Type.DRW:
            return

        ch = self._api.chans[msg.chan]

        with ch.lock:
            data = ch.peek(16, timeout=0)
            if not data:
                return

            if data[:4] == b'XZYH':
                hdr = ch.peek(16, timeout=0)
                if not hdr:
                    return

                xzyh = Xzyh.parse(hdr)[0]
                data = ch.read(xzyh.len + 16, timeout=0)
                if not data:
                    return None

                xzyh.data = data[16:]
                self.notify((msg.chan, xzyh))
            elif data[:2] == b'\xAA\xBB':
                aabb, data = self._recv_aabb(ch)
                if len(data) != 1:
                    raise ValueError(f"Unexpected reply from aabb request: {data}")

                aabb.data = data
                self.notify((msg.chan, aabb))
            else:
                raise ValueError(f"Unexpected data in stream: {data!r}")

    def worker_stop(self):
        self._api.send(PktClose())
        del self._api

    @property
    def connected(self):
        if not hasattr(self, "_api"):
            return False
        return self._api.state == PPPPState.Connected
