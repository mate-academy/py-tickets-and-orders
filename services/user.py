import init_django_orm
from django.db.models import QuerySet
from db.models import User

def create_user(
  username: str,
  password: str,
  email: str = None,
  first_name: str = None,
  last_name: str = None
) -> None:
  create_fields = {}
  if email:
      create_fields["email"] = email
  if first_name:
      create_fields["first_name"] = first_name
  if last_name:
      create_fields["last_name"] = last_name
  user = User.objects.create_user(username, password, **create_fields)
  user.save()

def get_user(user_id: int) -> User:
  return User.objects.get(id=user_id)

def update_user(
  user_id: int,
  username: str = None,
  password: str = None,
  email: str = None,
  first_name: str = None,
  last_name: str = None
) -> None:
  user = User.objects.get(id=user_id)
  if password:
    user.set_password(password)
    user.save()
  update_fields = {}
  if username:
        update_fields["username"] = username
  if email:
      update_fields["email"] = email
  if first_name:
      update_fields["first_name"] = first_name
  if last_name:
      update_fields["last_name"] = last_name
  
  User.objects.filter(id=user_id).update(**update_fields)
  
                
    
