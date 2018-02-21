# See linux statvfs command for usage
def df(dir='/'):
	from os import statvfs
	s = statvfs(dir)
	print((s[0]*s[3]) / 1048576,'MB')

df()