import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projeto-uninter-seguro-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade_v3.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # Ativação global da proteção CSRF
login_manager = LoginManager(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- MODELOS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), default='Morador')
    bio = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    category = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_help = db.Column(db.Boolean, default=False)
    is_urgent = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- ROTAS ---

@app.route('/')
def index():
    cat = request.args.get('category')
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)

    query = Post.query
    if cat:
        query = query.filter_by(category=cat)
    if status_filter == 'resolved':
        query = query.filter_by(is_resolved=True)
    elif status_filter == 'open':
        query = query.filter_by(is_resolved=False)

    # Melhoria técnica: Paginação para eficiência de performance (5 por página)
    pagination = query.order_by(Post.is_urgent.desc(), Post.date_posted.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    stats = {
        'total': Post.query.count(),
        'resolved': Post.query.filter_by(is_resolved=True).count(),
        'urgent': Post.query.filter_by(is_urgent=True, is_resolved=False).count(),
        'members': User.query.count(),
    }

    return render_template('index.html', posts=posts, stats=stats, current_category=cat, pagination=pagination)


@app.route('/dashboard')
def dashboard():
    # Nova rota de extensão: Gera métricas estatísticas de impacto social
    categories = ['Avisos', 'Segurança', 'Eventos', 'Serviços', 'Adoção', 'Doações']
    cat_counts = [Post.query.filter_by(category=c).count() for c in categories]
    
    stats = {
        'total': Post.query.count(),
        'resolved': Post.query.filter_by(is_resolved=True).count(),
        'urgent': Post.query.filter_by(is_urgent=True, is_resolved=False).count(),
        'members': User.query.count(),
    }
    return render_template('dashboard.html', stats=stats, categories=categories, cat_counts=cat_counts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user_type = request.form.get('user_type', 'Morador')

        if len(username) < 3:
            flash('O nome de usuário precisa ter ao menos 3 caracteres.')
            return render_template('register.html')
        if len(password) < 6:
            flash('A senha precisa ter ao menos 6 caracteres.')
            return render_template('register.html')

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Este nome de usuário já está em uso.')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada! Faça login para continuar.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuário ou senha incorretos.')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content', '').strip()
    if not content:
        flash('O conteúdo da publicação não pode estar vazio.')
        return redirect(url_for('index'))

    new_post = Post(
        content=content,
        category=request.form.get('category', 'Avisos'),
        location=request.form.get('location', '').strip() or None,
        is_help='is_help' in request.form,
        is_urgent='is_urgent' in request.form,
        author=current_user
    )

    file = request.files.get('image')
    if file and file.filename != '' and allowed_file(file.filename):
        # Melhoria de segurança: uso de UUID para evitar colisões de nomes de arquivos
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        new_post.image = unique_filename

    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = db.session.get(Post, post_id) or db.first_or_404(Post.query.filter_by(id=post_id))
    content = request.form.get('comment_content', '').strip()
    if content:
        comment = Comment(content=content, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('index') + f'#post-{post_id}')


@app.route('/resolve/<int:post_id>', methods=['POST'])  # Correção do Bug crítico de método
@login_required
def resolve_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author == current_user:
        post.is_resolved = not post.is_resolved
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)