import uuid
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user = 'root'
password = 'Meina9758'
database = 'RDPS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@10.1.0.110:3306/%s' % (user, password, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class rdps(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(255))
    token = db.Column(db.String(255))
    serial = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    lasttime = db.Column(db.DateTime)
    activedays = db.Column(db.Integer)


@app.route('/rdps', methods=['POST'])
def get_rdps():
    data = request.get_json()
    recived_uuid = data['uuid']
    serial = data['serial']
    if not recived_uuid:
        return jsonify({'message': 'uuid is missing'}), 400
    if not serial:
        return jsonify({'message': 'invalid access'}), 400
    try:
        uuid.UUID(recived_uuid)
    except ValueError:
        return jsonify({'message': 'uuid is invalid format'}), 400
    session = db.session()
    result = session.query(rdps).filter_by(token=recived_uuid).first()
    if result:
        # check if the uuid exist
        if result.lasttime:
            # check if the uuid is expired
            current_time = datetime.now()
            if result.lasttime < current_time:
                session.close()
                return jsonify({'message': 'uuid is expired'}), 403
            else:
                if serial != result.serial:
                    # check if the uuid is used on the same device
                    session.close()
                    return jsonify({'message': 'not same device'}), 403
                else:
                    days_left = (result.lasttime - current_time).days
                    username = result.username
                    passwd = result.password
                    session.close()
                    return jsonify({'username': username, 'password': passwd, 'days_left': days_left}), 200
            # return the username and password  if the uuid is not expired
        else:
            if not result.serial:
                # check if the record has serial
                result.serial = serial
                days = result.activedays
                expire_time = datetime.now() + timedelta(days=days)
                result.lasttime = expire_time
                session.commit()
                days_left = (result.lasttime - datetime.now()).days
                username = result.username
                passwd = result.password
                session.close()
                return jsonify({'username': username, 'password': passwd, 'days_left': days_left}), 200
            if serial != result.serial:
                # check if the uuid is used on the same device
                session.close()
                return jsonify({'message': 'not same device'}), 403
            # if serial == result.serial:
            #     # check if the uuid is used on the same device
            #     days_left = (result.lasttime - datetime.now()).days
            #     username = result.username
            #     passwd = result.password
            #     session.close()
            #     return jsonify({'username': username, 'password': passwd, 'days_left': days_left}), 200

    else:
        session.close()
        return jsonify({'message': 'uuid is not exist'}), 403
    # return if the uuid is not exist


if __name__ == '__main__':
    app.run()
