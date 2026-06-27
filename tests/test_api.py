import pytest
import asyncio
import pytest_asyncio
from typing import AsyncGenerator
from uuid import UUID
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import get_db
from app.db.base_class import Base
from app.db.seed import seed_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Override get_db dependency for tests to run on the temporary database
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Automatically create all tables and run seed data before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as db:
        await seed_db(db)
        
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an HTTPX AsyncClient bound to the app using ASGI transport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Welcome" in data["message"]
    assert data["docs"] == "/docs"

@pytest.mark.asyncio
async def test_seed_accommodations(client: AsyncClient):
    response = await client.get("/api/v1/accommodations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    names = [acc["name"] for acc in data]
    assert "Stayvillas" in names
    assert "Thanvi Kuteer" in names
    assert "Balaji Boys Hostel & PG" in names

@pytest.mark.asyncio
async def test_filter_accommodations_audience(client: AsyncClient):
    # Filter for Boys
    response = await client.get("/api/v1/accommodations/?target_audience=Boys")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for acc in data:
        assert acc["target_audience"] == "Boys"

    # Filter for Co-ed
    response = await client.get("/api/v1/accommodations/?target_audience=Co-ed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    for acc in data:
        assert acc["target_audience"] == "Co-ed"

@pytest.mark.asyncio
async def test_filter_accommodations_distance(client: AsyncClient):
    response = await client.get("/api/v1/accommodations/?max_distance_km=1.0")
    assert response.status_code == 200
    data = response.json()
    # Stayvillas (0.4km), Royal Home Boys Hostel (1.0km) should match
    assert len(data) == 2
    for acc in data:
        assert acc["distance_from_college_km"] <= 1.0

@pytest.mark.asyncio
async def test_filter_accommodations_area(client: AsyncClient):
    # Shastri Nagar substring match
    response = await client.get("/api/v1/accommodations/?area=Shastri Nagar")
    assert response.status_code == 200
    data = response.json()
    # Stayvillas (Sector-A Shastri Nagar), Thanvi Kuteer (Sector-G Shastri Nagar) should match
    assert len(data) == 2
    for acc in data:
        assert "Shastri Nagar" in acc["area"]

    # Sector-A substring match
    response = await client.get("/api/v1/accommodations/?area=Sector-A")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Stayvillas"

@pytest.mark.asyncio
async def test_crud_accommodation(client: AsyncClient):
    # 1. Create a new accommodation
    new_acc = {
        "name": "Arjun PG",
        "area": "Sardarpura",
        "address": "Manohar Bhawan, Sardarpura, Jodhpur",
        "contact_number": "+91 99999 88888",
        "target_audience": "Boys",
        "features": ["AC", "Single Room"],
        "distance_from_college_km": 0.8,
        "latitude": 26.2800,
        "longitude": 73.0200
    }
    response = await client.post("/api/v1/accommodations/", json=new_acc)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Arjun PG"
    assert created["features"] == ["AC", "Single Room"]
    assert created["distance_from_college_km"] == 0.8
    acc_id = created["id"]

    # 2. Read the created record
    response = await client.get(f"/api/v1/accommodations/{acc_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Arjun PG"

    # 3. Update the record
    updated_data = {"name": "Arjun Premium PG", "distance_from_college_km": 0.9}
    response = await client.put(f"/api/v1/accommodations/{acc_id}", json=updated_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Arjun Premium PG"
    assert updated["distance_from_college_km"] == 0.9
    assert updated["features"] == ["AC", "Single Room"]  # Untouched feature list should remain

    # 4. Delete the record
    response = await client.delete(f"/api/v1/accommodations/{acc_id}")
    assert response.status_code == 200
    
    # 5. Read again, should return 404
    response = await client.get(f"/api/v1/accommodations/{acc_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_seed_food_services(client: AsyncClient):
    response = await client.get("/api/v1/food-services/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    names = [fs["name"] for fs in data]
    assert "Meals By Muskan" in names
    assert "Vicky Da Dhaba" in names

@pytest.mark.asyncio
async def test_filter_food_services_type(client: AsyncClient):
    # Filter for Tiffin
    response = await client.get("/api/v1/food-services/?type=Tiffin")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for fs in data:
        assert fs["type"] == "Tiffin"

    # Filter for Dhaba
    response = await client.get("/api/v1/food-services/?type=Dhaba")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Vicky Da Dhaba"

@pytest.mark.asyncio
async def test_filter_food_services_area(client: AsyncClient):
    # Filter for Kamla Nehru Nagar
    response = await client.get("/api/v1/food-services/?area=Kamla Nehru Nagar")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Vinay Tiffin Service"

    # Case-insensitive substring match: "ratan" matches "Ratanada"
    response = await client.get("/api/v1/food-services/?area=ratan")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Meals By Muskan"

@pytest.mark.asyncio
async def test_crud_food_service(client: AsyncClient):
    # 1. Create a food service
    new_fs = {
        "name": "Jodhpur Sweets & Restaurant",
        "type": "Bhojnalaya",
        "area": "Sardarpura",
        "address": "C Road, Sardarpura, Jodhpur",
        "contact_number": "+91 99999 77777",
        "timings": "09:00 AM - 10:00 PM",
        "budget_type": "Mid-range",
        "usp": "Delicious sweets and thali"
    }
    response = await client.post("/api/v1/food-services/", json=new_fs)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Jodhpur Sweets & Restaurant"
    assert created["type"] == "Bhojnalaya"
    fs_id = created["id"]

    # 2. Read the record
    response = await client.get(f"/api/v1/food-services/{fs_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jodhpur Sweets & Restaurant"

    # 3. Update the record
    updated_data = {"name": "Jodhpur Sweets & Bhojnalaya", "timings": "08:00 AM - 11:00 PM"}
    response = await client.put(f"/api/v1/food-services/{fs_id}", json=updated_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Jodhpur Sweets & Bhojnalaya"
    assert updated["timings"] == "08:00 AM - 11:00 PM"
    assert updated["usp"] == "Delicious sweets and thali"  # Untouched field should remain

    # 4. Delete the record
    response = await client.delete(f"/api/v1/food-services/{fs_id}")
    assert response.status_code == 200
    
    # 5. Read again, should return 404
    response = await client.get(f"/api/v1/food-services/{fs_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_seed_fast_food_spots(client: AsyncClient):
    response = await client.get("/api/v1/fast-food-spots/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    names = [spot["name"] for spot in data]
    assert "21st Fast Food" in names
    assert "Hariom Fastfood" in names
    assert "Janta Sweet Home" in names

@pytest.mark.asyncio
async def test_filter_fast_food_spots_area(client: AsyncClient):
    # Filter by area "Jaljog"
    response = await client.get("/api/v1/fast-food-spots/?area=Jaljog")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for spot in data:
        assert "Jaljog" in spot["area"]

@pytest.mark.asyncio
async def test_filter_fast_food_spots_cost(client: AsyncClient):
    # Filter by cost <= 200
    response = await client.get("/api/v1/fast-food-spots/?max_cost_for_two=200")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for spot in data:
        assert spot["average_cost_for_two"] <= 200

@pytest.mark.asyncio
async def test_crud_fast_food_spot(client: AsyncClient):
    # 1. Create a fast food spot
    new_spot = {
        "name": "Arjun Burger Joint",
        "area": "Shastri Nagar",
        "address": "Sector-A Shastri Nagar, Jodhpur",
        "contact_number": "+91 99999 66666",
        "specialties": ["Burgers", "Fries"],
        "average_cost_for_two": 150,
        "top_items": {"Double Cheese Burger": 80.0, "French Fries": 50.0}
    }
    response = await client.post("/api/v1/fast-food-spots/", json=new_spot)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Arjun Burger Joint"
    assert created["top_items"]["Double Cheese Burger"] == 80.0
    spot_id = created["id"]

    # 2. Read the record
    response = await client.get(f"/api/v1/fast-food-spots/{spot_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Arjun Burger Joint"

    # 3. Update the record
    updated_data = {"name": "Arjun Premium Burger Joint", "average_cost_for_two": 180}
    response = await client.put(f"/api/v1/fast-food-spots/{spot_id}", json=updated_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Arjun Premium Burger Joint"
    assert updated["average_cost_for_two"] == 180
    assert updated["specialties"] == ["Burgers", "Fries"]  # Untouched

    # 4. Delete the record
    response = await client.delete(f"/api/v1/fast-food-spots/{spot_id}")
    assert response.status_code == 200
    
    # 5. Read again, should return 404
    response = await client.get(f"/api/v1/fast-food-spots/{spot_id}")
    assert response.status_code == 404
