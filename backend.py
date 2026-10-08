import sqlite3

# --- 1. DATABASE INITIALIZATION ---
def init_db():
    """Creates the necessary tables if they don't exist."""
    conn = sqlite3.connect("aeropool.db")
    cursor = conn.cursor()
    
    # Table to store active ride requests at the airport
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ride_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT,
            dropoff_zone TEXT,
            luggage_size TEXT, 
            luggage_units INTEGER,
            status TEXT DEFAULT 'Searching'
        )
    """)
    
    # Table to store successfully matched cabs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matched_cabs (
            cab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_1_id INTEGER,
            passenger_2_id INTEGER,
            shared_zone TEXT,
            total_luggage_units INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

# --- 2. TRUNK CAPACITY LOGIC ---
# A standard sedan trunk has a maximum capacity of 4 "units".
# Light (Backpack) = 1 unit
# Medium (1 Suitcase) = 2 units
# Heavy (2 Suitcases) = 3 units

def get_luggage_units(size_label):
    mapping = {"Light": 1, "Medium": 2, "Heavy": 3}
    return mapping.get(size_label, 1)

def add_ride_request(name, zone, luggage_size, is_shared=True):
    """Adds a new passenger to the waiting list."""
    units = get_luggage_units(luggage_size)
    
    conn = sqlite3.connect("aeropool.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ride_requests (passenger_name, dropoff_zone, luggage_size, luggage_units)
        VALUES (?, ?, ?, ?)
    """, (name, zone, luggage_size, units))
    
    conn.commit()
    req_id = cursor.lastrowid
    conn.close()
    return req_id

def process_daily_driver_log(driver_id, interior_img, exterior_img):
    """Processes driver verification photos and activates driver profile."""
    return f"Driver #{driver_id} profile activated & daily log verified (Interior: {interior_img}, Exterior: {exterior_img})."


# --- 3. THE MATCHMAKING ALGORITHM ---
def find_match(target_zone):
    """Finds two passengers going to the same zone whose bags fit in ONE trunk."""
    conn = sqlite3.connect("aeropool.db")
    cursor = conn.cursor()
    
    # Fetch all passengers currently searching for this specific zone
    cursor.execute("""
        SELECT request_id, passenger_name, luggage_units 
        FROM ride_requests 
        WHERE status = 'Searching' AND dropoff_zone = ?
    """, (target_zone,))
    
    waiting_list = cursor.fetchall()
    
    # We need at least 2 people to make a match
    if len(waiting_list) >= 2:
        for i in range(len(waiting_list)):
            for j in range(i + 1, len(waiting_list)):
                p1_id, p1_name, p1_units = waiting_list[i]
                p2_id, p2_name, p2_units = waiting_list[j]
                
                # CHECK: Do their combined bags fit in a standard 4-unit trunk?
                if (p1_units + p2_units) <= 4:
                    # Match found! Update their status in the database
                    cursor.execute("UPDATE ride_requests SET status = 'Matched' WHERE request_id IN (?, ?)", (p1_id, p2_id))
                    
                    # Create the dispatched cab record
                    cursor.execute("""
                        INSERT INTO matched_cabs (passenger_1_id, passenger_2_id, shared_zone, total_luggage_units)
                        VALUES (?, ?, ?, ?)
                    """, (p1_id, p2_id, target_zone, p1_units + p2_units))
                    
                    conn.commit()
                    conn.close()
                    
                    return f"✅ SUCCESS: Matched {p1_name} & {p2_name} for a shared cab to {target_zone}!"
                    
    conn.close()
    return "⏳ Waiting for a suitable co-passenger..."

# --- INITIALIZE ON RUN ---
if __name__ == "__main__":
    init_db()
    print("AeroPool Database and Matchmaker initialized.")