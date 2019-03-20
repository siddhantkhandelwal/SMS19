# URL Endpoints

- /accounts/login -> Login | name='account_login' or can also use {{ login_url }}
- /accounts/signup -> Signup | name='account_signup' or can also use {{ signup_url }}
- /accounts/password/reset -> Forgot Password | name='account_reset_password'
- /accounts/password/set -> Set password for the current logged in user | name='account_set_password'
- /accounts/password/change -> Change password for a logged in user | name='account_change_password'
- /accounts/logout -> Logout | name='account_logout'

### Note
- Difference between set password and change password is that when a person logs in through Google OAuth , no password is set, so set password is used . But when a user who had created a normal profile wants to change the passwords , then set password is used .
