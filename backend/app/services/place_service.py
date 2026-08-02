from sqlalchemy import func

from app.extensions import db
from app.models import Review


def attach_review_stats(places):
    place_ids = [p.id for p in places]

    if not place_ids:
        return []

    stats = (
        db.session.query(
            Review.place_id,
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("average_rating"),
        )
        .filter(Review.place_id.in_(place_ids))
        .group_by(Review.place_id)
        .all()
    )

    stats_by_place = {s.place_id: s for s in stats}

    results = []
    for place in places:
        data = place.to_dict()
        stat = stats_by_place.get(place.id)
        data["review_count"] = stat.review_count if stat else 0
        data["average_rating"] = round(float(stat.average_rating), 1) if stat and stat.average_rating else None
        results.append(data)

    return results
