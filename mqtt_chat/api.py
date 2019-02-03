from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker
from pprint import pprint
from flask import request, jsonify
import hashlib
import sqlite3


app = Flask(__name__)

engine = create_engine('sqlite:///reg.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uid = Column(String, primary_key = True)
    pasw = Column(String, nullable = False)
    usig = Column(String , nullable = False)
    contact = Column(String, nullable = False)
    
    def __repr__(self):
        return "<User('%s',%s,'%s',%s)>" % (self.uid, self.pasw, self.usig,self.contact)


@app.route('/api/v1.0/UserRegistration')
def user_reg():
    
    if 'username' not in request.args or 'contact' not in request.args or 'password' not in request.args:
        return jsonify({'message':'One or more mandatory field was found empty','status':201})
    else:
        username = request.args['username']
        contact = request.args['contact']
        password = request.args['password']
        salt = hashlib.sha256()
        salt.update(username.encode())
        salt.update(contact.encode())
        usersig = salt.hexdigest()
        salt = hashlib.sha256()
        salt.update(password.encode())
        passhash = salt.hexdigest()
        
        session = Session()
        
        try:
            session.add(User( uid = username,pasw = passhash ,usig = usersig,contact = contact ))
            session.commit()
        except:
            session.rollback()
            
        return jsonify({'message':'User successfully registered','username':username,'status':200})

@app.route('/api/v1.0/UserValidation')
def user_val():
    
    session = Session()
    
    if 'username' not in request.args or 'password' not in request.args :
        return jsonify({'message':'One or more mandatory field was found empty','status':201})
    
    else:
        
        try:
            row = session.query(User).filter_by(uid = request.args['username']).first()
            session.commit()
        except:
            session.rollback()
            
        if not row :
            
            return jsonify({'message':'User not registered' , 'status' : 202})
        
        else :
            
            password = request.args['password']
            salt = hashlib.sha256()
            salt.update(password.encode())
            if salt.hexdigest() == row.pasw :
                return jsonify({'message':'Validation passed' , 'status':200})
            else :
                return jsonify({'message':'Validation failed , Incorrect password','status':203})
            
            
@app.route('/api/v1.0/UserSignature')
def user_sig():
    
    session = Session()
    if 'username' in request.args:
        
        try:
            ob = session.query(User).filter_by(uid = request.args['username'] ).first()
            session.commit()
        except:
            session.rollback()
            
        return jsonify({'signature': ob.usig ,'status':200})  
    
    elif 'contact' in request.args:
        
        try:
            ob = session.query(User).filter_by(contact = request.args['contact'] ).first()
            session.commit()
        except:
            session.rollback()
            
        return jsonify({'signature': ob.usig ,'status':200})
        
    else:
        return jsonify({'message':'Provide username or contact to get signature','status':201})

@app.route('/api/v1.0/AllUsers')
def all_user():
    session = Session()
    try:
        res = jsonify([d.uid for d in session.query(User).all()])
        session.commit()
    except:
        session.rollback()
        
    return res

if __name__ == '__main__':
    app.run(debug=True)
