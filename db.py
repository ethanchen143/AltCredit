import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.credit_app_db
applications_collection = db.applications