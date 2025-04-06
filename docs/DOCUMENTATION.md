# ✅ Authentication & Permissions Module

### 🎯 Module Goals

- Support multiple farms per user
- Role-based team access
- Flexible permission engine
- Secure auth via JWT
- Scalable + production-ready

---

## 👥 Users & Teams

- Users can belong to multiple farms
- Each user is assigned to a farm via `TeamMember`
- Roles determine access level (e.g., Farmer, Vet, Admin)
- `is_admin` flag used for farm-level admin rights

---

## ✉️ Invite Flow

- Farm admin invites user (email, role, optional `is_admin`)
- Invite link sent as token
- Invite expires in 2 days
- User sets password and activates account
- `TeamMember.expires_at` supports temp users

---

## 🔐 Auth System

- JWT-based auth using SimpleJWT
- Endpoints:
  - `POST /api/auth/token/` → login
  - `POST /api/auth/refresh/` → refresh token
- `User.active_farm` determines farm context
- Switch farm: `POST /api/auth/switch-farm/`
- User activity (login/switch) is logged

---

## 🧩 Roles & Permissions

- `Role` has a ManyToMany to `Permission`
- Permissions have `code` + `label` (e.g. `animals.view`)
- Admin UI allows assigning multiple permissions per role
- Each team member inherits role’s permissions

---

## ✅ Backend Utilities

- `has_permission(user, "animals.add")` → True/False
- Handles:
  - Farm membership
  - Expired users
  - Role permission lookup
- DRF support via:
```python
permission_classes = [IsAuthenticated, HasRolePermission("code")]



API Endpoints Summary
Endpoint	Method	Description
/api/auth/token/	POST	Login
/api/auth/token/refresh/	POST	Refresh token
/api/auth/me/	GET	Get current user info
/api/auth/switch-farm/	POST	Change active farm
/api/auth/invite/	POST	Invite user to farm
/api/auth/accept-invite/	POST	Accept invite + set password
/api/auth/my-permissions/	GET	Get permissions for active farm
📦 Example Permissions
Code	Label
animals.view	View Animals
animals.add	Add Animals
users.invite	Invite Users
reports.view	View Reports
💻 Frontend Integration Tips
Call /auth/me to get farm and user info

Call /my-permissions and store list

Hide/show buttons or routes like:

tsx
Copy
Edit
if (permissions.includes("animals.add")) {
  showAddAnimalButton()
}



What does "Move to Animal" mean?
When a new animal is born, you:
Track the birth info in AnimalBirth (✅ already done)

After some time (e.g. 9 months), the baby becomes part of the active herd

So you move its data into the Animal model (the real list of animals you manage daily)

💼 In Enterprise Terms
This is like promoting a newborn from the delivery room → to the main livestock system

You:

Copy the fields (number, species, parents, gender, birth date)

Set moved_to_animals = True in the birth record

Avoid double data entry

Build full lifecycle traceability 🔄

🔁 When do we trigger the move?
Two ways:

✅ Manually → via POST /api/animal/births/<id>/move-to-animal/

✅ Automatically → after 9 months (in background script or scheduled job)

👀 Real World Example
Let’s say:

You created a goat birth NB-0925

9 months passed

You now want it in the main animal list to track its future vaccinations, death, breeding, etc.

💥 You call move-to-animal/, and it appears in /animals/




 Animal Module is 100% Completed 🎉
You’ve built:

🐄 Animal creation (with list, images, custom fields, validation)

👶 Birth tracking (manual + auto move)

💀 Death management (status, logs, images)

💉 Vaccination tracking (with filtering, expiration logic, logging)

🧠 Vaccine Recommendation model (future-proof for AI)

⚙️ Custom Fields (dynamic, required, validated, stored, filtered)

📁 Postman collections

🧪 Tested both in Django Admin and API

📊 Logging with UserLog

🔐 Permission + Multitenancy respected

Next steps could be:

  🔄 Export reports

  📆 Schedules / reminders for vaccines

  📈 Analytics per farm

  🤖 AI agent for vaccine suggestions

  🧬 Genetic tracking (optional)



## 🧱 Project & Personal Product Module

📁 **Location:** `product_catalogue/models/project.py`

---

### 🧩 Purpose & Design

This module separates **project-specific product usage** from general farm products to support both **centralized product management** and **project-level tracking**.

---

### 📌 `Project`

Represents a specific project or initiative within the farm  
(e.g., a seasonal planting project, livestock breeding program).

#### Fields:
- `name`: Project title.
- `description`: Optional details.
- `start_date`, `end_date`: Timeline of the project.
- `farm`: Linked via `FarmLinkedModel`.
- `created_by`: User who created the record.
- `created_at`: Auto timestamp.

#### Example:
```json
{
  "name": "Spring Wheat Cultivation",
  "start_date": "2025-03-01",
  "end_date": "2025-06-30"
}

PersonalProduct
Represents a product used by a specific project.
It links a farm product to a project and tracks how it's consumed or assigned.

Fields:
project: FK to Project.

product: FK to global Product.

quantity: Quantity allocated.

notes: Optional comments.

farm: Inherited from FarmLinkedModel.

created_by: User who created it.

created_at: Timestamp.

Constraints:
A product can only appear once per project
➤ Enforced via unique_together (project, product)

Example:
json
Copy
Edit
{
  "project": "Spring Wheat Cultivation",
  "product": "Organic Fertilizer",
  "quantity": 50,
  "notes": "Used in phase 1"
}
🔄 Why This Design?
✅ Clean separation between farm-level and project-level product data

✅ Enables tracking how products are used in real operations

✅ Scalable for reporting, stock monitoring, and analytics

