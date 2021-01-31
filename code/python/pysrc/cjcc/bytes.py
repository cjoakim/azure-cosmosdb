__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.10.22"

import humanize


class Bytes(object):

    @classmethod
    def human_readable(cls, n):
        return humanize.intcomma(n) 

    @classmethod
    def kilobyte(cls):
        return 1024

    @classmethod
    def kilobytes(cls, n):
        return Bytes.kilobyte() * abs(float(n))

    @classmethod
    def megabyte(cls):
        return pow(1024, 2)

    @classmethod
    def megabytes(cls, n):
        return Bytes.megabyte() * abs(float(n))

    @classmethod
    def gigabyte(cls):
        return pow(1024, 3)

    @classmethod
    def gigabytes(cls, n):
        return Bytes.gigabyte() * abs(float(n))

    @classmethod
    def terabyte(cls):
        return pow(1024, 4)

    @classmethod
    def terabytes(cls, n):
        return Bytes.terabyte() * abs(float(n))

    @classmethod
    def petabyte(cls):
        return pow(1024, 5)

    @classmethod
    def petabytes(cls, n):
        return Bytes.petabyte() * abs(float(n))

    @classmethod
    def exabyte(cls):
        return pow(1024, 6)

    @classmethod
    def exabytes(cls, n):
        return Bytes.exabyte() * abs(float(n))

    @classmethod
    def zettabyte(cls):
        return pow(1024, 7)

    @classmethod
    def zettabytes(cls, n):
        return Bytes.zettabyte() * abs(float(n))

    @classmethod
    def yottabyte(cls):
        return pow(1024, 8)

    @classmethod
    def yottabytes(cls, n):
        return Bytes.yottabyte() * abs(float(n))

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

    @classmethod
    def as_zettabytes(cls, n):
        return float(abs(n)) / float(cls.zettabyte())

    @classmethod
    def as_yottabytes(cls, n):
        return float(abs(n)) / float(cls.yottabyte())
