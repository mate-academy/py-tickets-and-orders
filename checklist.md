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
5. Always include `related_name` in relationships for better readability and maintainability

Good example:
```python
class Ticket(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='tickets')
```

Bad example:
```python
class Ticket(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
```

6. Use the `@transaction.atomic` decorator instead of using `with transaction.atomic:` for better readability and to ensure the entire function executes within a single transaction context

7. Place each argument on a new line, including `self`, with proper indentation and formatting
 
Good example:

```python
def __init__(
        self, 
        name: str,
        age: int
) -> None:
```

Bad example:

```python
def __init__(self, 
             name: str,age: int) -> None:
```

8. To improve the code's readability and maintainability, it’s better to use the previously created function

 Good example:

```python
def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)

def update_user(user_id: int) -> User:
    user = get_user(user_id)
```

 Bad example:

```python
def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)

def update_user(user_id: int) -> User:
    user = get_user_model().objects.get(pk=user_id)
```

9. If there’s no additional formatting or variables to include in the string, using an `f-string` is unnecessary. 

10. To improve code clarity, it’s best to specify the type of `QuerySet` returned in the type annotations.

Good example:

```python
def get_orders(username: str = None) -> QuerySet[Order]:
    return Order.objects.all()
```

 Bad example:

```python
def get_orders(username: str = None) -> QuerySet:
    return Order.objects.all()
```

## Clean Code

1. To maintain clarity and organization, please avoid adding comments directly in the repository code.