# 基类，read和add方法留空
class Record:
    def read(self):
        pass

    def add(self, user):
        pass


# 核心代码是裸露的
class KeyRecords(Record):
    def __init__(self):
        self.users = ['admin']

    def read(self):
        return ' '.join(self.users)

    def add(self, user):
        self.users.append(user)


# 定义了针对record类的错误基类
class RecordError(Exception):
    def __init__(self):
        self.message = 'Access Record Failed'


class AddUserNotAllowedRecordError(RecordError):
    def __init__(self, user):
        self.message = "Add user of {} failed due to no permission!".format(user)


class ReadUsersNotAllowedRecordError(RecordError):
    def __init__(self):
        self.message = "read users not allowed due to no permission!"


# 继承自record
class ProxyRecords(Record):
    def __init__(self):
        self.key_records = KeyRecords()  # 作为了属性
        self.secret = 'test'  # 硬编码密码，不推荐，仅示例

    def read(self, pwd=None):
        if self.secret == pwd:
            return self.key_records.read()
        else:
            raise ReadUsersNotAllowedRecordError()

    def add(self, pwd=None, user=None):
        if self.secret == pwd:
            self.key_records.add(user)
        else:
            raise AddUserNotAllowedRecordError(user)
        return 1


def main():
    pr = ProxyRecords()
    pwd = input("plz input the pwd:")
    try:
        pr.read(pwd)
        # 注意如果read中抛出并且捕获了异常，不会继续执行try
        if pr.add(pwd, 'zjc'):
            print("ADD Succeeded...")
    except ReadUsersNotAllowedRecordError as runare:
        print(runare.message)
    except AddUserNotAllowedRecordError as aunare:
        print(aunare.message)
    except RecordError as re:
        print(re.message)


if __name__ == '__main__':
    main()
