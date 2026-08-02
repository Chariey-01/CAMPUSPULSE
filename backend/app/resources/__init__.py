def register_resources(api):
    from app.resources.auth import RegisterResource, LoginResource, MeResource
    from app.resources.category import CategoryListResource, CategoryResource
    from app.resources.place import (
        PlaceListResource,
        PlaceResource,
        MyPlacesResource,
        PendingPlacesResource,
        PlaceApproveResource,
        PlaceRejectResource,
    )
    from app.resources.review import ReviewListResource, ReviewResource
    from app.resources.visit_plan import VisitPlanListResource, VisitPlanResource
    from app.resources.bookmark import BookmarkListResource, BookmarkResource
    from app.resources.profile import ProfileResource

    api.add_resource(RegisterResource, "/api/auth/register")
    api.add_resource(LoginResource, "/api/auth/login")
    api.add_resource(MeResource, "/api/auth/me")

    api.add_resource(CategoryListResource, "/api/categories")
    api.add_resource(CategoryResource, "/api/categories/<int:category_id>")

    api.add_resource(PlaceListResource, "/api/places")
    api.add_resource(PlaceResource, "/api/places/<int:place_id>")
    api.add_resource(MyPlacesResource, "/api/places/mine")
    api.add_resource(PendingPlacesResource, "/api/places/pending")
    api.add_resource(PlaceApproveResource, "/api/places/<int:place_id>/approve")
    api.add_resource(PlaceRejectResource, "/api/places/<int:place_id>/reject")

    api.add_resource(ReviewListResource, "/api/places/<int:place_id>/reviews")
    api.add_resource(ReviewResource, "/api/reviews/<int:review_id>")

    api.add_resource(VisitPlanListResource, "/api/visit-plans")
    api.add_resource(VisitPlanResource, "/api/visit-plans/<int:plan_id>")

    api.add_resource(BookmarkListResource, "/api/bookmarks")
    api.add_resource(BookmarkResource, "/api/bookmarks/<int:bookmark_id>")

    api.add_resource(ProfileResource, "/api/profile")
