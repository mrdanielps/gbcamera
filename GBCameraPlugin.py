import os

from PIL import Image, ImageFile


class GBCamImageFile(ImageFile.ImageFile):
    format = "GBCamera"
    format_description = "Game Boy Camera save file"

    __fp = None
    __frame = 0
    _n_frames = 30

    def _open(self):
        self.fp.seek(0, os.SEEK_END)
        if self.fp.tell() != 131072:
            raise SyntaxError("GB Camera save file must be 128K")

        self.mode = "P"
        self.size = (16 * 8, 14 * 8)

        # Apparently ImageFile does 'self.fp = None' after loading, so we must keep a reference to it.
        self.__fp = self.fp
        self.seek(0)

        p = [156, 189, 15, 140, 173, 15, 48, 98, 48, 15, 56, 15]
        p += [0] * (768 - len(p))
        self.putpalette(p)

    def load_read(self, n):
        res = b''

        # GB tiles are described here: https://github.com/jansegre/gameboy/blob/master/spec/gbspec.txt#L274
        data = self.fp.read(16)
        for y in range(8):
            for x in reversed(range(8)):
                c = ((data[y * 2] >> x) & 1) * 2 + ((data[y * 2 + 1] >> x) & 1)
                res += bytes([c])

        return res

    def seek(self, frame):
        if frame >= self._n_frames:
            raise EOFError

        self.__frame = frame
        self.fp = self.__fp

        # GBCamera pictures start at 0x2000, and have the following structure:
        #  * Large photo (16x14 tiles, 0xe00 bytes)
        #  * Small photo (4x4 tiles, 0x100 bytes)
        #  * Photo info (0x100 bytes)
        # More info here: http://www.devrs.com/gb/files/gbcam.txt
        self.tile = []
        for t in range(16 * 14):
            x = (t % 16) * 8
            y = (t // 16) * 8
            self.tile.append(("raw", (x, y, x + 8, y + 8), 0x2000 + 0x1000 * self.__frame + 16 * t, (self.mode, 0, 1)))

    def tell(self):
        return self.__frame

Image.register_open("GBCamera", GBCamImageFile)
Image.register_extension("GBCamera", ".sav")
