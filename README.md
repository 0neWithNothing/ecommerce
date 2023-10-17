# eCommerce Shop API

This is a API for merch eCommerce Shop

### Functionality

- JWT authentication and OAuth 2 with Google
- Manage user data (Address and Personal data for ordering)
- Admin user can manage categories, products, images for products and sizes
- Normal user can add/remove/update order-items to cart
- Payment simulation with Stripe


### Installation

1. Copy repository
2. Create `.env` file and put this variables </br>
~~~
DEBUG=1
SECRET_KEY='yoursecret'
ALLOWED_HOSTS=localhost 127.0.0.1

#### You can leave it as it is and just don't use endpoint with OAuth
DJANGO_GOOGLE_OAUTH2_CLIENT_ID='your data, but '
DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET='your data'

#### You can leave it as it is and just don't use endpoint with checkout (its only simulation of payment)
STRIPE_PUBLIC_KEY="your data"
STRIPE_SECRET_KEY="your data"
STRIPE_WEBHOOK_SECRET='your data'

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=postgres
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
~~~

3. Run `docker compose up -d --build`
4. Go to [localhost:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
5. You can create user with admin permission with `docker compose exec web python manage.py createsuperuser`
