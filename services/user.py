from db.models import User


def create_user(username, password, email=None, first_name=None, last_name=None):
    # Create a new user instance and set the fields
    new_user = User.objects.create_user(username=username, password=password, email=email or "", first_name=first_name or "",
                                        last_name=last_name or "")

    return new_user


def get_user(user_id):
    # Retrieve and return the user with the given ID
    # You should replace this with your own logic for fetching users from storage
    return User.objects.get(id=user_id)


def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    # Update the user fields if provided
    user = get_user(user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    # Save the updated user
    user.save()
