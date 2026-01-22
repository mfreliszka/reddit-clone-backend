import firebase_admin
from firebase_admin import credentials, firestore
from litestar import Litestar, get
from litestar.datastructures import State
from litestar.di import Provide

# 1. Logic to initialize Firebase
def init_firebase() -> firestore.firestore.Client:
    # On Google Cloud Run, it automatically finds the credentials
    # For local dev, you'd use credentials.Certificate("path/to/key.json")
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

# 2. Dependency: Provides the DB to your functions
async def provide_db(state: State) -> firestore.firestore.Client:
    return state.db

# 3. An example route using the database
@get("/posts")
async def get_posts(db: firestore.firestore.Client) -> list[dict]:
    # Standard Firestore query
    docs = db.collection("posts").order_by("created_at", direction="DESCENDING").limit(20).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

# 4. App configuration with Lifecycles
async def on_startup(app: Litestar) -> None:
    app.state.db = init_firebase()

app = Litestar(
    route_handlers=[get_posts],
    dependencies={"db": Provide(provide_db)}, # Injects 'db' into any route that asks for it
    on_startup=[on_startup],
    debug=True,
)