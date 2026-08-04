from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import User, Profile, Category, Place, Review, VisitPlan, Bookmark
from app.utils.security import hash_password


def clear_data():
    # delete children before parents - respects foreign key constraints
    Bookmark.query.delete()
    VisitPlan.query.delete()
    Review.query.delete()
    Place.query.delete()
    Profile.query.delete()
    User.query.delete()
    Category.query.delete()
    db.session.commit()


CATEGORY_DATA = [
    # name, icon, description
    ("Cafeteria", "utensils", "Places to eat on campus"),
    ("Library", "book", "Study and reading spaces"),
    ("Gym", "dumbbell", "Fitness and sports facilities"),
    ("Hostel", "home", "Student accommodation"),
    ("Clinic", "heart-pulse", "Health and medical services"),
    ("Stationery", "pencil", "Books, printing, and supplies"),
    ("Transport", "bus", "Campus transport stops"),
    ("Entertainment", "music", "Relaxation and leisure spots"),
]

USER_DATA = [
    # username, email, password, role, bio, course, year_of_study
    ("admin", "admin@campuspulse.com", "admin123", "admin", "System administrator", "N/A", 0),
    ("superadmin", "superadmin@campuspulse.com", "password123", "admin", "Platform manager", "N/A", 0),
    ("jane_doe", "jane@campuspulse.com", "password123", "student", "Loves quiet study spaces.", "Computer Science", 2),
    ("john_smith", "john@campuspulse.com", "password123", "student", "Gym enthusiast.", "Business", 3),
    ("alice_wanjiru", "alice@campuspulse.com", "password123", "student", "Enjoys coffee shops.", "Software Engineering", 1),
    ("brian_kiptoo", "brian@campuspulse.com", "password123", "student", "Football fan.", "Mechanical Engineering", 4),
    ("faith_njeri", "faith@campuspulse.com", "password123", "student", "Always at the library.", "Nursing", 2),
    ("kevin_otieno", "kevin@campuspulse.com", "password123", "student", "Photography lover.", "Information Technology", 3),
    ("grace_cherono", "grace@campuspulse.com", "password123", "student", "Bookworm.", "Education", 1),
    ("daniel_kamau", "daniel@campuspulse.com", "password123", "student", "Sketches campus buildings.", "Architecture", 4),
]

PLACE_DATA = [
    # name, category, submitted_by, status, description, address, opening_hours
    ("Java House Campus Branch", "Cafeteria", "jane_doe", "Approved", "Popular coffee shop near the main gate", "Main Gate, Block A", "7:00 AM - 9:00 PM"),
    ("Student Cafeteria", "Cafeteria", "john_smith", "Approved", "The main dining hall for students", "Central Block", "6:30 AM - 9:00 PM"),
    ("Mama Njeri Kitchen", "Cafeteria", "alice_wanjiru", "Approved", "Home-style meals at student prices", "Behind Hall B", "8:00 AM - 8:00 PM"),
    ("Campus Grill", "Cafeteria", "brian_kiptoo", "Approved", "Grilled snacks and fast food", "Sports Complex Road", "10:00 AM - 10:00 PM"),
    ("Old Cafeteria Extension", "Cafeteria", "kevin_otieno", "Rejected", "Proposed extension to the old cafeteria", "East Wing", "N/A"),
    ("Main Library", "Library", "faith_njeri", "Approved", "Central campus library with silent study rooms", "Academic Block C", "8:00 AM - 10:00 PM"),
    ("Engineering Library", "Library", "brian_kiptoo", "Approved", "Technical resources for engineering students", "Engineering Block", "8:00 AM - 9:00 PM"),
    ("Digital Learning Centre", "Library", "alice_wanjiru", "Approved", "Computers and online resources", "Academic Block D", "8:00 AM - 8:00 PM"),
    ("Student Gym", "Gym", "jane_doe", "Approved", "Campus fitness center", "Sports Complex", "6:00 AM - 8:00 PM"),
    ("Sports Complex", "Gym", "brian_kiptoo", "Approved", "Football and basketball facilities", "South Campus", "6:00 AM - 9:00 PM"),
    ("Fitness Hub", "Gym", "kevin_otieno", "Approved", "Modern gym equipment and personal training", "Hall A Basement", "6:00 AM - 10:00 PM"),
    ("Hall A Hostel", "Hostel", "daniel_kamau", "Approved", "First-year student accommodation", "North Campus", "24 hours"),
    ("Hall B Hostel", "Hostel", "grace_cherono", "Approved", "Mixed accommodation block", "North Campus", "24 hours"),
    ("Sunrise Hostel", "Hostel", "faith_njeri", "Pending", "Off-campus student housing", "East Gate", "24 hours"),
    ("Campus Medical Centre", "Clinic", "john_smith", "Approved", "Primary healthcare for students", "Admin Block", "8:00 AM - 6:00 PM"),
    ("Student Wellness Clinic", "Clinic", "grace_cherono", "Approved", "Counseling and wellness services", "Student Centre", "9:00 AM - 5:00 PM"),
    ("Campus Bookshop", "Stationery", "daniel_kamau", "Approved", "Textbooks and supplies", "Main Gate", "8:00 AM - 6:00 PM"),
    ("Smart Print Centre", "Stationery", "kevin_otieno", "Approved", "Printing and photocopying", "Library Annex", "8:00 AM - 8:00 PM"),
    ("Quick Copies", "Stationery", "alice_wanjiru", "Approved", "Fast, affordable printing", "Student Centre", "8:00 AM - 7:00 PM"),
    ("Main Bus Stop", "Transport", "john_smith", "Approved", "Main campus shuttle and bus stop", "Main Gate", "5:30 AM - 10:00 PM"),
    ("North Gate Shuttle Stop", "Transport", "jane_doe", "Approved", "Shuttle stop for North Campus residents", "North Gate", "6:00 AM - 9:00 PM"),
    ("Student Lounge", "Entertainment", "grace_cherono", "Pending", "Relaxation space with sofas and Wi-Fi", "Student Centre", "9:00 AM - 11:00 PM"),
    ("Amphitheatre", "Entertainment", "daniel_kamau", "Approved", "Open-air venue for events", "Central Campus", "Open access"),
    ("Gaming Hub", "Entertainment", "kevin_otieno", "Pending", "Console and PC gaming lounge", "Student Centre", "10:00 AM - 10:00 PM"),
]

