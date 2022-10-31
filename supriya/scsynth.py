import os
import platform
import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import uqbar.io
import uqbar.objects

import supriya


@dataclass(frozen=True)
class Options:
    """
    SuperCollider server options configuration.

    ::

        >>> import supriya.realtime
        >>> options = supriya.scsynth.Options()

    """

    ### CLASS VARIABLES ###

    audio_bus_channel_count: int = 1024
    block_size: int = 64
    buffer_count: int = 1024
    control_bus_channel_count: int = 16384
    executable: Optional[str] = None
    hardware_buffer_size: Optional[int] = None
    initial_node_id: int = 1000
    input_bus_channel_count: int = 8
    input_device: Optional[str] = None
    input_stream_mask: str = ""
    load_synthdefs: bool = False
    maximum_logins: int = 1
    maximum_node_count: int = 1024
    maximum_synthdef_count: int = 1024
    memory_locking: bool = False
    memory_size: int = 8192
    output_bus_channel_count: int = 8
    output_device: Optional[str] = None
    output_stream_mask: str = ""
    password: Optional[str] = None
    protocol: str = "udp"
    random_number_generator_count: int = 64
    remote_control_volume: bool = False
    restricted_path: Optional[str] = None
    sample_rate: Optional[int] = None
    threads: Optional[int] = None
    ugen_plugins_path: Optional[str] = None
    verbosity: int = 0
    wire_buffer_count: int = 64
    zero_configuration: bool = False

    ### INITIALIZER ###

    def __post_init__(self):
        if self.input_bus_channel_count is None:
            object.__setattr__(self, "input_bus_channel_count", 8)
        if self.output_bus_channel_count is None:
            object.__setattr__(self, "output_bus_channel_count", 8)
        if self.input_bus_channel_count < 0:
            raise ValueError(self.input_bus_channel_count)
        if self.output_bus_channel_count < 0:
            raise ValueError(self.output_bus_channel_count)
        if self.audio_bus_channel_count < (
            self.input_bus_channel_count + self.output_bus_channel_count
        ):
            raise ValueError("Insufficient audio buses")

    ### CLASS VARIABLES ###

    def __repr__(self):
        return uqbar.objects.get_repr(self, multiline=True, suppress_defaults=False)

    ### PUBLIC METHODS ###

    def serialize(self, port=57110, realtime=True) -> List[str]:
        result = []
        if realtime:
            if self.protocol == "tcp":
                result.extend(["-t", port])
            else:
                result.extend(["-u", port])
            if self.input_device:
                result.extend(["-H", self.input_device])
                if self.output_device != self.input_device:
                    result.append(self.output_device)
            if self.maximum_logins != 64:
                result.extend(["-l", self.maximum_logins])
            if self.password:
                result.extend(["-p", self.password])
            if self.sample_rate is not None:
                result.extend(["-S", int(self.sample_rate)])
            if not self.zero_configuration:
                result.extend(["-R", "0"])
        if self.audio_bus_channel_count != 1024:
            result.extend(["-a", self.audio_bus_channel_count])
        if self.control_bus_channel_count != 16384:
            result.extend(["-c", self.control_bus_channel_count])
        if self.input_bus_channel_count != 8:
            result.extend(["-i", self.input_bus_channel_count])
        if self.output_bus_channel_count != 8:
            result.extend(["-o", self.output_bus_channel_count])
        if self.buffer_count != 1024:
            result.extend(["-b", self.buffer_count])
        if self.maximum_node_count != 1024:
            result.extend(["-n", self.maximum_node_count])
        if self.maximum_synthdef_count != 1024:
            result.extend(["-d", self.maximum_synthdef_count])
        if self.block_size != 64:
            result.extend(["-z", self.block_size])
        if self.hardware_buffer_size is not None:
            result.extend(["-Z", int(self.hardware_buffer_size)])
        if self.memory_size != 8192:
            result.extend(["-m", self.memory_size])
        if self.random_number_generator_count != 64:
            result.extend(["-r", self.random_number_generator_count])
        if self.wire_buffer_count != 64:
            result.extend(["-w", self.wire_buffer_count])
        if not self.load_synthdefs:
            result.extend(["-D", "0"])
        if self.input_stream_mask:
            result.extend(["-I", self.input_stream_mask])
        if self.output_stream_mask:
            result.extend(["-O", self.output_stream_mask])
        if 0 < self.verbosity:
            result.extend(["-v", self.verbosity])
        if self.restricted_path is not None:
            result.extend(["-P", self.restricted_path])
        if self.memory_locking:
            result.append("-L")
        if self.ugen_plugins_path:
            result.extend(["-U", self.ugen_plugins_path])
        if self.supernova and self.threads:
            result.extend(["-t", self.threads])
        return [str(_) for _ in result]

    ### PUBLIC PROPERTIES ###

    @property
    def first_private_bus_id(self):
        return self.output_bus_channel_count + self.input_bus_channel_count

    @property
    def private_audio_bus_channel_count(self):
        return (
            self.audio_bus_channel_count
            - self.input_bus_channel_count
            - self.output_bus_channel_count
        )

    @property
    def scsynth_path(self):
        return supriya.scsynth.find(self.executable)

    @property
    def supernova(self):
        return Path(self.scsynth_path).stem == "supernova"


def _fallback_scsynth_path(executable: Optional[str] = None):
    paths = []
    system = platform.system()
    executable = executable or "scsynth"
    if Path(executable).stem == "supernova":
        executable = "supernova"
    if system == "Linux":
        paths.extend(
            [Path("/usr/bin/" + executable), Path("/usr/local/bin/" + executable)]
        )
    elif system == "Darwin":
        paths.append(
            Path("/Applications/SuperCollider.app/Contents/Resources/" + executable)
        )
    elif system == "Windows":
        paths.extend(
            Path(r"C:\Program Files").glob(r"SuperCollider*\\" + executable + ".exe")
        )
    for path in paths:
        if path.exists():
            return path
    return None


def find(executable: Optional[str] = None):
    """Find the ``scsynth`` or ``supernova`` executable.

    The following paths, if defined, will be searched (prioritised as ordered):

    1. The absolute path ``executable``
    2. The environment variable ``SCSYNTH_PATH`` (pointing to the `scsynth` binary)
    3. ``scsynth_path`` if defined in Supriya's configuration file
    4. The user's ``PATH``
    5. Common installation directories of the SuperCollider application.

    Returns a path to the ``scsynth`` or ``supernova`` executable.
    Raises ``RuntimeError`` if no path is found.
    """
    scsynth_path = Path(
        executable
        or os.environ.get("SCSYNTH_PATH")
        or supriya.config.get("core", "scsynth_path")
    )
    if scsynth_path.is_absolute() and uqbar.io.find_executable(str(scsynth_path)):
        return scsynth_path
    scsynth_path_candidates = uqbar.io.find_executable(scsynth_path.name)
    if scsynth_path_candidates:
        return Path(scsynth_path_candidates[0])
    fallback_path = _fallback_scsynth_path(executable)
    if fallback_path is not None:
        return fallback_path
    raise RuntimeError("Failed to locate " + executable)


def kill(supernova=False):
    executable = "supernova" if supernova else "scsynth"
    with subprocess.Popen(
        ["ps", "-Af"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as process:
        output = process.stdout.read()
    for line in output.decode().splitlines():
        parts = line.split()
        if not any(part == executable for part in parts):
            continue
        pid = int(parts[1])
        os.kill(pid, signal.SIGKILL)
