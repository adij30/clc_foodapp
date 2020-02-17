from Models import *
from hotel_order_controller import active_menus

def active_hotels():
    if Hotel.query.all():
        return Hotel.query.filter(Hotel.active == 'Y')


def calculate_total_price(dict_of_item_quantity):
    total = 0
    for menu_item, quantity in dict_of_item_quantity.items():
        # print(f"menu_item : {menu_item} quantity :{quantity}")
        menu_object = Menu.query.filter_by(id=menu_item).first()
        # print(f"{menu_object.name} * {quantity} = {(menu_object.price * int(quantity))}" )
        total = total + (menu_object.price * int(quantity))
    return total


@app.route('/app/customer/order/<int:cid>')
def order_page(cid):
    customer_object = Customers.query.filter_by(id=cid).first()
    customer_account_object = CustomerAccount.query.filter_by(custid=cid).first()
    if customer_account_object:
        return rt('order.html', customerobject=customer_object, hotels=active_hotels())
    else:
        action = f''' {customer_object.name}, you didn't add bank details, Kindly update your bank details to proceed with order...'''
        return rt('customer_loged_in.html', msg=action, flag="add_bank", customerobject=customer_object,
                  account=customer_account_object)


@app.route('/app/customer/confirm_order/', methods=['POST'])
def customer_confirm_order():
    hotel_id = req.form.get('hotelid')
    customer_id = req.form.get('customerid')
    d = req.form.to_dict()
    d.pop('placeorder')#this if for remove placeorder button name
    d.pop('hotelid')##this if for remove hotelmenuid, so we can calculate total price
    d.pop('customerid')##this if for remove hotelmenuid, so we can calculate total price
    d = {int(k): int(v) for k, v in d.items()}
    #this set comprehension for convert all str  to int
    #first all key and values are of str type
    menuid_quantity_dict = d
    menu_ids = [*d] #for grtting keys from dict
    #quantity = list(d.values())#for getting values from dict

    # print(d)
    # l = [*d]
    # print(l)

    #this if is checking if all menu quantiy are zero
    if all(value == 0 for value in menuid_quantity_dict.values()):
        print("in if")
        action = "You did'nt select any menu, add menu to place order... "
        return rt('select_menu.html', hid=hotel_id, cid=customer_id,
                  active_menu_list=active_menus(hotel_id),msg = action)
    else:

        hotelmenu_objects_list = []
        for menu_id in menu_ids:
            hotelmenu_object = HotelMenu.query.filter_by(menuid=menu_id).first()
            hotelmenu_objects_list.append(hotelmenu_object)

        # for customer_account_object
        customer_account_object = CustomerAccount.query.filter_by(custid=customer_id).first()
        if customer_account_object:
            customer_account_balance = customer_account_object.account.balance

            return rt('confirm_order.html', total=calculate_total_price(d),
                  menuid_quantity_dict=menuid_quantity_dict, hid=hotel_id, cid=customer_id,
                  hotelmenu_object_list=hotelmenu_objects_list,
                  customer_account_balance=customer_account_balance)


@app.route('/app/customer/hotel/order_placed/', methods=['POST'])
def order_placed():
    a = req.form
    hotel_id = req.form.get('hotelid')
    customer_id = req.form.get('customerid')
    menu_id_list = req.form.getlist('menuids')#this ids are in str type
    menu_id_list = list(map(int, menu_id_list))#now this ids are in int type
    total = req.form['totalamount']
    total = int(total[:-1])#for removing rupee char and convert total into int
    order_object = Orders(status='Pending',amount=total)
    print("menu_id_list :",menu_id_list)
    print(" order_object: ",order_object.__dict__)
    db.session.add(order_object)
    db.session.commit()

    #for OrdersMenu table
    for menuid in menu_id_list:
        oreder_menu_object = OrdersMenu(orderid=order_object.id, menuid=menuid)
        db.session.add(oreder_menu_object)
        db.session.commit()
        print("oreder_menu_object   added")

    #for CustomersOrders table
    customers_orders_object = CustomersOrders(custid=customer_id, orderid=order_object.id)
    db.session.add(customers_orders_object)
    db.session.commit()
    print("customers_orders_object added")


    #for HotelOrders table
    hotel_orders_object = HotelOrders(hotelid=hotel_id, orderid=order_object.id)
    db.session.add(hotel_orders_object)
    db.session.commit()
    print("hotel_orders_object added")


    # for HotelCustomers table
    #first we will check if customer is added in HotelCustomers table, if it is absent , then we add
    hotel_customers_object = HotelCustomers.query.filter_by(custid=customer_id).first()
    if hotel_customers_object:
        print("hotel_customers_object alredy present so we dont add")
        pass
    else:
        hotel_customers_object = HotelCustomers(hotelid=hotel_id, custid=customer_id)
        db.session.add(hotel_customers_object)
        db.session.commit()
        print("hotel_customers_object added")

    customer_object = Customers.query.filter_by(id=customer_id).first()
    return rt('successful_order_placed.html', customerobject=customer_object, data=a,
              total=total,hid=hotel_id, cid=customer_id, order_object=order_object )


@app.route('/app/customer/order_history/<int:cid>' )
def customer_order_history(cid):
    customer_object = Customers.query.filter_by(id=cid).first()
    customers_orders = CustomersOrders.query.filter_by(custid=cid).all()
    return rt('order_history_customer.html', customerobject=customer_object,
              customers_orders=customers_orders)