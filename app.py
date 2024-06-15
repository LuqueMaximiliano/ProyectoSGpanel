# app.py
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import requests
from config import Config
from models import db, bcrypt, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        cedula = request.form.get('cedula')
        birth_date = request.form.get('birth_date')
        role = request.form.get('role')
        password = request.form.get('password')

        user = User(full_name=full_name, username=username, cedula=cedula, birth_date=birth_date, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update_counters', methods=['POST'])
@login_required
def update_counters():
    if current_user.role != 'operador':
        return jsonify({"error": "Access forbidden"}), 403

    api_url = "https://api.externa.com/get_counters"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        current_user.cartas_leidas += data.get('cartas_leidas', 0)
        current_user.cartas_recibidas += data.get('cartas_recibidas', 0)
        current_user.linea_amarilla += data.get('linea_amarilla', 0)
        current_user.linea_azul += data.get('linea_azul', 0)
        current_user.videollamadas += data.get('videollamadas', 0)
        current_user.notas_voz_recibidas += data.get('notas_voz_recibidas', 0)
        current_user.notas_voz_enviadas += data.get('notas_voz_enviadas', 0)
        current_user.regalo_virtual += data.get('regalo_virtual', 0)
        current_user.presente += data.get('presente', 0)
        current_user.video_perfil += data.get('video_perfil', 0)
        current_user.adjunto_visto += data.get('adjunto_visto', 0)
        current_user.comision += data.get('comision', 0.0)

        db.session.commit()
        return jsonify({"message": "Counters updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500


@app.route('/get_commissions', methods=['GET'])
@login_required
def get_commissions():
    api_url_1 = "https://api.amolatina.com/credits/commissions/95164215631?from=2024-04-01T00%3A00%3A00.000Z&omit=0&positive=true&select=51&to=2024-04-19T14%3A14%3A40.079Z"
    api_url_2 = "https://api.amolatina.com/credits/commissions/95164215631?from=2024-06-01T00%3A00%3A00.000Z&omit=0&positive=false&select=50&to=2024-06-14T20%3A51%3A04.207Z"

    headers_1 = {
        "Authorization": "Token token=\"09edc648-aee2-4767-b485-de77400eaf6e\"",
        "Accept": "application/json"
    }

    headers_2 = {
        "Authorization": "Token token=\"0128b5f1-3ccf-4493-a39f-0a87eb21eb44\"",
        "Accept": "application/json"
    }

    response_1 = requests.get(api_url_1, headers=headers_1)
    response_2 = requests.get(api_url_2, headers=headers_2)
    
    if response_1.status_code == 200 and response_2.status_code == 200:
        data_1 = response_1.json()
        data_2 = response_2.json()
        combined_data = data_1 + data_2

        # Calculate total monthly and weekly profits
        total_monthly_profit = 0
        total_weekly_profit = 0
        now = datetime.now(timezone.utc)
        one_week_ago = now - timedelta(days=7)

        for commission in combined_data:
            profit = commission['profit']
            total_monthly_profit += profit

            commission_date = datetime.fromisoformat(commission['timestamp'].replace('Z', '+00:00'))
            commission_date = commission_date.replace(tzinfo=timezone.utc)
            if commission_date >= one_week_ago:
                total_weekly_profit += profit
        
        result = {
            "commissions": combined_data,
            "total_monthly_profit": total_monthly_profit,
            "total_weekly_profit": total_weekly_profit
        }

        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500


if __name__ == '__main__':
    app.run(debug=True)
