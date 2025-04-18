#  Household Services Application - V1

A multi-user dynamic web application designed for managing and booking home services like plumbing, AC repair, cleaning, and more. Built with **Flask**, **SQLite**, and **Bootstrap**, the app provides distinct roles for Admins, Service Professionals, and Customers, each with customized access and functionality.

---

##  Roles & Functionalities

###  Admin (Superuser)
- Single hardcoded superuser (no registration required)
- Admin dashboard for full control
- Can:
  - Monitor all users
  - Create/update/delete services with base prices
  - Approve or block service professionals
  - Block customers for fraud/poor reviews
  - View/search users or professionals

###  Service Professional
- Can register and log in
- Profile includes ID, name, experience, service type, etc.
- Actions:
  - View and accept/reject assigned service requests
  - Exit location when service is marked closed by the customer
  - Publicly visible based on customer reviews

###  Customer
- Can register and log in
- Can:
  - Search for services by name or pin code
  - Create, update, or close service requests
  - Review professionals after service

---

##  Key Concepts

### ✅ Service
- A service offered on the platform (e.g., plumbing, AC repair)
- Attributes: `id`, `name`, `price`, `time_required`, `description`

###  Service Request
- A request made by a customer for a service
- Attributes:
  - `id`, `service_id`, `customer_id`, `professional_id`
  - `date_of_request`, `date_of_completion`
  - `service_status`: requested / assigned / closed
  - `remarks`

---

##  Tech Stack

| Layer         | Technology             |
|---------------|------------------------|
| Backend       | Flask (Python)         |
| Frontend      | HTML, CSS, Bootstrap   |
| Templating    | Jinja2                 |
| Database      | SQLite (only)          |
| Auth          | Flask Session / JWT    |

---

##  Core Features

- Role-based login (RBAC): Admin / Professional / Customer
- Dynamic dashboard routing based on user role
- Service management with CRUD by Admin
- Review system for professionals
- Location and keyword-based search
- Session handling and login/logout flow

---
