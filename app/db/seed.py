import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.accommodation import Accommodation, TargetAudience
from app.models.food_service import FoodService, FoodServiceType, BudgetType
from app.models.fast_food_spot import FastFoodSpot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_db(db: AsyncSession) -> None:
    # 1. Seed Accommodations
    accommodation_check = await db.execute(select(Accommodation).limit(1))
    if not accommodation_check.scalars().first():
        logger.info("Seeding accommodations...")
        accommodations = [
            Accommodation(
                name="Stayvillas",
                area="Sector-A Shastri Nagar",
                address="A-80, Near Vishvakarma School, Sector-A, Shastri Nagar, Jodhpur, Rajasthan",
                contact_number="+91 96200 12388",
                target_audience=TargetAudience.CO_ED,
                features=["Premium villa-style", "High-speed Wi-Fi", "Housekeeping"],
                distance_from_college_km=0.4,
                latitude=26.2785,
                longitude=73.0185,
            ),
            Accommodation(
                name="Thanvi Kuteer",
                area="Sector-G Shastri Nagar",
                address="G-193, Behind Hanwant School, Shastri Nagar, Jodhpur, Rajasthan",
                contact_number="+91 94142 93883",
                target_audience=TargetAudience.CO_ED,
                features=["Peaceful area", "Garden", "Home-like environment"],
                distance_from_college_km=1.2,
                latitude=26.2721,
                longitude=73.0112,
            ),
            Accommodation(
                name="Royal Home Boys Hostel",
                area="Kalpatru Shopping Centre",
                address="E-49, Kalpataru Shopping Centre, Near CLG Coaching, Shastri Nagar, Jodhpur, Rajasthan - 342003",
                contact_number="+91 87694 44728",
                target_audience=TargetAudience.BOYS,
                features=["Near coaching hub", "Air conditioned", "Gym facility"],
                distance_from_college_km=1.0,
                latitude=26.2810,
                longitude=73.0234,
            ),
            Accommodation(
                name="Shree Gajanand P.G & Hostel",
                area="Pratap Nagar",
                address="Plot No. 107, Near Umraao Khan Petrol Pump Lane, Bombay Motor Circle, Pratap Nagar, Jodhpur, Rajasthan - 342003",
                contact_number="+91 99166 11442",
                target_audience=TargetAudience.CO_ED,
                features=["24/7 open", "Separate wings for boys & girls", "CCTV Security"],
                distance_from_college_km=2.0,
                latitude=26.2905,
                longitude=73.0345,
            ),
            Accommodation(
                name="KeshavKunj Hostel",
                area="Kamla Nehru Nagar",
                address="D-98, Areej Tower, Near JK Medical, Kamla Nehru Nagar, Jodhpur, Rajasthan",
                contact_number="+91 96609 50063",
                target_audience=TargetAudience.CO_ED,
                features=["Student friendly hub", "Common study hall", "Rooftop access"],
                distance_from_college_km=1.5,
                latitude=26.2654,
                longitude=73.0021,
            ),
            Accommodation(
                name="Balaji Boys Hostel & PG",
                area="Sardarpura",
                address="Plot No. 707, 8 C Road, Manohar Bhawan, 4th A Rd, Sardarpura, Jodhpur, Rajasthan - 342003",
                contact_number="+91 94609 81447",
                target_audience=TargetAudience.BOYS,
                features=["Mess facility", "Daily laundry", "Power backup"],
                distance_from_college_km=1.5,
                latitude=26.2856,
                longitude=73.0210,
            ),
        ]
        db.add_all(accommodations)
        await db.commit()
        logger.info("Successfully seeded accommodations.")
    else:
        logger.info("Accommodations already seeded.")

    # 2. Seed Food Services
    food_service_check = await db.execute(select(FoodService).limit(1))
    if not food_service_check.scalars().first():
        logger.info("Seeding food services...")
        food_services = [
            FoodService(
                name="Meals By Muskan",
                type=FoodServiceType.TIFFIN,
                area="Ratanada",
                address="Ratanada Circle, Ratanada, Jodhpur, Rajasthan",
                contact_number="Justdial Listed",
                timings="24 Hours",
                budget_type=BudgetType.BUDGET,
                usp="Hygienic home food",
            ),
            FoodService(
                name="S.S. Tiffin Service",
                type=FoodServiceType.TIFFIN,
                area="P.W.D Colony",
                address="P.W.D Colony, Ratanada, Jodhpur, Rajasthan",
                contact_number="+91 95216 42290",
                timings="Standard meal times",
                budget_type=BudgetType.BUDGET,
                usp="North Indian meals",
            ),
            FoodService(
                name="Vinay Tiffin Service",
                type=FoodServiceType.TIFFIN,
                area="Kamla Nehru Nagar",
                address="Behind Kamla Nagar Hospital, Kamla Nehru Nagar, Shyam Nagar, Jodhpur, Rajasthan",
                contact_number="Justdial Listed",
                timings="06:00 AM - 11:30 PM",
                budget_type=BudgetType.BUDGET,
                usp="Monthly student subscription",
            ),
            FoodService(
                name="Vicky Da Dhaba",
                type=FoodServiceType.DHABA,
                area="Chopasni Housing Board",
                address="Chopasni Housing Board, Jodhpur, Rajasthan",
                contact_number="Walk-in Only",
                timings="Lunch & Dinner",
                budget_type=BudgetType.BUDGET,
                usp="Heavy Punjabi/Desi meals",
            ),
            FoodService(
                name="Laxmi Bhojnalaya",
                type=FoodServiceType.BHOJNALAYA,
                area="Basni",
                address="Basni Phase 2, Jodhpur, Rajasthan",
                contact_number="Walk-in Only",
                timings="Lunch & Dinner",
                budget_type=BudgetType.BUDGET,
                usp="Traditional Rajasthani Thalis",
            ),
        ]
        db.add_all(food_services)
        await db.commit()
        logger.info("Successfully seeded food services.")
    else:
        logger.info("Food services already seeded.")

    # 3. Seed Fast Food Spots
    fast_food_check = await db.execute(select(FastFoodSpot).limit(1))
    if not fast_food_check.scalars().first():
        logger.info("Seeding fast food spots...")
        fast_food_spots = [
            FastFoodSpot(
                name="21st Fast Food",
                area="Shastri Nagar",
                address="Near Shastri Nagar Circle, Shastri Nagar, Jodhpur, Rajasthan",
                contact_number="+91 291 263 2121",
                specialties=["Veg Burger", "Paneer Sandwich", "Tandoori Maggi"],
                average_cost_for_two=200,
                top_items={"Veg Burger": 65.0, "Paneer Sandwich": 95.0, "Tandoori Maggi": 79.0}
            ),
            FastFoodSpot(
                name="Hariom Fastfood",
                area="Jaljog Choraha",
                address="Jaljog Choraha, Sardarpura, Jodhpur, Rajasthan",
                contact_number="Walk-in Only",
                specialties=["Vada Pav", "Cold Coffee"],
                average_cost_for_two=200,
                top_items={"Vada Pav": 50.0, "Cold Coffee": 70.0}
            ),
            FastFoodSpot(
                name="Janta Sweet Home",
                area="Jaljog",
                address="Jaljog Crossing, Shastri Nagar Road, Jodhpur, Rajasthan",
                contact_number="+91 291 243 6118",
                specialties=["Pyaz Kachori", "Masala Dosa", "Burgers"],
                average_cost_for_two=300,
                top_items={"Pyaz Kachori": 45.0, "Masala Dosa": 110.0, "Burgers": 75.0}
            )
        ]
        db.add_all(fast_food_spots)
        await db.commit()
        logger.info("Successfully seeded fast food spots.")
    else:
        logger.info("Fast food spots already seeded.")
