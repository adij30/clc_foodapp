from Models import *


def active_menus(hotel_id):
    active_menu_ids = [menu_id for menu_id in HotelMenu.query.filter(HotelMenu.hotelid==hotel_id) if menu_id.menu.active=='Y' ]
    #active_menu_ids = [id.menuid for id in hotel_menu_ids if id.menu.active=='Y']
    #here menu bakref is on HotelMenu table, we use this in ==>id.menu.active=='Y'
    return active_menu_ids


@app.route('/app/hotel/order/menu/', methods=["POST"])
def show_menu_for_place_order():
    hotel_id = req.form.get('hotelnames')
    customer_id = req.form.get('cid')
    return rt('select_menu.html',hid=hotel_id,cid=customer_id,
              active_menu_list=active_menus(hotel_id))


@app.route('/app/hotel/orders/<int:hid>')
def hotel_order_page(hid):
    hotel_object = Hotel.query.filter_by(id=hid).first()
    hotel_orders_objects = HotelOrders.query.filter_by(hotelid=hid).all()

    return rt('hotel_orders.html',  hotelobject=hotel_object,hotel_orders_objects=hotel_orders_objects)


@app.route('/app/hotel/order/accept/<int:order_id>')
def hotel_accept_order(order_id):
    order_object = Orders.query.filter_by(id=order_id).first()
    order_object.status = 'Complete'
    bill_amount = order_object.amount
    db.session.commit()

    # for customer account object
    customer_order_object = order_object.order_cust  # using relationship
    customer_id = customer_order_object.custid
    customer_account_object = CustomerAccount.query.filter_by(custid=customer_id).first()
    customer_account_object.account.balance = customer_account_object.account.balance - bill_amount  # using backref
    db.session.commit()
    # print("customer_account_balance",customer_account_balance)

    # for hotel account object
    hotel_order_object = order_object.order_hotel  # using relationship
    hotel_id = hotel_order_object.hotelid
    hotel_account_object = HotelAccount.query.filter_by(hotelid=hotel_id).first()
    hotel_account_object.account.balance = hotel_account_object.account.balance + bill_amount  # using backref
    db.session.commit()
    # print("hotel_account_balance",hotel_account_balance)

    hotel_object = Hotel.query.filter_by(id=hotel_id).first()
    hotel_orders_objects = HotelOrders.query.filter_by(hotelid=hotel_id).all()

    return rt('hotel_orders.html', hotelobject=hotel_object,
              orderobject=order_object, hotel_orders_objects=hotel_orders_objects)


@app.route('/app/hotel/order/cancel/<int:order_id>')
def hotel_cancel_order(order_id):
    order_object = Orders.query.filter_by(id=order_id).first()
    order_object.status = 'Cancelled'
    db.session.commit()

    hotel_order_object = order_object.order_hotel  # using relationship
    hotel_id = hotel_order_object.hotelid
    hotel_object = Hotel.query.filter_by(id=hotel_id).first()
    hotel_orders_objects = HotelOrders.query.filter_by(hotelid=hotel_id).all()

    return rt('hotel_orders.html', hotelobject=hotel_object,
              orderobject=order_object, hotel_orders_objects=hotel_orders_objects)
