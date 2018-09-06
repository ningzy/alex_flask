import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-know'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rippleidea:Ripple3616@alexflask.cxhafjw1sser.us-east-1.rds.amazonaws.com:3306/alexdb'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'alex.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'test_images')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    S3_BUCKET = 'alex-upload-flask'
    S3_KEY = 'AKIAJGRGCUNBPS4W6XZQ'
    S3_SECRET = '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'
    S3_LOCATION = 'https://s3.amazonaws.com/{}'.format(S3_BUCKET)
