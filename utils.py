from itsdangerous import URLSafeSerializer
from flask import current_app


def generatResetTokens(email):
    s = URLSafeSerializer(current_app.secret_key)
    return s.dumps(email,salt='password-reset')

def varifyResetTokens(token,max_age=3600):  # expires after 1 hour
    s = URLSafeSerializer(current_app.secret_key)

    try:
        email = s.loads(token, salt='password-reset',max_age=max_age)
    except:
        return None
    return email

