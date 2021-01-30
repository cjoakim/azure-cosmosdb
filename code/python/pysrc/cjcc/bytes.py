__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.05.28"


class Bytes(object):

    @classmethod
    def kilobyte(cls):
        return 1024

    @classmethod
    def megabyte(cls):
        return pow(1024, 2)

    @classmethod
    def gigabyte(cls):
        return pow(1024, 3)

    @classmethod
    def terabyte(cls):
        return pow(1024, 4)

    @classmethod
    def petabyte(cls):
        return pow(1024, 5)

    @classmethod
    def exabyte(cls):
        return pow(1024, 6)

    @classmethod
    def zettabyte(cls):
        return pow(1024, 7)

    @classmethod
    def yottabyte(cls):
        return pow(1024, 8)

    @classmethod
    def as_kilobytes(cls, n):
        return float(abs(n)) / float(cls.kilobyte())

    @classmethod
    def as_megabytes(cls, n):
        return float(abs(n)) / float(cls.megabyte())

    @classmethod
    def as_gigabytes(cls, n):
        return float(abs(n)) / float(cls.gigabyte())

    @classmethod
    def as_terabytes(cls, n):
        return float(abs(n)) / float(cls.terabyte())

    @classmethod
    def as_petabytes(cls, n):
        return float(abs(n)) / float(cls.petabyte())
