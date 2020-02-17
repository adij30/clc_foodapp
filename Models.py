# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_security.utils import encrypt_password
from flask import Flask, request as req,render_template as rt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/clc_food_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class Customers(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    name = db.Column("NAME", db.String(50))
    age = db.Column("AGE", db.Integer())
    mobile_no = db.Column("Mobile No", db.BigInteger(), unique=True)
    email = db.Column("EMAIL ID", db.String(50), unique=True)
    password = db.Column("PASSWORD",db.String(50))
    active = db.Column(db.String(10), default='Y')

    cust_acc = db.relationship('CustomerAccount', backref='customer', lazy=False, uselist=False)
    cust_hotel = db.relationship('HotelCustomers', backref='customer', lazy=False, uselist=False)
    cust_order = db.relationship('CustomersOrders', backref='customer', lazy=False, uselist=False)



class Account(db.Model):
    accno = db.Column("ACC_NO", db.Integer(), primary_key=True)
    balance = db.Column("BALANCE", db.Float())
    type = db.Column("TYPE", db.String(20))
    active = db.Column(db.String(10), default='Y')

    acc_cust = db.relationship('CustomerAccount', backref='account', lazy=False, uselist=False)
    acc_hotel = db.relationship('HotelAccount', backref='account', lazy=False, uselist=False)


class Hotel(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    name = db.Column("NAME", db.String(50))
    address = db.Column("ADDRESS", db.String(50))
    speciality = db.Column("SPECIALITY", db.String(50))
    mobile_no = db.Column("Mobile No", db.BigInteger(), unique=True)
    email = db.Column("EMAIL ID", db.String(50), unique=True)
    password = db.Column("PASSWORD", db.String(50))
    active = db.Column(db.String(10), default='Y')


    hotel_acc = db.relationship('HotelAccount', backref='hotel', lazy=False, uselist=False)
    hotel_menu = db.relationship('HotelMenu', backref='hotel', lazy=False, uselist=False)
    hotel_order = db.relationship('HotelOrders', backref='hotel', lazy=False, uselist=False)
    hotel_cust = db.relationship('HotelCustomers', backref='hotel', lazy=False, uselist=False)


class Menu(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    name = db.Column("NAME", db.String(50))
    price = db.Column("PRICE", db.Integer())
    active = db.Column(db.String(10), default='Y')

    menu_hotel = db.relationship('HotelMenu', backref='menu', lazy=False, uselist=False)
    menu_order = db.relationship('OrdersMenu', backref='menu', lazy=False, uselist=False)


class Orders(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    status = db.Column("STATUS", db.String(20))
    time = db.Column("DATE & TIME", db.DateTime(), default=datetime.utcnow)
    amount = db.Column("AMOUNT", db.Integer())
    active = db.Column(db.String(10), default='Y')

    order_hotel = db.relationship('HotelOrders', backref='order', lazy=False, uselist=False)
    order_cust = db.relationship('CustomersOrders', backref='order', lazy=False, uselist=False)
    order_menu = db.relationship('OrdersMenu', backref='order', lazy=False, uselist=False)


class CustomerAccount(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    custid = db.Column("CUSTOMER_ID", db.Integer(), db.ForeignKey('customers.ID'), unique=True, nullable=False)
    accno = db.Column("ACCOUNT_NO", db.Integer(), db.ForeignKey('account.ACC_NO'), unique=True, nullable=False)


class HotelAccount(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    hotelid = db.Column("HOTEL_ID", db.Integer(), db.ForeignKey('hotel.ID'), unique=True, nullable=False)
    accno = db.Column("ACCOUNT_NO", db.Integer(), db.ForeignKey('account.ACC_NO'), unique=True, nullable=False)


class HotelMenu(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    hotelid = db.Column("HOTEL_ID", db.Integer(), db.ForeignKey('hotel.ID'), unique=False, nullable=False)
    menuid = db.Column("MENU_ID", db.Integer(), db.ForeignKey('menu.ID'), unique=True, nullable=False)


class HotelOrders(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    hotelid = db.Column("HOTEL_ID", db.Integer(), db.ForeignKey('hotel.ID'), unique=False, nullable=False)
    orderid = db.Column("ORDER_ID", db.Integer(), db.ForeignKey('orders.ID'), unique=True, nullable=False)


class HotelCustomers(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    hotelid = db.Column("HOTEL_ID", db.Integer(), db.ForeignKey('hotel.ID'), unique=False, nullable=False)
    custid = db.Column("CUSTOMER_ID", db.Integer(), db.ForeignKey('customers.ID'), unique=True, nullable=False)


class CustomersOrders(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    custid = db.Column("CUSTOMER_ID", db.Integer(), db.ForeignKey('customers.ID'), unique=False, nullable=False)
    orderid = db.Column("ORDER_ID", db.Integer(), db.ForeignKey('orders.ID'), unique=True, nullable=False)


class OrdersMenu(db.Model):
    id = db.Column("ID", db.Integer(), primary_key=True)
    orderid = db.Column("ORDER_ID", db.Integer(), db.ForeignKey('orders.ID'), unique=False, nullable=False)
    menuid = db.Column("MENU_ID", db.Integer(), db.ForeignKey('menu.ID'), unique=False, nullable=False)



