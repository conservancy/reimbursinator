import hashlib

hasher = hashlib.md5()
with open ('simple_policy.py', 'rb') as afile:
	buf = afile.read()
	hasher.update(buf)
print("md5 of simple:   " + hasher.hexdigest())

hasher = hashlib.md5()
with open ('moderate_policy.py', 'rb') as afile:
	buf = afile.read()
	hasher.update(buf)
print("md5 of moderate: " + hasher.hexdigest())



hasher = hashlib.sha1()
with open ('simple_policy.py', 'rb') as afile:
	buf = afile.read()
	hasher.update(buf)
print("sha1 of simple:   " + hasher.hexdigest())

hasher = hashlib.sha1()
with open ('moderate_policy.py', 'rb') as afile:
	buf = afile.read()
	hasher.update(buf)
print("sha1 of moderate: " + hasher.hexdigest())
