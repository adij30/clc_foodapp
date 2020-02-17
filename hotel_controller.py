from Models import *
from customer_controller import encrypt_data,decrypt_data
from account_controller import *


def speciality_list():
    l = ['Veg','Non-Veg','Chinese','South-Indian']
    return l


@app.route('/app/hotel/login/')
def hotel_page():
    return rt('hotel_log_in.html')


@app.route('/app/hotel/sign_up/')
def hotel_sign_up():
    return rt('hotel_sign_up.html',speciality_list = speciality_list())


@app.route('/app/hotel/logout/<name>')
def hotel_logout(name):
    action = f"{name} You have Successfully Logout..."
    return rt('welcome.html', flag='hotel_logout', notification=action)


@app.route('/app/hotel/save/',methods=['POST'])
def hotel_save():
    password = encrypt_data(req.form['hpassword1'])
    hotel_object = Hotel(name=req.form['hname'].title(), address= req.form['haddress'].title(),
                         speciality=req.form['hspeciality'],mobile_no=req.form['hmobileno'],
                         email=req.form['hemail'],password=password)
    db.session.add(hotel_object)
    db.session.commit()
    action = 'Your account created successfully, Use your details to log in...'
    return rt('hotel_log_in.html', flag='signup', notification=action)


@app.route('/app/hotel/log_in/', methods=['POST'])
def hotel_log_in():
    if req.method == 'POST':
        user_id = req.form['huserid']
        user_password = req.form['hpassword']

        if '@' in user_id:
            user_email = user_id
            hotel_object = Hotel.query.filter_by(email=user_email).first()
        else:
            user_mobile = user_id
            hotel_object = Hotel.query.filter_by(mobile_no=user_mobile).first()

        if hotel_object:
            password_database = hotel_object.password
            password_database = "b'"+password_database+"'"
            user_password = encrypt_data(user_password)
            user_password = str(user_password)

            # print("user_password :", type(user_password))
            # print("password :", type(password_database))

            if user_password == password_database:
                acc = HotelAccount.query.filter_by(hotelid=hotel_object.id).first()
                print("acc :", acc)
                return rt('hotel_loged_in.html',  hotelobject=hotel_object, account=acc)
            else:
                action = "The password that you've entered is incorrect..."
                return rt('hotel_log_in.html', msg=action )
        else:
            action = "The email address or phone number that you've entered doesn't match any account. Sign up for an account."
            return rt('hotel_log_in.html', msg=action)


@app.route('/app/hotel/account/<int:id>', methods=['GET'])
def hotel_account(id):
    hotel_object = Hotel.query.filter_by(id=id).first()
    hotel_account_object = HotelAccount.query.filter_by(hotelid=id).first()
    if hotel_account_object:
        account_type_list=account_types_for_edit_page(hotel_account_object.account.type)
        #here account is backref , using that , i am retrive bank type of hotel

    else:
        account_type_list=account_types()

    return rt('account.html', object_data=hotel_account_object, account_types=account_type_list,
              object=hotel_object, object_type='hotel')


@app.route('/app/hotel/edit/<int:id>', methods=['GET'])
def hotel_edit(id):
    hotel_object = Hotel.query.filter_by(id=id).first()

    p = hotel_object.password
    p1 = decrypt_data(p.encode())
    p1= str(p1)
    #print(p1[2::], type(p1))
    hotel_object.password = p1[2:-1:]
    #print(hotel_object.password)

    l = speciality_list()
    l.remove(hotel_object.speciality)
    l.insert(0,hotel_object.speciality)

    return rt('hotel_edit.html', hotelobject=hotel_object, speciality_list=l)


@app.route('/app/hotel/update/', methods=['POST'])
def hotel_update():
    hotel_object = Hotel.query.filter_by(id=req.form['hid']).first()

    hotel_object.name = req.form['hname'].title()
    hotel_object.address = req.form['haddress'].title()
    hotel_object.speciality = req.form['hspeciality']
    hotel_object.mobile_no = req.form['hmobileno']
    hotel_object.email = req.form['hemail']

    password = encrypt_data(req.form['hpassword1'])
    hotel_object.password = password

    db.session.commit()

    acc = HotelAccount.query.filter_by(hotelid=hotel_object.id).first()
    action = 'Your Profile Updated Successfully...'
    return rt('hotel_loged_in.html', flag='update', msg=action,
              hotelobject=hotel_object, account=acc)


@app.route('/app/hotel/log_in_page/<int:hid>')
def hotel_home_page(hid):
    hotel_object = Hotel.query.filter_by(id=hid).first()
    acc = HotelAccount.query.filter_by(hotelid=hotel_object.id).first()
    return rt('hotel_loged_in.html', hotelobject=hotel_object, account=acc)



