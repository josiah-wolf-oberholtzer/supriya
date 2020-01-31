import asyncio
import logging
import os
import signal
import subprocess
import time

import supriya.exceptions

logger = logging.getLogger("supriya.server")


def boot(options, scsynth_path, port):
    options_string = options.as_options_string(port)
    command = "{} {}".format(scsynth_path, options_string)
    logger.info("Boot: {}".format(command))
    process = subprocess.Popen(
        command,
        shell=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        start_time = time.time()
        timeout = 10
        while True:
            line = process.stdout.readline().decode().rstrip()
            if line:
                logger.info("Boot: {}".format(line))
            if line.startswith("SuperCollider 3 server ready"):
                break
            elif line.startswith("ERROR:"):
                raise supriya.exceptions.ServerCannotBoot(line)
            elif line.startswith(
                "Exception in World_OpenUDP: bind: Address already in use"
            ):
                raise supriya.exceptions.ServerCannotBoot(line)
            elif (time.time() - start_time) > timeout:
                raise supriya.exceptions.ServerCannotBoot(line)
    except supriya.exceptions.ServerCannotBoot:
        try:
            process_group = os.getpgid(process.pid)
            os.killpg(process_group, signal.SIGINT)
            process.terminate()
            process.wait()
        except ProcessLookupError:
            pass
        raise
    return process


class ProcessProtocol:

    def __init__(self):
        self.is_running = False

    def boot(self, options, scsynth_path, port):
        ...

    def quit(self):
        ...


class SyncProcessProtocol(ProcessProtocol):

    def boot(self, options, scsynth_path, port):
        if self.is_running:
            return
        options_string = options.as_options_string(port)
        command = "{} {}".format(scsynth_path, options_string)
        logger.info("Boot: {}".format(command))
        self.process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            start_time = time.time()
            timeout = 10
            while True:
                line = self.process.stdout.readline().decode().rstrip()
                if line:
                    logger.info("Boot: {}".format(line))
                if line.startswith("SuperCollider 3 server ready"):
                    break
                elif line.startswith("ERROR:"):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif line.startswith(
                    "Exception in World_OpenUDP: bind: Address already in use"
                ):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif (time.time() - start_time) > timeout:
                    raise supriya.exceptions.ServerCannotBoot(line)
        except supriya.exceptions.ServerCannotBoot:
            try:
                process_group = os.getpgid(self.process.pid)
                os.killpg(process_group, signal.SIGINT)
                self.process.terminate()
                self.process.wait()
            except ProcessLookupError:
                pass
            raise

    def quit(self):
        if not self.is_running:
            return
        self.process.terminate()
        self.process.wait()


class AsyncProcessProtocol(asyncio.SubprocessProtocol, ProcessProtocol):

    def __init__(self):
        ProcessProtocol.__init__(self)
        asyncio.SubprocessProtocol.__init__(self)
        self.boot_future = None
        self.exit_future = None

    async def boot(self, options, scsynth_path, port):
        if self.is_running:
            return
        self.is_running = False
        options_string = options.as_options_string(port)
        command = "{} {}".format(scsynth_path, options_string)
        logger.info("Boot: {}".format(command))
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        _, _ = await loop.subprocess_exec(
            lambda: self, *command.split(), stdin=None, stderr=None
        )

    def connection_made(self, transport):
        self.is_running = True
        self.transport = transport

    def pipe_data_received(self, fd, data):
        for line in data.splitlines():
            if line.strip().startswith(b"Exception"):
                self.boot_future.set_result(False)
            elif line.strip().startswith(b"SuperCollider 3 server ready"):
                self.boot_future.set_result(None)

    def process_exited(self):
        self.is_running = False
        self.exit_future.set_result(None)

    async def quit(self):
        if not self.is_running:
            return
        if not self.boot_future.done():
            self.boot_future.set_result(False)
        if not self.exit_future.done():
            self.exit_future.set_result
        self.transport.close()
        self.is_running = False
