from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask import flash
from functools import wraps
import sqlite3
import os
import base64
from datetime import timedelta, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tst.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

connect = sqlite3.connect("test5.db",check_same_thread=False)
cursor = connect.cursor()


login_manager = LoginManager()
login_manager.init_app(app)

def add_main_admin():
    Admin = User(username='kaktus', password=generate_password_hash('23022007', method='pbkdf2:sha256', salt_length=16), role = 'Administrator')
    db.session.add(Admin)
    db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    contact_info = db.Column(db.String(200), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    last_active = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_user_online(user):
    if user.last_active:
        return datetime.now() - user.last_active < timedelta(minutes=5)  # Считаем онлайн, если активен в последние 5 минут
    return False

#authorisation
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_panel'))
        else:
            print("Неверный пароль")
    return render_template('login.html')

def role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))  # Перенаправление, если пользователь не аутентифицирован
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    default_avatar_path = 'default-avatar.jpg'
    user.last_active = datetime.now()
    db.session.commit()
    if request.method == 'POST':
        if user:
            user.email = request.form['email']
            user.phone = request.form['phone']
            user.contact_info = request.form['contact_info']
            
            # Если загружено новое изображение
            if request.form['cropped_image']:
                image_data = request.form['cropped_image'].split(',')[1]
                avatar_filename = f'{user.id}_avatar.png'
                avatar_path = os.path.join('static/images', avatar_filename)  # Сохраните как avatar.png или используйте уникальное имя
                with open(avatar_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                user.avatar = avatar_filename
            # Если не загружено новое изображение, оставляем текущее значение
            else:
                user.avatar = user.avatar if user.avatar else default_avatar_path
            db.session.commit()
        else:
            new_user = User(
                email=request.form['email'],
                phone=request.form['phone'],
                contact_info=request.form['contact_info'],
                avatar='avatar.png'
            )
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('profile'))

    avatar_src = user.avatar if (user and user.avatar) else default_avatar_path
    return render_template('admin_profile.html', user=user, avatar_src=avatar_src)

@app.context_processor
def inject_avatar_src():
    if current_user.is_authenticated:
        avatar_src = current_user.avatar if current_user.avatar else 'static/images/default-avatar.jpg'
    else:
        avatar_src = 'static/images/default-avatar.jpg'  # Путь к изображению по умолчанию
    return dict(avatar_src=avatar_src)


@app.route('/admin_list')
@login_required
@role_required
def admin_page():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        current_user.last_active = datetime.now()
        db.session.commit()
        admins = User.query.all()
        for admin in admins:
            admin.online = is_user_online(admin)
        if current_user.role == 'Administrator':
            return render_template('add_admin.html', users=admins)  # Возвращаем страницу для администраторов
        elif current_user.role == 'Moderator':
            return render_template('admin_list.html', users=admins)  # Возвращаем страницу для модераторов
        else:
            return redirect(url_for('login')) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route('/update-order', methods=['POST'])
def update_order():
    data = request.get_json()
    user_id = data.get('userid')
    print(user_id)
    success = data.get('success')
    orderid = data.get('order_number')
    print(orderid)
    print(success)
    if user_id is None or success is None:
        return jsonify({'error': 'Не указаны userId или success'}), 400

    try:
        cursor.execute('UPDATE orders SET success = ? WHERE user_id = ? AND order_number = ? ', (success, user_id, orderid))
        connect.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Запись не найдена'}), 404
        return jsonify({'message': 'Значение обновлено'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#info
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    current_user.last_active = datetime.now()
    db.session.commit()
    admins = User.query.all()
    cursor.execute('SELECT * FROM orders')
    users = cursor.fetchall()
    return render_template('orders.html',users = admins, userss = users)

@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('login'))  # Перенаправляем на страницу авторизации

#add_admin
@app.route('/add_admin', methods=['POST'])
@login_required
def add_admin():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_admin = User(username=username, password=hashed_password, role =role)
    db.session.add(new_admin)
    db.session.commit()
    return redirect(url_for('admin_page'))


@app.route('/delete_admin/<int:user_id>', methods=['POST'])
@login_required
def delete_admin(user_id):
    admin_count = User.query.count()
    if admin_count <= 1:
        return jsonify({"status": "error", "message": "Невозможно удалить последнего администратора"}), 400
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"status": "success", "message": "Администратор успешно удален"}), 200
    else:
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 404


@app.route('/api/data/<int:user_id>/<int:order_id>')
def get_data(user_id, order_id):
    cursor.execute('SELECT * FROM order_products WHERE user_id = ? AND order_id = ?',(user_id, order_id))
    cart = cursor.fetchall()
    data = [] 
    for i in range(len(cart)):
        item_data = {
            'nazv': cart[i][3],
            'price': cart[i][4],
            'art': cart[i][2],
            'quantity': cart[i][5],
            'sumprice': cart[i][6]
        }
        data.append(item_data)
    return jsonify(data)

@app.route('/api/users')
def get_users():
    cursor.execute('SELECT * FROM orders ORDER BY date DESC')
    users = cursor.fetchall()
    page = request.args.get('page', 1, type=int)
    per_page = 15
    total_users = len(users)
    # Вычисляем количество страниц
    total_pages = (total_users + per_page - 1) // per_page  # Округление вверх
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]
    return  jsonify({
        'users': paginated_users,
        'total_pages': total_pages
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)