from app import create_app
from app.extensions import db
from app.models import User, Profile, Category, Place, Review, VisitPlan, Bookmark
from app.utils.security import hash_password


def clear_data():
    Bookmark.query.delete()
    VisitPlan.query.delete()
    Review.query.delete()
    Place.query.delete()
    Profile.query.delete()
    User.query.delete()
    Category.query.delete()
    db.session.commit()


def seed_data():
    app = create_app()

    with app.app_context():
        print("Clearing existing data...")
        clear_data()

        print("Seeding categories...")
        cafeteria = Category(name="Cafeteria", icon="utensils", description="Places to eat on campus")
        library = Category(name="Library", icon="book", description="Study and reading spaces")
        gym = Category(name="Gym", icon="dumbbell", description="Fitness and sports facilities")
        db.session.add_all([cafeteria, library, gym])
        db.session.commit()

        print("Seeding users...")
        admin = User(
            username="admin",
            email="admin@campuspulse.com",
            password_hash=hash_password("admin123"),
            role="admin",
        )
        jane = User(
            username="jane_doe",
            email="jane@campuspulse.com",
            password_hash=hash_password("password123"),
            role="student",
        )
        john = User(
            username="john_smith",
            email="john@campuspulse.com",
            password_hash=hash_password("password123"),
            role="student",
        )
        db.session.add_all([admin, jane, john])
        db.session.commit()

        print("Seeding profiles...")
        db.session.add_all([
            Profile(user_id=admin.id, bio="System administrator", course="N/A", year_of_study=0),
            Profile(user_id=jane.id, bio="Loves coffee and quiet study spots", course="Computer Science", year_of_study=2),
            Profile(user_id=john.id, bio="Gym regular", course="Business", year_of_study=3),
        ])
        db.session.commit()

        print("Seeding places...")
        place1 = Place(
            name="Java House Campus Branch",
            description="Popular coffee shop near the main gate",
            address="Main Gate, Block A",
            phone="0712345678",
            opening_hours="7:00 AM - 9:00 PM",
            google_maps_link="https://maps.google.com/?q=java+house",
            category_id=cafeteria.id,
            submitted_by=jane.id,
            approved_by=admin.id,
            status="Approved",
        )
        place2 = Place(
            name="Main Library",
            description="Central campus library with silent study rooms",
            address="Academic Block C",
            opening_hours="8:00 AM - 10:00 PM",
            google_maps_link="https://maps.google.com/?q=main+library",
            category_id=library.id,
            submitted_by=john.id,
            approved_by=admin.id,
            status="Approved",
        )
        place3 = Place(
            name="Student Gym",
            description="Campus fitness center",
            address="Sports Complex",
            opening_hours="6:00 AM - 8:00 PM",
            category_id=gym.id,
            submitted_by=jane.id,
            status="Pending",
        )
        db.session.add_all([place1, place2, place3])
        db.session.commit()

        print("Seeding reviews...")
        db.session.add_all([
            Review(user_id=john.id, place_id=place1.id, rating=5, comment="Best coffee on campus!"),
            Review(user_id=jane.id, place_id=place2.id, rating=4, comment="Quiet and clean, great for finals week"),
        ])
        db.session.commit()

        print("Seeding visit plans...")
        db.session.add(VisitPlan(user_id=jane.id, place_id=place3.id, status="Planned", notes="Go after morning classes"))
        db.session.commit()

        print("Seeding bookmarks...")
        db.session.add(Bookmark(user_id=john.id, place_id=place1.id))
        db.session.commit()

        print("Seeding complete.")


if __name__ == "__main__":
    seed_data()
