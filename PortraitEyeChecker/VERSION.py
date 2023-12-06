"""
バージョン情報を管理しています。書き換えないでください。
"""

class Version:
    def __init__(self):
        self.__version = "1.0"
        self.__subver = "0"
        self.__date = "20231206"

    @property
    def subver(self):
        return self.__subver

    @subver.setter
    def subver(self, new_subver):
        self.__subver = new_subver

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, new_version):
        self.__version = new_version

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, new_date):
        self.__date = new_date
