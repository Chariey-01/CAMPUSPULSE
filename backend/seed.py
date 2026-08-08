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


def _unsplash(photo_id, width=1600, quality=65):
    # Every id below was downloaded and visually checked before being used
    # here - see frontend/src/lib/categoryPhotos.js for the same practice on
    # the frontend side. Category hero images are wide (1600px); place
    # images are requested smaller (800px) since they render in a card, not
    # a full-width banner - see PLACE_DATA below.
    return f"https://images.unsplash.com/photo-{photo_id}?w={width}&q={quality}&fit=crop&auto=format"


CATEGORY_DATA = [
    # name, icon, description, hero_image
    ("Cafeteria", "utensils", "Places to eat on campus", _unsplash("1414235077428-338989a2e8c0")),
    ("Library", "book", "Study and reading spaces", _unsplash("1507842217343-583bb7270b66")),
    ("Gym", "dumbbell", "Fitness and sports facilities", _unsplash("1534438327276-14e5300c3a48")),
    ("Hostel", "home", "Student accommodation", _unsplash("1595526114035-0d45ed16cfbf")),
    ("Clinic", "heart-pulse", "Health and medical services", _unsplash("1519494026892-80bbd2d6fd0d")),
    ("Stationery", "pencil", "Books, printing, and supplies", _unsplash("1543002588-bfa74002ed7e")),
    ("Transport", "bus", "Campus transport stops", _unsplash("1570125909232-eb263c188f7e")),
    ("Entertainment", "music", "Relaxation and leisure spots", _unsplash("1531482615713-2afd69097998")),
    # Wayfinding categories - these hold individual buildings/offices as places
    # rather than getting a category per department/office (e.g. "Computer
    # Science" and "Engineering" are places inside Academic Buildings, not
    # categories of their own) - keeps the category list itself manageable.
    ("Academic Buildings", "graduation-cap", "Lecture halls, labs, and faculty buildings", _unsplash("1562774053-701939374585")),
    ("Administration", "briefcase", "Offices for admissions, finance, and student records", _unsplash("1592280771190-3e2e4d571952")),
    ("Utilities", "wrench", "Washrooms, water points, ATMs, and everyday essentials", _unsplash("1517646287270-a5a9ca602e5c")),
    ("Safety & Security", "shield", "Security offices and emergency points on campus", _unsplash("1582139329536-e7284fece509")),
    ("Student Life", "users", "Clubs, student government, and community spaces", _unsplash("1523240795612-9a054b0db644")),
    ("Religious", "church", "Chapels, mosques, and quiet spaces for reflection", _unsplash("1548625149-fc4a29cf7092")),
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

# Place-level photos are deliberately different shots from their category's
# hero_image above - the whole point of this split is that a place shows its
# own identity (ideally its real photo/logo, one day uploaded by an admin or
# owner), not a repeat of the generic category image.
_CAFE_A, _CAFE_B = _unsplash("1517248135467-4c7edcad34c4", 800, 70), _unsplash("1554118811-1e0d58224f24", 800, 70)
_LIB_A, _LIB_B = _unsplash("1521587760476-6c12a4b040da", 800, 70), _unsplash("1495446815901-a7297e633e8d", 800, 70)
_GYM_A, _GYM_B = _unsplash("1571019613454-1cb2f99b2d8b", 800, 70), _unsplash("1517836357463-d25dfeac3438", 800, 70)
_HOST_A, _HOST_B = _unsplash("1631049307264-da0ec9d70304", 800, 70), _unsplash("1522771739844-6a9f6d5f14af", 800, 70)
_CLINIC_A, _CLINIC_B = _unsplash("1516549655169-df83a0774514", 800, 70), _unsplash("1666214280391-8ff5bd3c0bf0", 800, 70)
_STAT_A, _STAT_B = _unsplash("1517842645767-c639042777db", 800, 70), _unsplash("1587614382346-4ec70e388b28", 800, 70)
_TRANS_A, _TRANS_B = _unsplash("1449824913935-59a10b8d2000", 800, 70), _unsplash("1449965408869-eaa3f722e40d", 800, 70)
_ENT_A, _ENT_B = _unsplash("1470229722913-7c0e2dbbafd3", 800, 70), _unsplash("1514525253161-7a46d19cd819", 800, 70)
_ACAD_A, _ACAD_B = _unsplash("1571260899304-425eee4c7efc", 800, 70), _unsplash("1524178232363-1fb2b075b655", 800, 70)
_ADMIN_A, _ADMIN_B = _unsplash("1554224155-6726b3ff858f", 800, 70), _unsplash("1568992688065-536aad8a12f6", 800, 70)
_MOSQUE = _unsplash("1585036156171-384164a8c675", 800, 70)
_STUDENTLIFE = _unsplash("1541178735493-479c1a27ed24", 800, 70)
_PARKING = _unsplash("1465447142348-e9952c393450", 800, 70)
# Utilities and Safety & Security places intentionally have no image_url below -
# no verified photo distinct enough from their category hero was found for these
# (e.g. an ATM or a washroom), so they fall back to PlaceImage's category-tinted
# icon tile instead of forcing a mismatched stock photo.

PLACE_DATA = [
    # name, category, submitted_by, status, description, address, opening_hours, image_url
    ("Java House Campus Branch", "Cafeteria", "jane_doe", "Approved", "Popular coffee shop near the main gate", "Main Gate, Block A", "7:00 AM - 9:00 PM", _CAFE_A),
    ("Student Cafeteria", "Cafeteria", "john_smith", "Approved", "The main dining hall for students", "Central Block", "6:30 AM - 9:00 PM", _CAFE_B),
    ("Mama Njeri Kitchen", "Cafeteria", "alice_wanjiru", "Approved", "Home-style meals at student prices", "Behind Hall B", "8:00 AM - 8:00 PM", _CAFE_A),
    ("Campus Grill", "Cafeteria", "brian_kiptoo", "Approved", "Grilled snacks and fast food", "Sports Complex Road", "10:00 AM - 10:00 PM", _CAFE_B),
    ("Old Cafeteria Extension", "Cafeteria", "kevin_otieno", "Rejected", "Proposed extension to the old cafeteria", "East Wing", "N/A", _CAFE_A),
    ("Main Library", "Library", "faith_njeri", "Approved", "Central campus library with silent study rooms", "Academic Block C", "8:00 AM - 10:00 PM", _LIB_A),
    ("Engineering Library", "Library", "brian_kiptoo", "Approved", "Technical resources for engineering students", "Engineering Block", "8:00 AM - 9:00 PM", _LIB_B),
    ("Digital Learning Centre", "Library", "alice_wanjiru", "Approved", "Computers and online resources", "Academic Block D", "8:00 AM - 8:00 PM", _LIB_A),
    ("Student Gym", "Gym", "jane_doe", "Approved", "Campus fitness center", "Sports Complex", "6:00 AM - 8:00 PM", _GYM_A),
    ("Sports Complex", "Gym", "brian_kiptoo", "Approved", "Football and basketball facilities", "South Campus", "6:00 AM - 9:00 PM", _GYM_B),
    ("Fitness Hub", "Gym", "kevin_otieno", "Approved", "Modern gym equipment and personal training", "Hall A Basement", "6:00 AM - 10:00 PM", _GYM_A),
    ("Hall A Hostel", "Hostel", "daniel_kamau", "Approved", "First-year student accommodation", "North Campus", "24 hours", _HOST_A),
    ("Hall B Hostel", "Hostel", "grace_cherono", "Approved", "Mixed accommodation block", "North Campus", "24 hours", _HOST_B),
    ("Sunrise Hostel", "Hostel", "faith_njeri", "Pending", "Off-campus student housing", "East Gate", "24 hours", _HOST_A),
    ("Campus Medical Centre", "Clinic", "john_smith", "Approved", "Primary healthcare for students", "Admin Block", "8:00 AM - 6:00 PM", _CLINIC_A),
    ("Student Wellness Clinic", "Clinic", "grace_cherono", "Approved", "Counseling and wellness services", "Student Centre", "9:00 AM - 5:00 PM", _CLINIC_B),
    ("Campus Bookshop", "Stationery", "daniel_kamau", "Approved", "Textbooks and supplies", "Main Gate", "8:00 AM - 6:00 PM", _STAT_A),
    ("Smart Print Centre", "Stationery", "kevin_otieno", "Approved", "Printing and photocopying", "Library Annex", "8:00 AM - 8:00 PM", _STAT_B),
    ("Quick Copies", "Stationery", "alice_wanjiru", "Approved", "Fast, affordable printing", "Student Centre", "8:00 AM - 7:00 PM", _STAT_A),
    ("Main Bus Stop", "Transport", "john_smith", "Approved", "Main campus shuttle and bus stop", "Main Gate", "5:30 AM - 10:00 PM", _TRANS_A),
    ("North Gate Shuttle Stop", "Transport", "jane_doe", "Approved", "Shuttle stop for North Campus residents", "North Gate", "6:00 AM - 9:00 PM", _TRANS_B),
    ("Student Lounge", "Entertainment", "grace_cherono", "Pending", "Relaxation space with sofas and Wi-Fi", "Student Centre", "9:00 AM - 11:00 PM", _ENT_A),
    ("Amphitheatre", "Entertainment", "daniel_kamau", "Approved", "Open-air venue for events", "Central Campus", "Open access", _ENT_B),
    ("Gaming Hub", "Entertainment", "kevin_otieno", "Pending", "Console and PC gaming lounge", "Student Centre", "10:00 AM - 10:00 PM", _ENT_A),

    ("Main Gate", "Transport", "john_smith", "Approved", "Primary vehicle and pedestrian entrance to campus", "Perimeter Road", "24 hours", None),
    ("Visitor Parking", "Transport", "grace_cherono", "Approved", "Parking area for visitors and staff", "Near Main Gate", "6:00 AM - 10:00 PM", _PARKING),

    ("Engineering Complex", "Academic Buildings", "brian_kiptoo", "Approved", "Labs and lecture halls for engineering students", "North Academic Precinct", "7:00 AM - 9:00 PM", _ACAD_A),
    ("Science Complex", "Academic Buildings", "faith_njeri", "Approved", "Physics, chemistry, and biology laboratories", "North Academic Precinct", "7:00 AM - 9:00 PM", _ACAD_B),
    ("Business School", "Academic Buildings", "alice_wanjiru", "Approved", "Home of the school of business and economics", "South Academic Precinct", "7:00 AM - 8:00 PM", _ACAD_A),
    ("Computing & ICT Building", "Academic Buildings", "kevin_otieno", "Approved", "Computer labs and the ICT department", "South Academic Precinct", "7:00 AM - 10:00 PM", _ACAD_B),

    ("Administration Block", "Administration", "daniel_kamau", "Approved", "Main administrative offices", "Central Campus", "8:00 AM - 5:00 PM", _ADMIN_A),
    ("Registrar's Office", "Administration", "jane_doe", "Approved", "Student records, transcripts, and enrollment", "Administration Block, Ground Floor", "8:00 AM - 4:30 PM", _ADMIN_B),
    ("Finance Office", "Administration", "john_smith", "Approved", "Fee payments and financial queries", "Administration Block, 1st Floor", "8:30 AM - 4:00 PM", _ADMIN_A),
    ("Admissions Office", "Administration", "grace_cherono", "Pending", "New student admissions and inquiries", "Administration Block, Ground Floor", "8:00 AM - 4:30 PM", _ADMIN_B),

    ("Central Washrooms", "Utilities", "brian_kiptoo", "Approved", "Public restrooms near the main square", "Main Square", "24 hours", None),
    ("Library Water Point", "Utilities", "faith_njeri", "Approved", "Free drinking water dispenser", "Main Library, Ground Floor", "8:00 AM - 10:00 PM", None),
    ("Campus ATM", "Utilities", "alice_wanjiru", "Approved", "24-hour cash withdrawal point", "Student Centre", "24 hours", None),
    ("Lost & Found Office", "Utilities", "kevin_otieno", "Pending", "Report or collect lost items", "Main Security Office", "9:00 AM - 5:00 PM", None),

    ("Main Security Office", "Safety & Security", "daniel_kamau", "Approved", "Campus security and visitor sign-in", "Main Gate", "24 hours", None),
    ("Emergency Assembly Point", "Safety & Security", "jane_doe", "Approved", "Designated gathering point during evacuations", "Central Quad", "Always accessible", None),
    ("CCTV Control Room", "Safety & Security", "john_smith", "Rejected", "Campus surveillance monitoring", "Main Security Office", "N/A", None),

    ("Student Centre", "Student Life", "grace_cherono", "Approved", "Hub for student activities and events", "Central Campus", "7:00 AM - 11:00 PM", None),
    ("Clubs & Societies Office", "Student Life", "kevin_otieno", "Approved", "Register and manage student clubs", "Student Centre, 2nd Floor", "9:00 AM - 5:00 PM", _STUDENTLIFE),
    ("Student Union Office", "Student Life", "brian_kiptoo", "Approved", "Elected student government offices", "Student Centre, 2nd Floor", "9:00 AM - 5:00 PM", None),
    ("Counseling Centre", "Student Life", "faith_njeri", "Pending", "Confidential student counseling services", "Student Centre, 3rd Floor", "9:00 AM - 4:00 PM", None),

    ("Campus Chapel", "Religious", "alice_wanjiru", "Approved", "Christian chapel open for services and quiet prayer", "East Campus", "6:00 AM - 9:00 PM", None),
    ("Campus Mosque", "Religious", "daniel_kamau", "Approved", "Prayer space and ablution facilities", "East Campus", "5:00 AM - 10:00 PM", _MOSQUE),
    ("Interfaith Prayer Room", "Religious", "jane_doe", "Pending", "Quiet multi-faith prayer and reflection room", "Student Centre, 3rd Floor", "24 hours", None),
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

    ("Engineering Complex", "kevin_otieno", 5, "Great labs and fast wifi."),
    ("Engineering Complex", "faith_njeri", 4, "Clean and well maintained."),
    ("Engineering Complex", "grace_cherono", 4, "Can get crowded before exams."),

    ("Administration Block", "jane_doe", 3, "Lines can be long during registration week."),
    ("Administration Block", "brian_kiptoo", 4, "Staff were helpful once I got to the counter."),
    ("Administration Block", "alice_wanjiru", 5, "Sorted my transcript request in one visit."),

    ("Student Centre", "daniel_kamau", 5, "Great place to hang out between classes."),
    ("Student Centre", "kevin_otieno", 5, "Love the events they host here."),
    ("Student Centre", "john_smith", 4, "Could use more seating during lunch hour."),
    ("Student Centre", "faith_njeri", 4, "Good wifi and charging points."),

    ("Campus Chapel", "alice_wanjiru", 5, "Peaceful place, love the Sunday service."),
    ("Campus Chapel", "grace_cherono", 5, "Beautiful and quiet."),
    ("Campus Chapel", "daniel_kamau", 4, "Nice space for reflection between classes."),

    ("Campus Mosque", "daniel_kamau", 5, "Well maintained ablution area."),
    ("Campus Mosque", "jane_doe", 5, "Quiet and peaceful, great for Jummah."),
    ("Campus Mosque", "john_smith", 4, "Good facilities."),

    ("Central Washrooms", "brian_kiptoo", 3, "Usually clean but can run out of supplies."),
    ("Central Washrooms", "kevin_otieno", 4, "Convenient location near the main square."),
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

    ("jane_doe", "Registrar's Office", "Planned"),
    ("john_smith", "Student Centre", "Visited"),
    ("alice_wanjiru", "Finance Office", "Planned"),
    ("brian_kiptoo", "Campus Chapel", "Visited"),
    ("faith_njeri", "Admissions Office", "Planned"),
    ("kevin_otieno", "Engineering Complex", "Visited"),
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

    ("jane_doe", "Student Centre"),
    ("john_smith", "Administration Block"),
    ("alice_wanjiru", "Campus Chapel"),
    ("brian_kiptoo", "Engineering Complex"),
    ("faith_njeri", "Campus Mosque"),
    ("kevin_otieno", "Clubs & Societies Office"),
    ("grace_cherono", "Central Washrooms"),
    ("daniel_kamau", "Main Gate"),
]


def seed_data():
    app = create_app()

    with app.app_context():
        print("Clearing existing data...")
        clear_data()

        print("Seeding categories...")
        categories = {}
        for name, icon, description, hero_image in CATEGORY_DATA:
            category = Category(name=name, icon=icon, description=description, hero_image=hero_image)
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
        for name, category_name, submitted_by, status, description, address, hours, image_url in PLACE_DATA:
            place = Place(
                name=name,
                description=description,
                address=address,
                opening_hours=hours,
                image_url=image_url,
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
