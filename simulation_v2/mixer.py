from typing import Dict

import pygame as pg

from resources import path


class Mixer:
    def __init__(self) -> None:
        self.sounds: Dict[str, pg.mixer.Sound] = {}

    def initialize(self):
        pg.mixer.init(44100, -16, 2, 1024)

        for name in [

        ]:
            self.load_sound(name, name)
            self.sounds[name].set_volume(0.1)

    def load_sound(self, name: str, filename: str):
        self.sounds[name] = pg.mixer.Sound(path("sounds/" + filename + ".wav"))

    def play(self, sound: str) -> None:
        if sound in self.sounds:
            self.sounds[sound].play()

    def play_music(self, music: str) -> None:
        pg.mixer.music.load(path("music/" + music + ".ogg"))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)

    def stop_music(self) -> None:
        pg.mixer.music.fadeout(100)
