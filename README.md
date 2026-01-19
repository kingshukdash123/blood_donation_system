## 📘 API Route Details & Functionalities

<details>
<Summary>API Routes</Summary>

#### Authentication Routes
```http
    POST /auth/register
    POST /auth/login
    POST  /auth/logout
    GET  /auth/me
```
#### User Profile
```http
    GET  /donor/profile
    PUT  /donor/profile

    GET  /blood-bank/profile
    PUT  /blood-bank/profile

    GET  /hospital/profile
    PUT  /hospital/profile
```

#### Hospital Routes
```http
    POST /hospital/blood-requests
    GET  /hospital/blood-requests?status=PENDING
    GET  /hospital/nearby-blood-banks
```

#### Blood Bank Routes
```http
    GET  /blood-bank/blood-requests?status=PENDING
    POST /blood-bank/blood-requests/{request_id}/fulfill
    POST /blood-bank/blood-requests/{request_id}/alert

    GET  /blood-bank/inventory
    PUT  /blood-bank/inventory

    GET  /blood-bank/blood-requests/{request_id}/donors

```

#### Donor Routes
```http
    GET  /donor/alerts?status=SENT
    POST /donor/alerts/{alert_id}/respond
             
    POST /donor/donations
    PUT  /donor/availability
```

#### WebSocket Routes
```http
    WS /ws/donor/{donor_id}
    WS /ws/blood-bank/{blood_bank_id}
```

#### Admin Routes
```http
    POST /admin/verify-user/{user_id}
    GET  /admin/users
    GET  /admin/stats
```
---
---
</details>

<details>
<Summary>API Routes Details</Summary>

## 🔐 Authentication Routes

### POST `/auth/register`

**Access:** Public  
**Role:** Hospital / Blood Bank / Donor  

#### Purpose
Registers a new user in the system.

#### Functionality
- Accepts user details:
  - Name
  - Phone number
  - Password
  - Role
- Hashes password using **bcrypt**
- Creates a record in the `users` table
- Creates role-specific records:
  - `hospitals`
  - `blood_banks`
  - `donors`
- Sets `is_verified = false` (requires admin verification)

#### Validations
- Phone number must be unique
- Role must be valid
- Password strength validation

---

### POST `/auth/login`

**Access:** Public  

#### Purpose
Authenticates user and issues JWT token.

#### Functionality
- Validates phone number and password
- Checks if the user is verified
- Generates JWT access token
- Returns:
  - Access token
  - User role

#### Side Effects
- JWT token is required for all protected routes

---

### POST `/auth/logout`

**Access:** Authenticated User  

#### Purpose
Logs out the user.

#### Functionality
- Invalidates JWT (token blacklist or frontend discard)
- Clears session (if applicable)

---

### GET `/auth/me`

**Access:** Authenticated User  

#### Purpose
Fetch logged-in user’s basic information.

#### Functionality
- Extracts user data from JWT
- Returns:
  - User ID
  - Role
  - Phone number
  - Verification status

---

## 👤 User Profile Routes

### GET `/donor/profile`

**Access:** Donor  

#### Purpose
Fetch donor profile details.

#### Returns
- Blood group
- Availability status
- Last donation date
- Location

---

### PUT `/donor/profile`

**Access:** Donor  

#### Purpose
Update donor profile.

#### Updates
- Location
- Contact information
- Blood group (optional)

---

### GET `/blood-bank/profile`

**Access:** Blood Bank  

#### Purpose
Fetch blood bank profile details.

---

### PUT `/blood-bank/profile`

**Access:** Blood Bank  

#### Purpose
Update blood bank details.
- Address
- Location
- Contact information

---

### GET `/hospital/profile`

**Access:** Hospital  

#### Purpose
Fetch hospital profile details.

---

### PUT `/hospital/profile`

**Access:** Hospital  

#### Purpose
Update hospital information.

---

## 🏥 Hospital Routes

### POST `/hospital/blood-requests`

**Access:** Hospital  

#### Purpose
Create a new blood request.

#### Functionality
- Hospital specifies:
  - Blood group
  - Units required
- Creates a record in `blood_requests`
- Sets request status to `PENDING`

---

### GET `/hospital/blood-requests?status=PENDING`

**Access:** Hospital  

#### Purpose
View hospital’s own blood requests.

#### Features
- Filter requests by status:
  - `PENDING`
  - `FULFILLED`
  - `ALERTED`

---

### GET `/hospital/nearby-blood-banks`

**Access:** Hospital  

#### Purpose
View nearby blood banks.

#### Functionality
- Uses hospital latitude and longitude
- Returns blood banks sorted by distance

---

## 🏦 Blood Bank Routes

### GET `/blood-bank/blood-requests?status=PENDING`

**Access:** Blood Bank  

#### Purpose
View nearby hospital blood requests.

---

### POST `/blood-bank/blood-requests/{request_id}/fulfill`

**Access:** Blood Bank  

#### Purpose
Fulfill a blood request directly from inventory.

#### Functionality
- Checks inventory availability
- Deducts blood units
- Updates request status to `FULFILLED`
- Links blood bank to the request

#### ⚠ Transaction Safety
- Inventory update and request update occur atomically

---

### POST `/blood-bank/blood-requests/{request_id}/alert`

**Access:** Blood Bank  

#### Purpose
Alert nearby donors when inventory is insufficient.

#### Functionality
- Finds eligible nearby donors
- Creates entries in `donor_alerts`
- Sends real-time WebSocket notifications
- Updates request status to `ALERTED`

---

### GET `/blood-bank/inventory`

**Access:** Blood Bank  

#### Purpose
View current blood inventory.

---

### PUT `/blood-bank/inventory`

**Access:** Blood Bank  

#### Purpose
Update blood inventory counts.

#### Examples
- Add units after a donation
- Correct mismatched inventory data

---

### GET `/blood-bank/blood-requests/{request_id}/donors`

**Access:** Blood Bank  

#### Purpose
View donor responses for a specific blood request.

#### Returns
- Donor ID
- Response status
- Timestamp

---

## 🧑‍🦰 Donor Routes

### GET `/donor/alerts?status=SENT`

**Access:** Donor  

#### Purpose
View received blood request alerts.

---

### POST `/donor/alerts/{alert_id}/respond`

**Access:** Donor  

#### Purpose
Accept or decline a blood request.

#### Functionality
- Updates alert status
- Locks donor if accepted
- Notifies the blood bank

---

### POST `/donor/donations`

**Access:** Donor  

#### Purpose
Record a blood donation.

#### Functionality
- Creates donation record
- Updates blood bank inventory
- Updates donor’s last donation date

---

### PUT `/donor/availability`

**Access:** Donor  

#### Purpose
Mark donor as available or unavailable.

---

## 🔌 WebSocket Routes

### WS `/ws/donor/{donor_id}`

**Access:** Donor  

#### Purpose
Real-time blood alert notifications.

#### Events
- New blood request alert
- Request cancellation
- Thank-you notifications

---

### WS `/ws/blood-bank/{blood_bank_id}`

**Access:** Blood Bank  

#### Purpose (Optional)
- Real-time donor acceptance updates
- Inventory update notifications

---

## 🛡️ Admin Routes

### POST `/admin/verify-user/{user_id}`

**Access:** Admin  

#### Purpose
Verify newly registered users.

---

### GET `/admin/users`

**Access:** Admin  

#### Purpose
View all registered users.

---

### GET `/admin/stats`

**Access:** Admin  

#### Purpose
View system analytics.

#### Example Statistics
- Total donors
- Total blood requests
- Fulfilled vs pending requests

</details>
