import bcrypt


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


password = "..."


hashed = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)
hashed_str = hashed.decode("utf-8")
print(hashed_str)

if check_password(password, hashed_str):
    login_ok = True
else:
    login_ok = False
