# Tickets and orders

Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before starting.

In `db/models.py` you already have tables you created earlier. Now
you have to create or edit tables:
1. `Movie`, add:
    - index on field `title`.
2. `Order`, with such fields:
    - datetime field `created_at`, the datetime when the order was created,
set `auto_now_add` to fill this field automatically during the creation.
    - foreign key `user`, the user that created the order.
   
There should be implemented the string representation of the order:
```python
print(Order.objects.first())
<Order: 2022-03-15 15:59:50>
```
Orders should be ordered from the newest to the oldest by default.

3. `Ticket`, with such fields:
   - foreign key `movie_session`, is related to the table `MovieSession`
   - foreign key `order`, is related to the table `Order`
   - integer field `row`, the row of the seat 
   - integer field `seat`, number of the seat in row

There should be implemented the string representation of the ticket, show
information about movie session, row and seat:
```python
print(Ticket.objects.first())
<Ticket: Speed 2020-11-11 09:30:00 (row: 6, seat: 12)>
```
Ticket should implement method `clean()`. This method should check if 
`row` and `seat` are correct and are not greater than values in 
`ticket.movie_session.cinema_hall`, if they are - ValidationError should
be raised. You also should override method `save()` and add there 
`full_clean()` method call in order to call method `clean()` when you 
save the ticket.

Also fields `row`, `seat`, `movie_session` should be unique together. 
Use `UniqueConstraint`, [constraints](https://medium.com/@timmerop/how-to-add-a-uniqueconstraint-concurrently-in-django-2043c4752ee6).
```python
import datetime

cinema_hall = CinemaHall.objects.create(name="Blue", rows=18, seats_in_row=24)
movie_session = MovieSession.objects.create(
    show_time=datetime.datetime(2022, 3, 20, 19, 30),
    movie_id=1, 
    cinema_hall=cinema_hall)
order = Order.objects.create(user_id=1)

ticket = Ticket.objects.create(
    movie_session=movie_session,
    order=order,
    row=19,
    seat=20
)
ticket.clean()
# django.core.exceptions.ValidationError: {'row': ['row number must be in available range: (1, rows): (1, 18)']}

ticket = Ticket.objects.create(
    movie_session=movie_session,
    order=order,
    row=17,
    seat=26
)
ticket.clean()
# django.core.exceptions.ValidationError: {'seat': ['seat number must be in available range: (1, seats_in_row): (1, 24)']}
```
4. Custom model `User`, that model should inherit from `AbstractUser`. To replace
the default user model with custom, edit `settings.py`, inside `INSTALLED_APPS`, 
add there two apps: `"django.contrib.auth"` and `"django.contrib.contenttypes"`, also
add `AUTH_USER_MODEL` equals to `"db.User"`.

Use the following command to load prepared data from fixture to test and debug your code:
  
`python manage.py loaddata cinema_db_data.json`.

- After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin.user`
  - Password: `1qazcde3`

In `services` you already have services you created earlier. Now
you have to create or edit such services:
1. Edit `movie.py`, edit function:
   - `get_movies`, add optional argument `title`, if `title` is not `None`,
function returns result as earlier, but also filter movies with title 
that contains `title`.
2. Create `user.py`, add such functions:
   - `create_user`, takes `username`, `password`, optional parameters 
`email`, `first_name`, `last_name`. The method should save user properly (password 
should be encrypted), use method `.create_user()` for this purpose. Also, 
set fields if appropriate optional values are provided.
   - `get_user`, takes `user_id`, returns user with the given id.
   - `update_user`, takes `user_id`, optional parameters `username`, `password`, 
`email`, 
`first_name`, `last_name`. Update user with
provided id and set fields if appropriate values are provided. To save password
properly use the method `.set_password()`.
3. Edit `movie_session.py`, add such functions:
   - `get_taken_seats`, takes `movie_session_id` - the id of the
movie session, list of dicts with rows and seats of the tickets of the 
provided session. Example:
   ```python
   get_taken_seats(movie_session_id=1) == [
        {"row": 7, "seat": 10},
        {"row": 7, "seat": 11}
    ]
   ```
4. Create `order.py`, add such functions:
   - `create_order`, takes `tickets` - list of the tickets, where each ticket 
is a dict with keys: row, seat, movie_session, `username` - username of the
user, optional `date`. This method should create an order with the provided user,
if `date` is provided, set `created_at` to this date. Then creates 
tickets with that order and data provided in `tickets`.
   ```python
   tickets: [
       {
           "row": 6,
           "seat": 12,
           "movie_session": 1
       },
       {
           "row": 6,
           "seat": 13,
           "movie_session": 1
       }
   ]
   create_order(tickets=tickets, username="Username_1", date="2022-4-20 11:27")
   ```
   The function should be executed completely or not executed at all. For this
   purpose use [transaction.atomic](https://docs.djangoproject.com/en/4.0/topics/db/transactions/).
   - `get_orders`, takes optional `username`, if `username` is provided, returns
all orders for the user with the provided username, else returns all orders.
5. Edit `movie.py`, edit function:
    - Edit `create_movie`, make it as transaction too.

### Note: Check your code using this [checklist](checklist.md) before pushing your solution.