REVIEW_DATA = [
    # place, reviewer, rating, comment
    ("Java House Campus Branch", "john_smith", 5, "Best coffee on campus."),
    ("Java House Campus Branch", "alice_wanjiru", 4, "Friendly staff."),
    ("Java House Campus Branch", "brian_kiptoo", 5, "Amazing ambience."),
    ("Java House Campus Branch", "faith_njeri", 4, "Affordable meals."),
    ("Java House Campus Branch", "kevin_otieno", 3, "Crowded during lunch."),

    ("Main Library", "jane_doe", 5, "Very quiet."),
    ("Main Library", "grace_cherono", 4, "Perfect for revision."),
    ("Main Library", "daniel_kamau", 5, "Excellent internet."),
    ("Main Library", "alice_wanjiru", 3, "Needs more charging ports."),
    ("Main Library", "brian_kiptoo", 5, "Helpful librarians."),

    ("Engineering Library", "kevin_otieno", 4, "Good resources."),
    ("Engineering Library", "faith_njeri", 5, "Peaceful."),
    ("Engineering Library", "john_smith", 4, "Comfortable chairs."),
    ("Engineering Library", "grace_cherono", 5, "Great study environment."),
    ("Engineering Library", "jane_doe", 3, "Small space."),

    ("Student Gym", "daniel_kamau", 5, "Modern equipment."),
    ("Student Gym", "alice_wanjiru", 4, "Affordable."),
    ("Student Gym", "faith_njeri", 5, "Very clean."),
    ("Student Gym", "grace_cherono", 3, "Busy evenings."),
    ("Student Gym", "kevin_otieno", 4, "Helpful trainers."),

    ("Sports Complex", "jane_doe", 4, "Large football field."),
    ("Sports Complex", "john_smith", 5, "Basketball court is great."),
    ("Sports Complex", "daniel_kamau", 4, "Well maintained."),
    ("Sports Complex", "alice_wanjiru", 5, "Excellent facilities."),
    ("Sports Complex", "faith_njeri", 4, "Good lighting."),

    ("Campus Medical Centre", "grace_cherono", 5, "Professional nurses."),
    ("Campus Medical Centre", "kevin_otieno", 4, "Quick service."),
    ("Campus Medical Centre", "jane_doe", 5, "Clean environment."),
    ("Campus Medical Centre", "brian_kiptoo", 3, "Long queues."),
    ("Campus Medical Centre", "daniel_kamau", 4, "Friendly doctor."),

    ("Student Lounge", "alice_wanjiru", 5, "Relaxing."),
    ("Student Lounge", "faith_njeri", 4, "Nice sofas."),
    ("Student Lounge", "john_smith", 5, "Great atmosphere."),
    ("Student Lounge", "brian_kiptoo", 3, "Needs more charging points."),
    ("Student Lounge", "grace_cherono", 4, "Excellent Wi-Fi."),

    ("Campus Bookshop", "kevin_otieno", 5, "Affordable books."),
    ("Campus Bookshop", "jane_doe", 4, "Helpful staff."),
    ("Campus Bookshop", "daniel_kamau", 4, "Fast printing."),
    ("Campus Bookshop", "john_smith", 5, "Everything available."),
    ("Campus Bookshop", "alice_wanjiru", 3, "Limited parking."),
]

