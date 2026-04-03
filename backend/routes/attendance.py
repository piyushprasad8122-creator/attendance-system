from fastapi import APIRouter, HTTPException, Depends
from database import attendance_collection, users_collection
from utils.auth import get_current_user
from datetime import datetime, date
from bson import ObjectId

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/checkin")
async def check_in(current_user: dict = Depends(get_current_user)):
    today = date.today().isoformat()
    user_id = current_user["user_id"]

    # Check if already checked in today
    existing = await attendance_collection.find_one({
        "user_id": user_id,
        "date": today
    })

    if existing and existing.get("check_in"):
        raise HTTPException(
            status_code=400,
            detail="Already checked in today"
        )

    now = datetime.utcnow()

    # Determine if late (after 9:30 AM)
    status = "present"
    if now.hour > 9 or (now.hour == 9 and now.minute > 30):
        status = "late"

    if existing:
        await attendance_collection.update_one(
            {"user_id": user_id, "date": today},
            {"$set": {"check_in": now, "status": status}}
        )
    else:
        await attendance_collection.insert_one({
            "user_id": user_id,
            "full_name": current_user["full_name"],
            "date": today,
            "check_in": now,
            "check_out": None,
            "status": status,
            "verified_by_face": False
        })

    return {
        "message": "Check-in successful",
        "time": now.isoformat(),
        "status": status
    }

@router.post("/checkout")
async def check_out(current_user: dict = Depends(get_current_user)):
    today = date.today().isoformat()
    user_id = current_user["user_id"]

    existing = await attendance_collection.find_one({
        "user_id": user_id,
        "date": today
    })

    if not existing or not existing.get("check_in"):
        raise HTTPException(status_code=400, detail="You haven't checked in today")

    if existing.get("check_out"):
        raise HTTPException(status_code=400, detail="Already checked out today")

    now = datetime.utcnow()
    await attendance_collection.update_one(
        {"user_id": user_id, "date": today},
        {"$set": {"check_out": now}}
    )

    # Calculate hours worked
    check_in_time = existing["check_in"]
    hours = round((now - check_in_time).seconds / 3600, 2)

    return {
        "message": "Check-out successful",
        "time": now.isoformat(),
        "hours_worked": hours
    }

@router.get("/today")
async def get_today(current_user: dict = Depends(get_current_user)):
    today = date.today().isoformat()
    record = await attendance_collection.find_one({
        "user_id": current_user["user_id"],
        "date": today
    })

    if not record:
        return {"checked_in": False, "checked_out": False, "date": today}

    return {
        "checked_in": bool(record.get("check_in")),
        "checked_out": bool(record.get("check_out")),
        "check_in": record.get("check_in"),
        "check_out": record.get("check_out"),
        "status": record.get("status"),
        "date": today
    }

@router.get("/my-history")
async def my_history(current_user: dict = Depends(get_current_user)):
    cursor = attendance_collection.find(
        {"user_id": current_user["user_id"]}
    ).sort("date", -1).limit(30)

    records = []
    async for record in cursor:
        records.append({
            "date": record["date"],
            "check_in": record.get("check_in"),
            "check_out": record.get("check_out"),
            "status": record.get("status", "present"),
            "verified_by_face": record.get("verified_by_face", False)
        })

    return records
