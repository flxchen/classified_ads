class Config:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/userDatabase'
    MAX_CONTENT_LENGTH = 16*1024*1024
    UPLOAD_FOLDER = 'uploads'
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kevinchen346@yahoo.com'
    MAIL_PASSWORD = 'pevcsybtinlyraqn'
    MAIL_DEFAULT_SENDER = 'kevinchen346@yahoo.com'
    STRIPE_PUBLIC_KEY = 'pk_test_51Q8DzKDns5yIkVLKH1mlkaAuTUKNloR0y9DNFimSF54V2qHXJT7OpagITpCnZtAfSoFTOtxvXP9tRqWUdsd0R2K000BZ15tR7s'
    STRIPE_SECRET_KEY = 'sk_test_51Q8DzKDns5yIkVLKlEWX2bkgWqgk12AvLCASVChwGqy9ITwN1nQ3VrgEiejMID6LiTugdeN3j4Brd3TYgHUJfXvl00SQJ0vpz5'