from Models import *


def account_types():
    account_types_list = ["Saving Account", "Current Account", "Regular Savings", "NRI Accounts"]
    return account_types_list


def account_types_for_edit_page(account_type):
    account_types_list = account_types()
    account_types_list.remove(account_type)
    account_types_list.insert(0, account_type)
    return account_types_list


@app.route('/app/account/save/', methods=['POST'])
def account_save_update():
    account_object = Account.query.filter_by(accno=req.form['acc_no']).first()
    if account_object:
        account_object.balance = req.form['acc_balance']
        account_object.type = req.form['acc_type']
        db.session.commit()
        if req.form['objecttype'] == 'customer':
            customer_object = Customers.query.filter_by(id=req.form['id']).first()
            action = f"{customer_object.name} ,Your Account Datails Updated Successfully...!"
            return rt('customer_loged_in.html', msg=action, account="update_account", flag='update',
                  customerobject=customer_object)
        if req.form['objecttype'] == 'hotel':
            hotel_object = Hotel.query.filter_by(id=req.form['id']).first()
            action = f"{hotel_object.name} ,Your Account Datails Updated Successfully...!"
            return rt('hotel_loged_in.html', msg=action, account="update_account", flag='update',
                  hotelobject=hotel_object)

    else:
        account_object = Account(accno=req.form['acc_no'], balance=req.form['acc_balance'],
                                     type=req.form['acc_type'])
        db.session.add(account_object)
        db.session.commit()

        if req.form['objecttype'] == 'customer':
            customer_account_object = CustomerAccount(custid=req.form['id'], accno=req.form['acc_no'])
            db.session.add(customer_account_object)
            db.session.commit()

            customer_object = Customers.query.filter_by(id=req.form['id']).first()
            action = f"{customer_object.name}, Your Bank Details Added Successfully...!"
            return rt('customer_loged_in.html', account="account_added", flag= 'update', msg=action ,
                  customerobject=customer_object)

        if req.form['objecttype'] == 'hotel':
            hotel_account_object = HotelAccount(hotelid=req.form['id'], accno=req.form['acc_no'])
            db.session.add(hotel_account_object)
            db.session.commit()

            hotel_object = Hotel.query.filter_by(id=req.form['id']).first()
            action = f"{hotel_object.name}, Your Bank Details Added Successfully...!"
            return rt('hotel_loged_in.html', account="account_added", flag='update', msg=action ,
                  hotelobject=hotel_object)


