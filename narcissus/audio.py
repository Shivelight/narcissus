from typing import Union, BinaryIO
from os import PathLike

from pydub import AudioSegment
from pydub.playback import play


def play_audio(file_or_path: Union[AudioSegment, BinaryIO, PathLike]):
    if not isinstance(file_or_path, AudioSegment):
        file_or_path = AudioSegment.from_file(file_or_path)
    play(file_or_path)
