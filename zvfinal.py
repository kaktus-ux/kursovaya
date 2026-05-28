import telebot
from telebot import types
import json
import sqlite3
import time


token = '5503704504:AAE1sSl7x3v_4cE3KcvxAagUpgY4VFuxb34'
payment_token = '381764678:TEST:90999'

bot = telebot.TeleBot(token)
items_per_page = 1
current_pages = {}
connect = sqlite3.connect('test5.db',check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cart_users (
                user_id INTEGER,
                user_name TEXT,
                user_phone TEXT  ,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS cart_products (
               id INTEGER PRIMARY KEY,
                cart_id INTEGER,
                name TEXT,
                price INTEGER,
                article TEXT,
               quantity INTEGER,
               sumprice INTEGER,
               img TEXT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
               order_number INTEGER,
                user_id INTEGER,
                user_name TEXT,
                user_phone TEXT,
               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               success INTEGER DEFAULT 0,
               order_price INTEGER);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS order_products (
               user_id INTEGER,
               order_id INTEGER,
                product_id INTEGER,
                name TEXT,
                price INTEGER,
               quantity INTEGER,
               sumprice INTEGER);''')
connect.commit()

stroit_mat = """
{
    "Стройматериалы": {
        "Асбест": [
            {
                "name": "Шнур асбестовый 5000х8 мм",
                "art": "48895",
                "op": "Шнур асбестовый 5000х8 мм ГОСТ 1779-83 общего назначения, состоит из волокон хризотилового асбеста с примесью хлопка и других химических волокон, используется в уплотнении соединений в различных тепловых агрегатах и теплопроводящих системах. Отпускается бухтой, толщина шнура от 25 мм. Рабочая температура до +400°C.",
                "price": "270",
                "nal": "10",
                "photourl": "https://zv.market/upload/resize_cache/iblock/f2c/450_450_140cd750bba9870f18aada2478b24840a/shnur_asbestovyy_8_mm_dlina_25_m.jpg"
            },
            {
                "name": "Труба асбестоцементная безнапорная 3950х100 мм",
                "art": "7744",
                "op": "Безнапорная асбестовая труба используется для устройства наружных трубопроводов безнапорной канализации, дымоходов, воздуховодов, газоходов, мусоропроводов.",
                "price": "676",
                "nal": "73",
                "photourl": "https://zv.market/upload/iblock/bec/truba_asbestotsementnaya_beznapornaya_100_mm_dlina_3_95_m.jpg"
            },
            {
                "name": "Шифер плоский АЦЭИД ТУ н/п 3000х1500х10 мм",
                "art": "980512",
                "op": "Шифер плоский АЦЭИД ТУ н/п 3000х1500х10 мм - это листовой строительный материал, который производится из портланд цемента, асбеста и воды. Асбест- это минерал, который придает шиферу огнеупорные свойства, а цемент - очень хорошие прочностные характеристики. Благодаря хорошей геометрии и ровной поверхности листов широко используется в строительстве для устройства стен, полов, перегородок, оснований под кровлю, для наружной и внутренней отделки зданий. Шифер является не прессованным.",
                "price": "2285",
                "nal": "32",
                "photourl": "https://zv.market/upload/iblock/1e5/shifer_ploskiy_atseid_3000kh1500kh10_mm.jpg"
            },
            {
                "name": "Муфта соединительная Полиэтиленовая 200 мм безнапорная",
                "art": "7752",
                "op": "Муфта соединительная Полиэтиленовая 200 мм безнапорная - для соединения асбестоцементных безнапорных труб диаметром до 400 мм, трубы большего диаметра соединяются при помощи асбестоцементных муфт для безнапорных асбестоцементных труб. Перед соединением полиэтиленовой муфты с трубой необходимо внутреннюю поверхность конца асбестоцементной безнапорной трубы очистить от заусенцев,грязи и песка на длине 50 мм. Так же после соединения асбестоцементых безнапорных труб, полиэтиленовые муфты нагревают с целью плотного прилегания муфты к трубам, что обеспечивает герметичность соединения.",
                "price": "185",
                "nal": "8",
                "photourl": "https://zv.market/upload/iblock/b2a/mufta_soedinitelnaya_polietilenovaya_200_mm_beznapornaya.jpg"
            },
            {
                "name": "Муфта соединительная Асбестовая 100 мм безнапорная",
                "art": "7747",
                "op": "Муфта соединительная Асбестовая 100 мм безнапорная - это фасонные части к асбестоцементным безнапорным трубам,которые предназначены для соединения безнапорных асбестоцементных труб между собой.",
                "price": "204",
                "nal": "24",
                "photourl": "https://zv.market/upload/iblock/78a/mufta_soedinitelnaya_asbestovaya_100_mm_beznapornaya.jpg"
            }
        ]
    },

    "Металлопрокат": {
        "Листмет":[
            {
                "name": "Угол рифленый для алюминиевого листа Квинтет 60х30х1,5 мм",
                "art": "231595",
                "op": "Угол рифленый для алюминиевого листа Квинтет 60х30х1,5 мм, имеет специальный рельеф поверхности в виде продолговатых рифлей (выступов), расположенных под углом друг к другу. Материал экологически чистый и долговечный в использовании, обладает хорошими противоскользящими свойствами, а также стойкостью к коррозии и механическому воздействию. Использовать его можно в различных температурных условиях и условиях окружающей среды. Углами отделывают ступени зданий, водных и наземных транспортных средств. Кроме того рифленые углы подходят для оригинального тюнинга транспортных средств, прицепов и фургонов.",
                "price": "1532",
                "nal": "9",
                "photourl": "https://zv.market/upload/iblock/7d3/ugol_riflenyy_dlya_alyuminievogo_lista_kvintet_60kh30kh1_5_mm.jpg"
            },
            {
                "name": "Лист алюминиевый рифленый 300х600х1,5 мм Квинтет",
                "art": "231584",
                "op": "Лист алюминиевый рифленый 300х600х1,5 мм Квинтет - это вид листового проката, представляющий собой металлический лист с выпуклым рисунком, выполненным методом продавливания полотна и применяется в различных отраслях промышленности.",
                "price": "1249",
                "nal": "6",
                "photourl": "https://zv.market/upload/iblock/aa9/list_alyuminievyy_riflenyy_300kh600kh1_5_mm_kvintet.jpg"
            }
        ]
    }
}

             """

data = json.loads(stroit_mat)

def start_kb():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    b1 = telebot.types.InlineKeyboardButton('🧱 Строительные материалы', callback_data='Стройматериалы')
    b2 = telebot.types.InlineKeyboardButton('⚙️ Металлопрокат', callback_data='Металлопрокат')
    b3 = telebot.types.InlineKeyboardButton('🪚 Пиломатериалы', callback_data='btn3')
    b4 = telebot.types.InlineKeyboardButton('🖼️ Отделочные материалы', callback_data='btn4')
    b5 = telebot.types.InlineKeyboardButton('🛠️ Инструменты', callback_data='btn5')
    b6 = telebot.types.InlineKeyboardButton('🧷 Скобяные изделия', callback_data='btn6')
    b7 = telebot.types.InlineKeyboardButton('👷🏻‍♂️ Инженерные системы', callback_data='btn7')
    b8 = telebot.types.InlineKeyboardButton('🌳 Товары для сада', callback_data='btn8')
    b9 = telebot.types.InlineKeyboardButton('🦺 Спецодежда', callback_data='btn9')
    b10 = telebot.types.InlineKeyboardButton('💧 Сантехника', callback_data='btn10')
    b11 = telebot.types.InlineKeyboardButton('🌡️ Отопление', callback_data='btn11')
    b12 = telebot.types.InlineKeyboardButton('🔌 Электрика', callback_data='btn12')
    keyboard.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
    b13 = telebot.types.InlineKeyboardButton('🚚 Доставка', callback_data='dst')
    b14 = telebot.types.InlineKeyboardButton('💸 Оплата', callback_data='opl')
    keyboard.row(b13,b14)
    b15 = telebot.types.InlineKeyboardButton('☎️ Контакты', callback_data='cont')
    b16 = telebot.types.InlineKeyboardButton('🛒 Корзина',callback_data='cart')
    keyboard.row(b15,b16)
    return keyboard

@bot.message_handler(commands=['start'])
def send_logo(message):
    logo = 'https://s.rbk.ru/v1_companies_s3/resized/1200xH/media/trademarks/fa08879c-f43d-421a-94dc-297ac98cede6.jpg'
    welcome_text = (f'Добро пожаловать в меню. Я - чат-бот магазина zv.market [ㅤ]({logo})')
    keyboard = start_kb()
    bot.send_message(chat_id=message.chat.id, text=welcome_text, reply_markup=keyboard, parse_mode='Markdown')

def get_kart(number, message, category, subcategory):
    # Получаем данные о товаре из динамической категории и подкатегории
    product = data[category][subcategory][number]
    
    text = f"*{product['name']}* \n\n" \
           f"*Артикул*: {product['art']}    🏷️ *Цена*: {product['price']} руб./шт    ✅ *В наличии*: {product['nal']} \n\n" \
           f"{product['op']}"
    
    photo = product['photourl']
    
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    b2 = telebot.types.InlineKeyboardButton('Купить', callback_data=f'buy_{category}_{subcategory}_{number}')  # Добавлено subcategory для уникальности
    b3 = telebot.types.InlineKeyboardButton('Просмотреть корзину', callback_data='cart')
    keyboard.add(b2, b3)
    
    bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, parse_mode='Markdown', reply_markup=keyboard)


def final_message(message):
    text = '🔄 Были показаны все товары из этой категории'
    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
    bx = telebot.types.InlineKeyboardButton('↩️Назад',callback_data='menu')
    kb.add(bx)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=kb)

def add_to_cart(cart_id, item_id, category, subcategory):
    userid = cart_id
    cursor.execute(f'''SELECT user_id FROM cart_users WHERE user_id = ?''',(userid,))
    dataa = cursor.fetchone()
    if dataa is None:
        cursor.execute('''INSERT INTO cart_users(user_id) VALUES (?)''',(userid,))
        connect.commit()
    else:
        pass
    name = data[category][subcategory][item_id]['name']
    price = data[category][subcategory][item_id]['price']
    article = data[category][subcategory][item_id]['art']
    img = data[category][subcategory][item_id]['photourl']
    quantity = 1
    cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, article))
    existing_product = cursor.fetchone()
    if existing_product:
        new_quantity = existing_product[5] +1
        new_price = existing_product[3]*new_quantity
        cursor.execute('UPDATE cart_products SET quantity = ?, sumprice = ? WHERE cart_id = ? AND article = ? ', (new_quantity, new_price, userid, article))
    else:
        cursor.execute('INSERT INTO cart_products (cart_id, name, price, article, quantity, sumprice, img) VALUES (?, ?, ?, ?, ?, ?, ?)', (cart_id, name, price, article, quantity, price, img))
    connect.commit()
    return article


def cart(chat_id, message_id, userid):
    # Получаем текущую страницу для данного пользователя, если она не установлена, то устанавливаем в 0
    page = current_pages.get(userid, 0)
    
    b = cursor.execute('SELECT COUNT(article) FROM cart_products WHERE cart_id = ?;', (userid,))
    lenn = max([row[0] for row in b])
    start_index = page * items_per_page
    end_index = min((page + 1) * items_per_page, lenn)
    
    cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? LIMIT ? OFFSET ?;', (userid, items_per_page, start_index))
    products = cursor.fetchall()
    
    # Если нет продуктов в корзине
    if not products:
        text = "🛒 Ваша корзина пуста."
        bot.send_message(chat_id=chat_id, text=text)
        return
    
    # Обработка и отображение продуктов
    for product in products:
        name = product[2]
        price = product[3]
        art = product[4]
        quantity = product[5]
        sumprice = product[6]
        img = product[7]
        markup = telebot.types.InlineKeyboardMarkup()
        
        cursor.execute('SELECT sumprice FROM cart_products WHERE cart_id = ?', (userid,))
        prices = cursor.fetchall()
        total_price = sum(int(price[0]) for price in prices)
        
        # Кнопки управления
        bcounter = telebot.types.InlineKeyboardButton(text=f'{page+1}/{lenn}', callback_data='-')
        bp = telebot.types.InlineKeyboardButton(text='<==', callback_data='prev')
        bn = telebot.types.InlineKeyboardButton(text='==>', callback_data='next')
        b1 = telebot.types.InlineKeyboardButton(text='Очистить корзину', callback_data='delete_items')
        b2 = telebot.types.InlineKeyboardButton(text=f'Заказ на {total_price} рублей. Оформить?', callback_data='oform')
        dele = telebot.types.InlineKeyboardButton(text='❌', callback_data=f'full_delete_{art}')
        quaplus = telebot.types.InlineKeyboardButton(text='➕', callback_data=f'plus_{art}')
        quantityb = telebot.types.InlineKeyboardButton(text=f'{quantity} шт', callback_data='-')
        quaminus = telebot.types.InlineKeyboardButton(text='➖', callback_data=f'delete_item_{art}')
        bx = telebot.types.InlineKeyboardButton(text='Продолжить покупки', callback_data='menu')

        # Добавление кнопок в разметку
        if page > 0 and end_index < lenn:
            markup.row(bp, bcounter, bn)
            markup.row(dele, quaminus, quantityb, quaplus)
        elif page > 0 and end_index >= lenn:
            markup.row(bp, bcounter)
            markup.row(dele, quaminus, quantityb, quaplus)
        elif page == 0 and end_index < lenn:
            markup.row(bcounter, bn)
            markup.row(dele, quaminus, quantityb, quaplus)
        elif page == 0 and end_index == lenn:
            markup.row(dele, quaminus, quantityb, quaplus)

        markup.row(b1, bx)
        markup.row(b2)

        text = f'🛒 *Ваша корзина:*\n\n{name} [ ]({img})\n\nАртикул: *{art}*\n\nЦена: *{price}* x *{quantity}*шт = *{sumprice}* руб'
        
        # Отправка сообщения или редактирование
        if message_id:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)
            except telebot.apihelper.ApiTelegramException as e:
                bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=markup)

def delete_item(cursor, item_id, userid):
    # Получаем текущую страницу для данного пользователя
    page = current_pages.get(userid, 0)
    
    cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, item_id))
    existing_product = cursor.fetchone()
    
    if existing_product:
        quantity = existing_product[5]
        if quantity > 1:
            new_quantity = quantity - 1
            new_price = existing_product[3] * new_quantity
            cursor.execute('UPDATE cart_products SET quantity = ?, sumprice = ? WHERE cart_id = ? AND article = ?', (new_quantity, new_price, userid, item_id))
            connect.commit()
        elif quantity == 1:
            cursor.execute('DELETE FROM cart_products WHERE article = ?', (item_id,))
            connect.commit()
            if page >= 1:
                current_pages[userid] = page - 1  # Уменьшаем страницу для данного пользователя

def plus_item(cursor,item_id, userid):
    cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, item_id))
    existing_product = cursor.fetchone()
    quantity = existing_product[5]
    new_quantity = quantity + 1
    new_price = existing_product[3] * new_quantity
    cursor.execute('UPDATE cart_products SET quantity = ?, sumprice = ? WHERE cart_id = ? AND article = ?', (new_quantity, new_price, userid, item_id))
    connect.commit()


def full_delete(cursor, item_id, userid):
    # Получаем текущую страницу для данного пользователя
    page = current_pages.get(userid, 0)
    cursor.execute('DELETE FROM cart_products WHERE article = ?', (item_id,))
    connect.commit()
    if page >= 1:
        current_pages[userid] = page - 1  # Уменьшаем страницу для данного пользователя

def enter_name(message, userid):
    cursor.execute(f'''SELECT * FROM cart_users WHERE user_id = ?''',(userid,))
    dat = cursor.fetchone()
    if dat[1] is None:
        bot.send_message(chat_id=message.chat.id, text = 'Введите свое имя:')
        bot.register_next_step_handler(message, lambda msg: add_name_to_table(msg, userid))
    else:
        kb = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton('Да', callback_data='Yes')
        b2 = telebot.types.InlineKeyboardButton('Нет', callback_data='No')
        kb.row(b1,b2)
        bot.send_message(chat_id=message.chat.id, text= f'{dat[1]} - это ваше имя?', reply_markup=kb)

def add_name_to_table(message, userid):
    user_name = message.text.strip()
    cursor.execute('UPDATE cart_users SET user_name = ? WHERE user_id = ? ', (user_name, userid,))
    connect.commit()
    enter_phone(message, userid)

def enter_phone(message, userid):
    cursor.execute(f'''SELECT * FROM cart_users WHERE user_id = ?''',(userid,))
    dat = cursor.fetchone()
    if dat[2] is None:
        if message.message_id:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text = 'Введите свой номер телефона:')
            except:
                bot.send_message(chat_id=message.chat.id, text='Введите свой номер телефона:')
        else:
            bot.send_message(chat_id=message.chat.id, text='Введите свой номер телефона:')
        bot.register_next_step_handler(message, lambda msg: add_phone_to_table(msg, userid))
    else:
        kb = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton('Да', callback_data='Yes1')
        b2 = telebot.types.InlineKeyboardButton('Нет', callback_data='No1')
        kb.row(b1,b2)
        if message.message_id:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text= f'{dat[2]} - это ваш номер?', reply_markup=kb)
            except:
                bot.send_message(chat_id=message.chat.id, text= f'{dat[2]} - это ваш номер?', reply_markup=kb)
        else:
            bot.send_message(chat_id=message.chat.id, text= f'{dat[2]} - это ваш номер?', reply_markup=kb)

def add_phone_to_table(message, userid):
    user_phon = message.text.strip()
    cursor.execute('UPDATE cart_users SET user_phone = ? WHERE user_id = ? ', (user_phon, userid,))
    connect.commit()
    check_number(message,userid)

def add_phone_to_table_1(message, userid):
    user_phon = message.text.strip()
    cursor.execute('UPDATE cart_users SET user_phone = ? WHERE user_id = ? ', (user_phon, userid,))
    connect.commit()
    payment_methods(message)

def check_number(message,userid):
    cursor.execute(f'''SELECT * FROM cart_users WHERE user_id = ?''',(userid,))
    dat = cursor.fetchone()
    number = dat[2]
    if str(number) not in '+0123456789' and (len(str(number))not in range(11,13)):
        bot.send_message(message.chat.id, text = 'Номер введен некорректно. Введите еще раз:')
        bot.register_next_step_handler(message, lambda msg: add_phone_to_table(msg, userid))
    else:
        add_phone_to_table_1(message,userid)
    
def payment_methods(message):
    kb = telebot.types.InlineKeyboardMarkup()
    b1 = telebot.types.InlineKeyboardButton('Оплата картой', callback_data='credit_card') 
    kb.row(b1)
    b2 = telebot.types.InlineKeyboardButton('Другое', callback_data='other')
    kb.row(b2)
    bx = telebot.types.InlineKeyboardButton('Вернуться', callback_data='cart')
    b3 = telebot.types.InlineKeyboardButton('Подробнее об оплате', callback_data='opl1')
    kb.row(b3,bx)
    if message.message_id:
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите способ оплаты:', reply_markup=kb)
        except:
            bot.send_message(message.chat.id, 'Выберите способ оплаты:',reply_markup=kb)
    else:
        bot.send_message(message.chat.id, 'Выберите способ оплаты:',reply_markup=kb)

def total_price(userid):
    cursor.execute('SELECT sumprice FROM cart_products WHERE cart_id = ?', (userid,))
    prices = cursor.fetchall()
    total_price = sum(int(price[0]) for price in prices)
    tprice = [types.LabeledPrice(label='Сумма заказа', amount=total_price*100)]
    cursor.execute('SELECT * FROM cart_products WHERE cart_id = ?',(userid,))
    products = cursor.fetchall()
    spnames = []
    for product in products:
        name = product[2]
        quantity = product[5]
        if quantity >1:
            n_and_q = str(name)+' x' +str(quantity)
        else:
            n_and_q = str(name)
        spnames.append(n_and_q)
    strnames = ', '.join(spnames)
    return tprice, strnames, total_price

def pay(message,userid):
    bot.send_message(message.chat.id, "Добро пожаловать в процесс оплаты. Нажмите на кнопку ниже, чтобы произвести платеж.")
    totprice = total_price(userid)[0]
    des = total_price(userid)[1]
    total_pr = total_price(userid)[2]
    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
    b1 = telebot.types.InlineKeyboardButton(f'Оплатить {total_pr} RUB', pay=True)
    b2 = telebot.types.InlineKeyboardButton('Вернуться', callback_data='cart')
    kb.add(b1,b2)
    bot.send_invoice(chat_id=message.chat.id, title='Ваш заказ', description=des, invoice_payload='cart', provider_token=payment_token, currency='RUB', prices=totprice, is_flexible=False, provider_data=None, start_parameter='test_bot', reply_markup=kb)

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment(message):
    userid = message.from_user.id
    if message.successful_payment.invoice_payload == 'cart':
        order_price = total_price(userid)[2]
        cursor.execute('SELECT MAX(order_number) FROM orders WHERE user_id = ?', (userid,))
        result = cursor.fetchone()
        order_number = result[0] + 1 if result[0] is not None else 1
        cursor.execute('INSERT INTO orders (user_id, order_number, date, user_phone, user_name, order_price) '
                    'SELECT ?, ?, DATETIME(CURRENT_TIMESTAMP, "+3 hours"), user_phone, user_name, ? FROM cart_users WHERE user_id = ?;',
                    (userid, order_number, order_price, userid))
        connect.commit()
        order_id = order_number
        cursor.execute('INSERT INTO order_products (user_id, order_id, product_id, name, price, quantity, sumprice) '
                    'SELECT cart_id, ?, article, name, price, quantity, sumprice FROM cart_products WHERE cart_id = ?;',
                    (order_id, userid))
        connect.commit()
        cursor.execute('DELETE FROM cart_products WHERE cart_id = ?;', (userid,))
        connect.commit()
        cursor.execute('UPDATE orders SET success = ? WHERE user_id = ? AND order_number = ?', (1, userid, order_id))
        connect.commit()
        kb = telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu'))
        bot.send_message(chat_id=message.chat.id, text="Платеж совершен успешно! Ожидайте звонка в ближайшее время",reply_markup=kb)

def other(message, userid):
    order_price = total_price(userid)[2]
    cursor.execute('SELECT MAX(order_number) FROM orders WHERE user_id = ?', (userid,))
    result = cursor.fetchone()
    order_number = result[0] + 1 if result[0] is not None else 1
    cursor.execute('INSERT INTO orders (user_id, order_number, date, user_phone, user_name, order_price) '
                'SELECT ?, ?, DATETIME(CURRENT_TIMESTAMP, "+3 hours"), user_phone, user_name, ? FROM cart_users WHERE user_id = ?;',
                (userid, order_number, order_price, userid))
    connect.commit()
    order_id = order_number
    cursor.execute('INSERT INTO order_products (user_id, order_id, product_id, name, price, quantity, sumprice) '
                'SELECT cart_id, ?, article, name, price, quantity, sumprice FROM cart_products WHERE cart_id = ?;',
                (order_id, userid))
    connect.commit()
    cursor.execute('DELETE FROM cart_products WHERE cart_id = ?;', (userid,))
    connect.commit()
    cursor.execute('UPDATE orders SET success = ? WHERE user_id = ? AND order_number = ?', (0, userid, order_id))
    connect.commit()
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu'))
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text='Данные отправлены, ожидайте звонка',reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    userid = call.from_user.id
    current_page = current_pages.get(userid, 0)
    data_parts = call.data.split('_')
    if call.message:
        print(data_parts)
        if call.data == "dst":
            kb = telebot.types.InlineKeyboardMarkup()
            kb.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu'))
            dost = 'Доставка товара производится до подъезда, дачи, коттеджа исключительно при наличии подъездных путей, предназначенных для проезда грузовых автомобилей.\n\nСтроительная база Золотые Ворота расположена в Домодедовском районе, доставка осуществляется по Москве и Московской области\n\nСтоимость доставки товара рассчитывается индивидуально, ниже приведены формулы для расчета стоимость доставки:\n\n - Транспорт до 1500 кг или до 2 м3 - до 10 км 1000 рублей, свыше за каждый километр по 50 руб\n - Транспорт до 4700 кг или до 6 м3 - до 10 км 2500 рублей, свыше за каждый километр по 100 руб\n - Транспорт до 10000 кг или до 10 м3 - до 10 км 4000 рублей, свыше за каждый километр по 130 руб\n\nДоставка осуществляется в течение дня в порядке очереди, в случае необходимости экспресс-доставки стоимость увеличивается в 2 раза\n\nДоставка товара производится до подъезда, дачи, коттеджа исключительно при наличии подъездных путей, предназначенных для проезда грузовых автомобилей.'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=dost,reply_markup=kb)
        if call.data == "opl":
            oplata = '*Оплата наличными*\n\n При выборе варианта оплаты наличными, Вы дожидаетесь приезда водителя и оплачиваете заказ на месте.\n\nТакже оплата наличными доступна при самовывозе из магазина.\n\n*Безналичный расчёт*\n\nПри оформлении заказа в корзине Вы можете выбрать вариант безналичной оплаты. Мы принимаем карты Visa, Master Card и МИР.\n\nВам могут отказать от авторизации в случае:\n\n-если ваш банк не поддерживает технологию 3D-Secure;\n-на карте недостаточно средств для покупки;\n-истекло время ожидания ввода данных;\n-в данных была допущена ошибка.\n\nВы можете сообщить менеджеру об ошибке и он повторно выставит счет на Вашу электронную почту, либо воспользоваться другой картой, или обратиться в свой банк для решения вопроса, если ошибка возникла снова.\n\nТакже оплата картой доступна при самовывозе товара из магазина.\n\n*Покупка в кредит*\n\nВы можете оформить кредит на заказанный товар выбрав соответствующий вариант при оформлении заказа.'
            kb = telebot.types.InlineKeyboardMarkup()
            kb.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=oplata, parse_mode= "Markdown",reply_markup=kb)
        if call.data == 'opl1':
            oplata = '*Оплата наличными*\n\n При выборе варианта оплаты наличными, Вы дожидаетесь приезда водителя и оплачиваете заказ на месте.\n\nТакже оплата наличными доступна при самовывозе из магазина.\n\n*Безналичный расчёт*\n\nПри оформлении заказа в корзине Вы можете выбрать вариант безналичной оплаты. Мы принимаем карты Visa, Master Card и МИР.\n\nВам могут отказать от авторизации в случае:\n\n-если ваш банк не поддерживает технологию 3D-Secure;\n-на карте недостаточно средств для покупки;\n-истекло время ожидания ввода данных;\n-в данных была допущена ошибка.\n\nВы можете сообщить менеджеру об ошибке и он повторно выставит счет на Вашу электронную почту, либо воспользоваться другой картой, или обратиться в свой банк для решения вопроса, если ошибка возникла снова.\n\nТакже оплата картой доступна при самовывозе товара из магазина.\n\n*Покупка в кредит*\n\nВы можете оформить кредит на заказанный товар выбрав соответствующий вариант при оформлении заказа.'
            kb = telebot.types.InlineKeyboardMarkup()
            b2 = telebot.types.InlineKeyboardButton('Назад', callback_data='payment_methods')
            kb.add(b2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=oplata, parse_mode= "Markdown",reply_markup=kb)
        if call.data == "cont":
            cont = 'Адрес: Городской округ Домодедово, село ЯМ, ул. Почтовая, Владение 1\n\nРежим работы: Пн. – Вс.: 8:00-23:00 Без выходных!\n\nОтдел по работе с корпоративными клиентами:\nb2b@zv.market\n8 (499) 702-74-34\n\nТелефон:\n8 800 250 76 26\n8 499 702 55 45\n\nE-mail: info@zv.market'
            kb = telebot.types.InlineKeyboardMarkup()
            kb.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cont, reply_markup=kb)
        if call.data == 'menu':
            logo = 'https://s.rbk.ru/v1_companies_s3/resized/1200xH/media/trademarks/fa08879c-f43d-421a-94dc-297ac98cede6.jpg'
            welcome_text = (f'Добро пожаловать в меню. Я - чат-бот магазина zv.market [ㅤ]({logo})')
            keyboard = start_kb()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_text, reply_markup=keyboard, parse_mode='Markdown')
        if call.data == 'payment_methods':
            payment_methods(call.message)
        if call.data == 'cart':
            kb = telebot.types.InlineKeyboardMarkup()
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=kb)
            products_list = cursor.execute('SELECT * FROM cart_products WHERE cart_id =? ;',(userid,)).fetchall()
            if len(products_list)==0:
                kb = telebot.types.InlineKeyboardMarkup()
                kb.add(telebot.types.InlineKeyboardButton('↩️В меню',callback_data='menu'))
                if call.message.message_id:
                    try:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= 'Ваша корзина пуста 😔', reply_markup=kb)
                    except:
                        bot.send_message(chat_id=call.message.chat.id, text= 'Ваша корзина пуста 😔', reply_markup=kb)
                else:
                    bot.send_message(chat_id=call.message.chat.id, text= 'Ваша корзина пуста 😔', reply_markup=kb)
            else:
                cart(call.message.chat.id, call.message.message_id, userid)
        if call.data.startswith('buy_'):
            # Извлекаем данные из callback_data
            data_parts1 = call.data.split('_')
            category = data_parts1[1] 
            subcategory = data_parts1[2]
            item_id1 = int(data_parts1[3])
            art = add_to_cart(userid, item_id1, category, subcategory)
            bot.answer_callback_query(call.id, 'Корзина обновлена', show_alert=False)
            
            cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, art))
            existing_product = cursor.fetchone()
            
            if existing_product:
                quantityb = existing_product[5]
                kb = telebot.types.InlineKeyboardMarkup()
                quaplus = telebot.types.InlineKeyboardButton(text='➕', callback_data=f'plus1_{art}')
                quantityb_btn = telebot.types.InlineKeyboardButton(text=f'{quantityb} шт', callback_data='-')
                quaminus = telebot.types.InlineKeyboardButton(text='➖', callback_data=f'delete_item1_{art}')
                
                kb.row(quaminus, quantityb_btn, quaplus)
                kb.row(telebot.types.InlineKeyboardButton('Просмотреть корзину', callback_data='cart'))
                
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)
        if call.data.startswith('delete_item1_'):
            item_id = int(call.data.split('_')[-1])
            cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, item_id))
            existing_product = cursor.fetchone()
            quantityb = existing_product[5]
            if quantityb >1:
                delete_item(cursor, item_id, userid)
                bot.answer_callback_query(call.id, 'Количество уменьшено!', show_alert=False)
                cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, item_id))
                existing_product = cursor.fetchone()
                quantityb = existing_product[5]
                kb = telebot.types.InlineKeyboardMarkup()
                quaplus = telebot.types.InlineKeyboardButton(text='➕', callback_data=f'plus1_{item_id}')
                quantityb = telebot.types.InlineKeyboardButton(text=f'{quantityb} шт', callback_data='-')
                quaminus = telebot.types.InlineKeyboardButton(text='➖', callback_data=f'delete_item1_{item_id}')
                kb.row(quaminus,quantityb,quaplus)
                kb.row(telebot.types.InlineKeyboardButton('Просмотреть корзину', callback_data='cart'))
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)
            else:
                full_delete(cursor, item_id)
                index = next((i for i, d in enumerate(data['Асбестотехнические изделия']) if d['art'] == str(item_id)), None)
                bot.answer_callback_query(call.id, 'Позиция удалена', show_alert=False)
                kb = telebot.types.InlineKeyboardMarkup()
                b1 = telebot.types.InlineKeyboardButton('Купить', callback_data=f'buy_{index}')
                b2 = telebot.types.InlineKeyboardButton('Просмотреть корзину', callback_data='cart')
                kb.row(b1, b2)
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)
        if data_parts[0]=='plus1':
            item_id = int(call.data.split('_')[-1])
            plus_item(cursor, item_id, userid)
            bot.answer_callback_query(call.id, 'Количество увеличено!', show_alert=False)
            cursor.execute('SELECT * FROM cart_products WHERE cart_id = ? AND article = ?', (userid, item_id))
            existing_product = cursor.fetchone()
            quantityb = existing_product[5]
            kb = telebot.types.InlineKeyboardMarkup()
            quaplus = telebot.types.InlineKeyboardButton(text='➕', callback_data=f'plus1_{item_id}')
            quantityb = telebot.types.InlineKeyboardButton(text=f'{quantityb} шт', callback_data='-')
            quaminus = telebot.types.InlineKeyboardButton(text='➖', callback_data=f'delete_item1_{item_id}')
            kb.row(quaminus,quantityb,quaplus)
            kb.row(telebot.types.InlineKeyboardButton('Просмотреть корзину', callback_data='cart'))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)
        if call.data.startswith('delete_item_'):
            item_id = int(call.data.split('_')[-1])
            delete_item(cursor, item_id, userid)
            bot.answer_callback_query(call.id, 'Количество уменьшено!', show_alert=False)
            prod_list = cursor.execute('SELECT * FROM cart_products WHERE cart_id = ?;', (userid,)).fetchall()
            if len(prod_list) > 0:
                cart(call.message.chat.id, call.message.message_id, userid)
            else:
                text = 'Ваша корзина пуста 😔'
                kb = telebot.types.InlineKeyboardMarkup()
                kb.add(telebot.types.InlineKeyboardButton('↩️Назад',callback_data='menu'))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=kb)
        if call.data.startswith('plus_'):
            item_id = int(call.data.split('_')[-1])
            plus_item(cursor, item_id, userid)
            bot.answer_callback_query(call.id, 'Количество увеличено!', show_alert=False)
            cart(call.message.chat.id, call.message.message_id, userid)
        if call.data.startswith('full_delete_'):
            item_id = int(call.data.split('_')[-1])
            full_delete(cursor, item_id, userid)
            bot.answer_callback_query(call.id, 'Предмет удален', show_alert=False)
            prod_list = cursor.execute('SELECT * FROM cart_products WHERE cart_id = ?;', (userid,)).fetchall()
            if len(prod_list) > 0:
                cart(call.message.chat.id, call.message.message_id, userid)
            else:
                text = 'Ваша корзина пуста 😔'
                kb = telebot.types.InlineKeyboardMarkup()
                kb.add(telebot.types.InlineKeyboardButton('↩️Назад',callback_data='menu'))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=kb)
        if call.data == 'delete_items':
            cursor.execute('DELETE FROM cart_products WHERE cart_id = ?;',(userid,))
            connect.commit()
            bot.answer_callback_query(call.id,'Корзина очищена',show_alert=False)
            text = 'Ваша корзина пуста 😔'
            kb = telebot.types.InlineKeyboardMarkup()
            kb.add(telebot.types.InlineKeyboardButton('↩️Назад',callback_data='menu'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=kb)
        if call.data == 'prev' and current_page > 0:
            current_pages[userid] = current_page - 1
            cart(call.message.chat.id, call.message.message_id, userid)
            bot.answer_callback_query(call.id)
        elif call.data == 'next':
            current_pages[userid] = current_page + 1
            cart(call.message.chat.id, call.message.message_id, userid)
            bot.answer_callback_query(call.id)
        if call.data == 'oform':
            enter_name(call.message, userid)
        if call.data == 'Yes':
            enter_phone(call.message, userid)
        if call.data == 'No':
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = 'Введите свое имя:')
            bot.register_next_step_handler(call.message,userid, add_name_to_table)
        if call.data == 'Yes1':
            payment_methods(call.message)
        if call.data == 'No1':
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = 'Введите свой номер телефона:')
            bot.register_next_step_handler(call.message,userid,add_phone_to_table)
        if call.data == 'credit_card':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            pay(call.message,userid)
        if call.data == 'other':
            other(call.message, userid)
        # Проверяем, является ли нажатая кнопка категорией
        if len(data_parts) == 1 and data_parts[0] in data:
            category = data_parts[0]  # Динамически устанавливаем категорию
            kb = telebot.types.InlineKeyboardMarkup(row_width=1)
            # Добавляем подкатегории в клавиатуру
            for subcat in data[category]:
                button = types.InlineKeyboardButton(text=subcat, callback_data=f"{category}_{subcat}")
                kb.add(button)
            bx = telebot.types.InlineKeyboardButton('Вернуться', callback_data='menu')
            kb.add(bx)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите подкатегорию:', reply_markup=kb)

        # Проверяем, является ли нажатая кнопка подкатегорией
        elif len(data_parts) == 2 and data_parts[0] in data:
            category, subcategory = data_parts
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, text=f"Вы выбрали подкатегорию: {subcategory}", reply_markup=None)
            current_count = len(data[category][subcategory])
            # Вызываем функцию get_kart для получения первых товаров
            for number in range(current_count//2):  # Измените диапазон по необходимости
                get_kart(number, call.message, category, subcategory)
            # Добавляем кнопку "Показать больше"
            text = '🔄 Было показано несколько товаров из этой категории'
            kb = telebot.types.InlineKeyboardMarkup(row_width=2)
            b1 = telebot.types.InlineKeyboardButton('⬇️Показать еще', callback_data=f'show_more_{category}_{subcategory}')
            bx = telebot.types.InlineKeyboardButton('↩️Назад',callback_data='menu')
            kb.add(b1,bx)
            bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=kb)

        # Обработка нажатия на кнопку "Показать больше"
        elif len(data_parts) == 4 and data_parts[0] == 'show':
            category, subcategory = data_parts[2], data_parts[3]
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            current_count = len(data[category][subcategory])
            for i in range(current_count//2, current_count):
                get_kart(i, call.message, category, subcategory)
            final_message(call.message)






while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(5)  # Ждем 5 секунд перед повторной попыткой