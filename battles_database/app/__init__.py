from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from markupsafe import escape


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Регистрация пользовательских фильтров Jinja2
    from app.filters import init_app as init_filters
    init_filters(app)
    
    # Добавляем фильтр escapejs
    @app.template_filter('escapejs')
    def escape_js(text):
        return escape(text)

    # Регистрация роутов
    from app.routes import init_app as init_routes
    init_routes(app)
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

     # 👇 1. Передача allow_editing во все шаблоны
    @app.context_processor
    def inject_globals():
        return {
            'allow_editing': app.config.get('ALLOW_EDITING', True)
        }

    # 👇 2. Защита от POST-запросов и захода на /new и /edit
    @app.before_request
    def block_editing_if_disabled():
        if app.config.get('ALLOW_EDITING', True):
            return  # Всё разрешено
            
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            abort(403)
            
        if request.endpoint:
            if 'new_' in request.endpoint or 'edit_' in request.endpoint:
                abort(403)

    # 👇 3. Красивая страница ошибки 403
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

        
    return app