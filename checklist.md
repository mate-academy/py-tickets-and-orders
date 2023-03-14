# Сheck Your Code Against the Following Points

## Don't Push db files
Make sure you don't push db files (files with `.sqlite`, `.db3`, etc. extension).

## Don't Forget to Add Migrations to your PR
This is a required for the tests to pass.

## Don't Repeat Yourself
Call the `save()` method only one time if it's possible.

Good example:
```python
user = get_user_model().objects.create_user(
    username=username, password=password
)

if first_condition:
    # some actions
if second_condition:
    # some actions
    
user.save()
```

Bad example:
```python
user = get_user_model().objects.create_user(
    username=username, password=password
)

if first_condition:
    # some actions
    user.save()
if second_condition:
    # some actions
    user.save()
```

## Code Style
1. Use one style of quotes in your code. Double quotes are preferable.
2. Implement `class Meta` only after you defined all attributes.

Good example:
```python
class Order(models.Model):
    created_at = ...
    user = ...

    class Meta:
        pass
```

Bad example:
```python
class Order(models.Model):
    created_at = ...

    class Meta:
        pass    

    user = ...
```

3. Choose correct and suitable variable names.

Good example:
```python
user = get_user_model().objects.create_user(
    username=username, password=password
)
```

Bad example:
```python
u = User.objects.create_user(
    username=username, password=password
)
```

4. Use `get_user_model()` instead of `User`, it is the best practice.

Good example:
```python
get_user_model().objects.create_user(
    username=username, password=password
)
```

Bad example:
```python
User.objects.create_user(
    username=username, password=password
)
```

## Clean Code
Add comments, prints, and functions to check your solution when you write your code. 
Don't forget to delete them when you are ready to commit and push your code.
