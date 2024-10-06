# kim a.k.a Keep In Mind

kim is a public pip librairy. It's purpose is to keep in mind your variable so you can call update and delte them anytime anywhere. It's especially useful for very large project where it can be tough to call your variable in a recursive algorithme.

## Install

kim is compatible with python>=3.5 and doesn't require any other package from pip.
```bash
pip install kim-python
```


## How to use
### Create
To create a variable which you would like kim to remember use CreateOrUpdate :
```python
import kim

kim.CreateOrUpdate(category="my_category", name="my_variable", value="Hello World")

print(kim.my_category.my_variable)
print(type(kim.my_category.my_variable))
```
```bash
Hello World
<class 'str'>
```
Note that if your using an IDE with IntelliSense, you'll have the option to autofill kim.my_category.my_variable, but it requires one compilation.
### Update
You can update your variables also by calling CreateOrUpdate:
```python
import kim

kim.CreateOrUpdate(category="my_category", name="my_variable", value="Hello World")
print(kim.my_category.my_variable)
print(type(kim.my_category.my_variable))

kim.CreateOrUpdate(category="my_category", name="my_variable", value=["Hello world", {"foo": "bar"}])
print(kim.my_category.my_variable)
print(type(kim.my_category.my_variable))
```
```bash
Hello World
<class 'str'>
['Hello world', {'foo': 'bar'}]
<class 'list'>
```
### Delete
To erase every created variables call Clear :
```python
import kim

kim.CreateOrUpdate(category="my_category", name="foo", value=100)
kim.CreateOrUpdate(category="my_category", name="bar", value={"hello world": 1})

try:
    print(kim.my_category.foo)
except Exception as e:
    print(e)
try:
    print(kim.my_category.bar)
except Exception as e:
    print(e)

kim.Clear()

try:
    print(kim.my_category.foo)
except Exception as e:
    print(e)
try:
    print(kim.my_category.bar)
except Exception as e:
    print(e)
```
```bash
100
{'hello world': 1}
module 'kim' has no attribute 'my_category'
module 'kim' has no attribute 'my_category'
```

To delete a category use Remove without specify which variable to delete :
```python
import kim

kim.CreateOrUpdate(category="my_category", name="my_variable", value="Hello World")

kim.Remove(category="my_category")

try:
    print(kim.my_category.my_variable)
except Exception as e:
    print(e)
```
```bash
module 'kim' has no attribute 'my_category'
```
To delete all the variable use Clear


### Read
In addtion of fetching your variables with kim.my_category.my_variable you can use the function variables_dict to get a dictionary of the saved variables :

```python
import kim

kim.CreateOrUpdate(category="my_category", name="my_variable", value="Hello World")

print(kim.variables_dict())
```
```bash
{'my_category': {'my_variable': 'Hello World'}}
```