VISIT_PLAN_DATA = [
    # user, place, status
    ("jane_doe", "Student Gym", "Planned"),
    ("jane_doe", "Java House Campus Branch", "Visited"),
    ("john_smith", "Main Library", "Planned"),
    ("brian_kiptoo", "Sports Complex", "Visited"),
    ("kevin_otieno", "Gaming Hub", "Planned"),
    ("alice_wanjiru", "Campus Bookshop", "Planned"),
    ("grace_cherono", "Engineering Library", "Visited"),
    ("faith_njeri", "Campus Medical Centre", "Planned"),
    ("daniel_kamau", "Hall A Hostel", "Cancelled"),
    ("john_smith", "Student Lounge", "Planned"),
    ("brian_kiptoo", "Main Bus Stop", "Visited"),
    ("kevin_otieno", "Smart Print Centre", "Planned"),
    ("alice_wanjiru", "Digital Learning Centre", "Planned"),
    ("grace_cherono", "Java House Campus Branch", "Visited"),
    ("faith_njeri", "Mama Njeri Kitchen", "Planned"),
    ("daniel_kamau", "Fitness Hub", "Planned"),
    ("jane_doe", "Campus Grill", "Visited"),
    ("john_smith", "Sunrise Hostel", "Planned"),
    ("kevin_otieno", "Amphitheatre", "Planned"),
    ("alice_wanjiru", "Student Cafeteria", "Visited"),
]

BOOKMARK_DATA = [
    # user, place
    ("jane_doe", "Java House Campus Branch"),
    ("jane_doe", "Main Library"),
    ("jane_doe", "Student Gym"),
    ("john_smith", "Sports Complex"),
    ("john_smith", "Engineering Library"),
    ("john_smith", "Student Lounge"),
    ("brian_kiptoo", "Fitness Hub"),
    ("brian_kiptoo", "Campus Grill"),
    ("brian_kiptoo", "Hall A Hostel"),
    ("faith_njeri", "Campus Medical Centre"),
    ("faith_njeri", "Digital Learning Centre"),
    ("faith_njeri", "Campus Bookshop"),
    ("kevin_otieno", "Gaming Hub"),
    ("kevin_otieno", "Quick Copies"),
    ("kevin_otieno", "Main Bus Stop"),
    ("grace_cherono", "Student Cafeteria"),
    ("grace_cherono", "Amphitheatre"),
    ("grace_cherono", "Mama Njeri Kitchen"),
    ("daniel_kamau", "Hall B Hostel"),
    ("daniel_kamau", "North Gate Shuttle Stop"),
    ("daniel_kamau", "Java House Campus Branch"),
    ("daniel_kamau", "Student Lounge"),
]


def seed_data():
    app = create_app()

    with app.app_context():
        print("Clearing existing data...")
        clear_data()

        print("Seeding categories...")
        categories = {}
        for name, icon, description in CATEGORY_DATA:
            category = Category(name=name, icon=icon, description=description)
            db.session.add(category)
            categories[name] = category
        db.session.commit()

        print("Seeding users and profiles...")
        users = {}
        for username, email, password, role, bio, course, year in USER_DATA:
            user = User(username=username, email=email, password_hash=hash_password(password), role=role)
            db.session.add(user)
            db.session.flush()  # assigns user.id without committing yet
            db.session.add(Profile(user_id=user.id, bio=bio, course=course, year_of_study=year))
            users[username] = user
        db.session.commit()

        print("Seeding places...")
        admin = users["admin"]
        places = {}
        for name, category_name, submitted_by, status, description, address, hours in PLACE_DATA:
            place = Place(
                name=name,
                description=description,
                address=address,
                opening_hours=hours,
                category_id=categories[category_name].id,
                submitted_by=users[submitted_by].id,
                status=status,
                approved_by=admin.id if status in ("Approved", "Rejected") else None,
                approved_at=datetime.utcnow() if status in ("Approved", "Rejected") else None,
            )
            db.session.add(place)
            places[name] = place
        db.session.commit()

        print("Seeding reviews...")
        for place_name, reviewer, rating, comment in REVIEW_DATA:
            db.session.add(Review(
                user_id=users[reviewer].id,
                place_id=places[place_name].id,
                rating=rating,
                comment=comment,
            ))
        db.session.commit()

        print("Seeding visit plans...")
        for username, place_name, status in VISIT_PLAN_DATA:
            db.session.add(VisitPlan(
                user_id=users[username].id,
                place_id=places[place_name].id,
                status=status,
                planned_date=datetime.utcnow() + timedelta(days=3) if status == "Planned" else None,
                visited_at=datetime.utcnow() if status == "Visited" else None,
            ))
        db.session.commit()

        print("Seeding bookmarks...")
        for username, place_name in BOOKMARK_DATA:
            db.session.add(Bookmark(user_id=users[username].id, place_id=places[place_name].id))
        db.session.commit()

        print("Seeding complete.")


if __name__ == "__main__":
    seed_data()
