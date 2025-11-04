from hashlib import sha512

user_a = {'username': 'manager', 'password': '1111'}
user_b = {'username': 'bbb', 'password': '1111'}

hashed_a = sha512((user_a['username'] + user_a['password']).encode('utf-8'))
hashed_b = sha512((user_b['username'] + user_b['password']).encode('utf-8'))

print(hashed_a.hexdigest())
print(hashed_b.hexdigest())

u = input("Username: ")
p = input("Password: ")
hashed = sha512((u + p).encode('utf-8')).hexdigest()
print(hashed)

if hashed == hashed_a.hexdigest():
    print("User A")
elif hashed == hashed_b.hexdigest():
    print("User B")
else: 
    print("Invalid user")
