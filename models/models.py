from sqlalchemy import MetaData, Column, Table, Integer, String, Boolean, Float, Date

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(length=320), unique=True, nullable=False),
    Column("email", String(length=320), unique=True, nullable=False),
    Column("csvfile", String(length=1024), unique=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

booking = Table(
    "booking",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("booking_date", Date),
    Column("length_of_stay", Integer),
    Column("guest_name", String(length=1024)),
    Column("daily_rate", Float)
)