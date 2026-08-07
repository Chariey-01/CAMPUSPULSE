from sqlalchemy import func

from app.extensions import db
from app.models import Review


def attach_review_stats(places):
    # Serialize `places` with review_count/average_rating merged in.

    # Stats are fetched in a single grouped query for all place ids up front
    # (rather than querying per place) to avoid an N+1 query pattern when
    # called with a full page of results.
    
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

    # index by place_id for O(1) lookup while building results below
    stats_by_place = {s.place_id: s for s in stats}

    results = []
    for place in places:
        data = place.to_dict()
        stat = stats_by_place.get(place.id)
        data["review_count"] = stat.review_count if stat else 0
        # average_rating stays None (rather than 0) when a place has no reviews yet,
        # so the frontend can distinguish "unrated" from "rated 0"
        data["average_rating"] = round(float(stat.average_rating), 1) if stat and stat.average_rating else None
        results.append(data)

    return results
