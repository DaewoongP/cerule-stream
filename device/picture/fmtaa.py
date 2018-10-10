import datetime

now = datetime.datetime.now()

print("{}-{}-{}-{}.jpg".format(now.hour, now.minute, now.second, now.microsecond))