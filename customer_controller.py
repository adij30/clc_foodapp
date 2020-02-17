from Models import *
from account_controller import *
import base64


def encrypt_data(password):
    password = base64.b64encode(password.encode('utf-8', errors='strict'))
    return password


def decrypt_data(password):
    password = base64.b64decode(password.decode('utf-8', errors='strict'))
    return password


@app.route('/app/customer/login/')
def customer_page():
    return rt('customer_log_in.html')


@app.route('/app/customer/sign_up/')
def customer_sign_up():
    return rt('customer_sign_up.html')


@app.route('/app/customer/logout/<name>')
def customer_logout(name):
    action = f" {name} You have Successfully Logout..."
    return rt('welcome.html', flag='user_logout', notification=action)


@app.route('/app/customer/save/',methods=['POST'])
def customer_save():
    password = encrypt_data(req.form['cpassword1'])
    customer_object = Customers(password=password, name=req.form['cname'].title(),
                                age=req.form['cage'], mobile_no=req.form['cmobileno'],
                                email=req.form['cemail'])
    db.session.add(customer_object)
    db.session.commit()
    action = 'Your account created successfully, Use your details to log in...'
    return rt('customer_log_in.html',flag='user_signup',notification=action)


@app.route('/app/customer/loged_in/', methods=['POST'])
def customer_log_in():
    user_id = req.form['cuserid']
    user_password = req.form['cpassword']

    if '@' in user_id:
        user_email = user_id
        customer_object = Customers.query.filter_by(email=user_email).first()
    else:
        user_mobile = user_id
        customer_object = Customers.query.filter_by(mobile_no=user_mobile).first()

    if customer_object:
        password_database = customer_object.password
        password_database = "b'"+password_database+"'"
        user_password = encrypt_data(user_password)
        user_password = str(user_password)

        # print("user_password :", type(user_password))
        # print("password :", type(password_database))

        if user_password == password_database:
            acc = CustomerAccount.query.filter_by(custid=customer_object.id).first()
            print("acc :",acc)
            return rt('customer_loged_in.html', customerobject =customer_object,
                      account=acc)
        else:
            action = "The password that you've entered is incorrect..."
            return rt('customer_log_in.html', msg=action )
    else:
        action = "The email address or phone number that you've entered doesn't match any account. Sign up for an account."
        return rt('customer_log_in.html', msg=action)


@app.route('/app/customer/loged_in_page/<int:cid>')
def customer_home_page(cid):
    customer_object = Customers.query.filter_by(id=cid).first()
    acc = CustomerAccount.query.filter_by(custid=customer_object.id).first()
    return rt('customer_loged_in.html', customerobject=customer_object, account=acc)


@app.route('/app/customer/edit/<int:id>', methods=['GET'])
def customer_edit(id):
    customer_object = Customers.query.filter_by(id=id).first()

    p = customer_object.password
    p1 = decrypt_data(p.encode())
    p1= str(p1)
    #print(p1[2::], type(p1))
    customer_object.password = p1[2:-1:]
    print(customer_object.password)

    return rt('customer_edit.html', customerobject =customer_object)


@app.route('/app/customer/update/', methods=['POST'])
def customer_update():
    customer_object = Customers.query.filter_by(id=req.form['cid']).first()
    customer_object.name = req.form['cname']
    customer_object.age = req.form['cage']
    customer_object.mobile_no = req.form['cmobileno']
    customer_object.email = req.form['cemail']

    password = encrypt_data(req.form['cpassword1'])
    customer_object.password = password
    db.session.commit()

    acc = CustomerAccount.query.filter_by(custid=customer_object.id).first()
    action = 'Your Profile Updated Successfully...'
    return rt('customer_loged_in.html', flag='update', msg=action, customerobject=customer_object, account=acc)


@app.route('/app/customer/account/<int:id>', methods=['GET'])
def customer_account(id):
    customer_object = Customers.query.filter_by(id=id).first()
    customer_account_object = CustomerAccount.query.filter_by(custid=id).first()
    if customer_account_object:
        account_type_list=account_types_for_edit_page(customer_account_object.account.type)
        #here account is backref , using that , i am retrive bank type of customer
        print(account_type_list)
    else:
        account_type_list=account_types()
        print(account_type_list)
        print(type(customer_object))

    return rt('account.html', object_data=customer_account_object, account_types = account_type_list,
              object=customer_object, object_type = 'customer')

