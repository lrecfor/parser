from fastapi import FastAPI
import uvicorn
import schedule
import updater
from database import Database

app = FastAPI()
db = Database()


@app.get("/")
async def root():
    return {"Print /{new_id} to read news"}


@app.get("/{new_id}")
async def output_news(new_id: int):
    return db.get(new_id)


if __name__ == "__main__":
    updater.update_database()

    uvicorn.run(
                "app:app",
                host='localhost',
                port=8080,
                reload=True
            )

    schedule.every().hour.do(updater.update_database)
    while True:
        schedule.run_pending()
