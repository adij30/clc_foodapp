from Models import *


def all_active_menu(hid):
    #both query give same output
    # menu_ids = [i.menuid for i in HotelMenu.query.filter_by(hotelid=hid).all()]
    # print(menu_ids)
    menu_ids = [hotelmenu.menu for hotelmenu in HotelMenu.query.filter(HotelMenu.hotelid==hid)]
    #above here i use backref menu
    active_menu_ids = list(filter(lambda x:x.active=='Y',menu_ids))
    return active_menu_ids


@app.route('/app/hotel/menu/<int:hotelid>')
def menu_page(hotelid):
    hotel_object = Hotel.query.filter_by(id=hotelid).first()
    return rt('menu.html', menus=all_active_menu(hotelid), hotelobject=hotel_object)


@app.route('/app/hotel/menu/add/', methods=['POST'])
def menu_save_update():
    hotel_id = req.form['hid']
    hotel_object = Hotel.query.filter_by(id=hotel_id).first()
    menu_object = Menu.query.filter_by(id=req.form['mid']).first()
    if menu_object:
        menu_object.name = req.form['mname'].title()
        menu_object.price = req.form['mprice']
        db.session.commit()
        action = f"{menu_object.name} menu updated successfully..."
        return rt('menu.html', menus=all_active_menu(hotel_id), msg=action,
                  hotelobject=hotel_object)

    else:
        menu_object = Menu(name=req.form['mname'].title(),price=req.form['mprice'])
        db.session.add(menu_object)
        db.session.commit()

        menu_id = menu_object.id
        hotel_menu_object = HotelMenu(hotelid=hotel_id,menuid=menu_id)
        db.session.add(hotel_menu_object)
        db.session.commit()

        action = f"{req.form['mname'].title()} menu added successfully..."
        return rt('menu.html',menus=all_active_menu(hotel_id), msg=action, hotelobject=hotel_object)


@app.route('/app/hotel/menu/edit/<int:mid>', methods=['GET'])
def menu_edit(mid):
    hotel_menu_object = HotelMenu.query.filter_by(menuid=mid).first()
    hotel_id = hotel_menu_object.hotelid
    hotel_object = Hotel.query.filter_by(id=hotel_id).first()

    menu_object = Menu.query.filter_by(id=mid).first()
    return rt('menu.html', menus=all_active_menu(hotel_id), menu=menu_object, hotelobject=hotel_object)


@app.route('/app/hotel/menu/delete/<int:mid>', methods=['GET'])
def menu_delete(mid):
    hotel_menu_object = HotelMenu.query.filter_by(menuid=mid).first()
    hotel_id = hotel_menu_object.hotelid
    hotel_object = Hotel.query.filter_by(id=hotel_id).first()

    menu_object = Menu.query.filter_by(id=mid).first()
    menu_name = menu_object.name
    menu_object.active='N'
    #db.session.delete(menu_object)
    db.session.commit()
    action = f"Menu Record of {menu_name} with ID {mid} Deleted Successfully...!"
    return rt('menu.html', menus=all_active_menu(hotel_id), msg=action, hotelobject=hotel_object)

