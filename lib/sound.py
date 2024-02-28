from pygame import mixer


class Sound:
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound("./assets/sound//main_theme.ogg")
        self.coin = mixer.Sound("./assets/sound//coin.ogg")
        self.bump = mixer.Sound("./assets/sound//bump.ogg")
        self.stomp = mixer.Sound("./assets/sound//stomp.ogg")
        self.jump = mixer.Sound("./assets/sound//small_jump.ogg")
        self.death = mixer.Sound("./assets/sound//death.wav")
        self.kick = mixer.Sound("./assets/sound//kick.ogg")
        self.brick_bump = mixer.Sound("./assets/sound//brick-bump.ogg")
        self.powerup = mixer.Sound('./assets/sound//powerup.ogg')
        self.powerup_appear = mixer.Sound('./assets/sound//powerup_appears.ogg')
        self.pipe = mixer.Sound('./assets/sound//pipe.ogg')

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
