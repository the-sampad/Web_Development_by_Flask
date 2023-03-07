from werkzeug import security

password = 'Sampad@2000'
new_pass =security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
print(new_pass)