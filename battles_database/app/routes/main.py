from flask import Blueprint, render_template

from app.models import Battle, Commander, MilitaryUnit, Country

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    stats = {
        'battles': Battle.query.count(),
        'commanders': Commander.query.count(),
        'units': MilitaryUnit.query.count(),
        'countries': Country.query.count(),
    }

    recent_battles = Battle.query.order_by(Battle.id.desc()).limit(3).all()

    map_battles = []
    for b in Battle.query.all():
        if b.place and b.place.latitude and b.place.longitude:
            v = (b.victory or '').lower()
            if 'french' in v:
                victor = 'france'
            elif 'russian' in v or 'russia' in v:
                victor = 'russia'
            elif 'british' in v or 'allied' in v:
                victor = 'allies'
            else:
                victor = 'other'

            map_battles.append({
                'id': b.id,
                'name': b.name,
                'latitude': float(b.place.latitude),
                'longitude': float(b.place.longitude),
                'year': b.date_begin.year if b.date_begin else 0,
                'victor': victor,
            })

    return render_template(
        'index.html',
        stats=stats,
        recent_battles=recent_battles,
        map_battles=map_battles,
    )