from Models import *
from customer_controller import *
from hotel_controller import *
from menu_controller import *
from customer_order_controller import *
from hotel_order_controller import *


@app.route('/app/welcome/')
def start_page():
    return rt('welcome.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    # db.drop_all()








