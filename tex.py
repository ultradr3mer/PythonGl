import numpy as np
from OpenGL.GL import *
from OpenGL.raw.GL.EXT.texture_compression_s3tc import *

from ddsfile import *


class Tex:
    def __init__(self, filename):
        dds_file = DDSFile(filename)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        for mip_map_level in range(0, len(dds_file.images)):
            img = dds_file.images[mip_map_level]

            if dds_file.dxt_id == 0:
                glTexImage2D(GL_TEXTURE_2D,
                             mip_map_level,
                             GL_RGB8,
                             dds_file.images_size[mip_map_level][0],
                             dds_file.images_size[mip_map_level][1],
                             0,
                             GL_RGB,
                             GL_UNSIGNED_BYTE,
                             np.frombuffer(img, dtype='ubyte'))
            else:
                glCompressedTexImage2D(GL_TEXTURE_2D,
                                       mip_map_level,
                                       Tex.get_internal_format(dds_file),
                                       dds_file.images_size[mip_map_level][0],
                                       dds_file.images_size[mip_map_level][1],
                                       0,
                                       np.frombuffer(img, dtype='ubyte'))

        glFinish()

        self.handle = texture

        pass

    @staticmethod
    def get_internal_format(dds_file: DDSFile):
        if dds_file.dxt_id == DDS_DXT1:
            return GL_COMPRESSED_RGB_S3TC_DXT1_EXT

        if dds_file.dxt_id == DDS_DXT3:
            return GL_COMPRESSED_RGBA_S3TC_DXT3_EXT

        if dds_file.dxt_id == DDS_DXT5:
            return GL_COMPRESSED_RGBA_S3TC_DXT5_EXT

        raise NotImplementedError()
