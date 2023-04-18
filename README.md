# PyElzhen

This framework is built on the basis of clean architecture.

## Requirements

- python==3.8.12
- pydantic==1.10.2
- Django==3.2.9
- djangorestframework==3.12.4
- Markdown==3.4.1
- django-filter==21.1

## Installation

Install using pip...

```
pip install git+http://192.168.59.2/elzhendevelopers/pyelzhen.git
```

### Definitions

- models: In this part, you should design your database models and be sure to add function 'to_dict' to your model.
  Adding the 'to_dict' function should definitely be considered, because the toolset built into this design will not
  work without this function. Also, for each model, a schema must be created exactly equal to the model. I emphasize
  again that this tool will not work without these two.
    - to_dict: A function to convert the model into a dictionary.
- schema: Schemas are the same language between different layers in the framework, and you can create an appropriate
  schema for each interaction between different layers.
    - model: Model schemas are schemas that are created for each model and include all the fields of a model.
- repository layer: The repository layer is created to manage the program's connections with the database, and there
  should be no direct connection with the database before and after this layer.
- interactor layer: In this layer, we create the necessary logic to generate a data. Keep in mind that in this layer we
  can communicate with zero or more other interactors, but we must pay attention to the fact that each interactor at
  most (zero or one) can communicate with one repository.
- view layer: This layer manages the communication between the view wrapper and the interactor layer. In this layer, we
  do not implement any logic and we have no connection with the database, and we are only allowed to receive the data
  sent to the lower layers from the client and prepare it for sending to the lower layers, as well as the response from
  the layer. It prepares the received data to be sent to the client.
- factory: The concept of a factor is that we do not instantiate any of the classes that are created in Repository,
  Interactor or View layers inside the body of the classes (inside the body of the layers). For this reason, we have a
  factory for each of these layers, which creates an instance of the class as we need based on our needs.
    - repository factory: An instance of the Repository layer based on our needs.
    - interactor factory: An instance of the Interactor layer based on our needs.
    - view factory: An instance of the View layer based on our needs.

## Example

Suppose we have created a project with Django and have met the prerequisites for the project to run. And we have
installed the desired library. As below...

```shell
cd /<<PROJECT_DIR>>/
source /venv/bin/activate
pip install git+http://192.168.59.2/elzhendevelopers/pyelzhen.git

```

- First, we create an application in Django.

```shell
python manage.py startapp app

```

- Next, we will create the following items in the created application.

```shell
cd /app/

tree
.
├── admin.py
├── apps.py
├── docs
│   └── app.postman_collection.json
├── fixtures
│   └── book
│   └── 1.json
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   └── __init__.py
├── models.py
├── org
│   ├── factories
│   │   ├── __init__.py
│   │   ├── interactors
│   │   │   ├── book
│   │   │   │   ├── __create.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── repositories
│   │   │   ├── book
│   │   │   │   ├── __create.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── views
│   │   ├── book
│   │   │   ├── __create.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── interactors
│   │   ├── book
│   │   │   ├── __create.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── models
│   │   ├── __author.py
│   │   ├── __book.py
│   │   └── __init__.py
│   ├── schemas
│   │   ├── api
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── models
│   │   ├── __book.py
│   │   └── __init__.py
│   ├── urls
│   │   └── book.py
│   └── views
│   ├── book
│   │   ├── __create.py
│   │   └── __init__.py
│   └── __init__.py
├── tests
│   ├── __init__.py
│   └── tests_integration
│   ├── book
│   │   ├── __create.py
│   │   └── __init__.py
│   └── __init__.py
├── urls.py
└── views.py

```

At this stage, we should start building tools and different layers of the program and put each of them in their proper
place.

- In the first step, we design and implement our models.

Note: Do not forget to implement 'to_dict' function.

```python
#!/app/org/models/__author.py
from django.db import models


class Author(models.Model):
    name = models.CharField()

    def to_dict(self, depth=1):
        if depth < 1:
            return self.pk
        tmp = {
            'pk': self.pk,
            'id': self.pk,
            'name': self.name,
        }
        return tmp

```

```python
#!/app/org/models/__init__.py
from .__author import Author as AuthorModel
```

```python
#!/app/models.py
from .org.models import AuthorModel
```

```python
#!/app/org/models/__book.py
from django.db import models
from app.models import AuthorModel


class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(to=AuthorModel, on_delete=models.CASCADE)

    def to_dict(self, depth=1):
        if depth < 1:
            return self.pk
        tmp = {
            'pk': self.pk,
            'id': self.pk,
            'title': self.title,
            'author': self.author.to_dict(depth=-1) if self.author else None,
        }
        return tmp

```

```python
#!/app/org/models/__init__.py
from .__author import Author as AuthorModel
from .__book import Book as BookModel
```

```python
#!/app/models.py
from .org.models import (
    AuthorModel,
    BookModel,
)

```

- In the second step, we create the corresponding schema for each model.

```python
#!/app/org/schemas/models/__author.py
from typing import Optional
from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: Optional[int]
    pk: Optional[int]
    name: Optional[str]
```

```python
#!/app/org/schemas/models/__init__.py
from .__author import AuthorSchema
```

```python
#!/app/org/schemas/models/__book.py
from typing import Optional, Union
from pydantic import BaseModel

from app.org.schemas.models import AuthorSchema


class BookSchema(BaseModel):
    id: Optional[int]
    pk: Optional[int]
    title: Optional[str]
    title: Optional[Union[int, AuthorSchema]]
```

```python
#!/app/org/schemas/models/__init__.py
from .__author import AuthorSchema
from .__book import BookSchema
```

- In the third step, we create a factory repository for each model.

```python
#!/app/org/factories/repositories/book/__ceate.py
from pyelzhen.apis.repositories import CreateRepository as Repository
from app.models import BookModel as Model


def create_repository_instance(*args, **kwargs):
    ret = Repository(model=Model)
    return ret

```

```python
#!/app/org/factories/repositories/book/__init__.py
from .__create import create_repository_instance
```

- In the fourth step, we create an interactor for each logic.

```python
#!/app/org/interactors/author/__ceate.py
from pyelzhen.apis.interactors import CreateInteractor as Base


class BookCreateInteractor(Base):
    pass


```

```python
#!/app/org/interactors/book/__init__.py
from .__create import BookCreateInteractor
```

- In the fifth step, we create a repository for each interactor.

```python
#!/app/org/factories/interactors/book/__ceate.py
from app.org.interactors.book import BookInteractor as Interactor
from app.org.factories.repositories.book import create_repository_instance as repository


def create_interactor_instance(*args, **kwargs):
    inst = Interactor(repository=repository(*args, **kwargs))
    return inst

```

```python
#!/app/org/factories/interactors/book/__init__.py
from .__create import create_interactor_instance
```

- In the sixth step, we create a APIView for each API.

```python
#!/app/org/views/book/__ceate.py
from pyelzhen.apis.views import CreateAPIView as Base


class BookCreateAPIView(Base):
    pass

```

```python
#!/app/org/views/book/__init__.py
from .__create import BookCreateAPIView
```

- In the seventh step, we create a factory for each view.

```python
#!/app/org/factories/views/book/__ceate.py
from app.org.views.book import BookUpdateAPIView as APIView

from app.org.factories.interactors.book import create_interactor_instance as interactor_instance
from app.org.schemas.model import (
    BookSchema as InputSchema,
    BookSchema as OutputSchema,
)


def create_api_view_instance(*args, **kwargs):
    input_schema_class = InputSchema
    output_schema_class = OutputSchema
    input_field_name_list = {
        'title',
        'author',
    }
    output_field_name_list = {
        'id',
        'title',
        'author',
    }
    rslt = APIView(
        interactor=interactor_instance(*args, **kwargs),
        input_schema_class=input_schema_class,
        output_schema_class=output_schema_class,
        input_field_name_list=input_field_name_list,
        output_field_name_list=output_field_name_list,
    )
    return rslt



```

```python
#!/app/org/factories/views/book/__init__.py
from .__create import create_api_view_instance
```

- Finally, we call this 'APIViewFactory' in the wrapper and add it to urlspattern.

```python
#!/app/org/urls/book.py
from django.urls import path

from app.org.factories.views.user import create_api_view_instance
from probeTesterBackend.views import APIViewWrapperNew

app_name = 'books'
urlpatterns = [
    path('v1', APIViewWrapperNew.as_view(view_creator_func=create_api_view_instance), name='create'),
]

```

```python
#!/app/urls.py
from django.urls import path, include

app_name = 'apps'
urlpatterns = [
    path('', include('app.org.urls.book')),

]

```

Now your REST API is ready to use.

## Documentation

### Repository

```python
from pyelzhen.apis.repositories import (
    BaseRepository,
    CreateRepository,
    ListRepository,
    RetrieveRepository,
    UpdateRepository,
)
``` 

Note: This tool is used to create a repository.

To use this tool, you just need to create a factory according to your model and pass your Django model to its
constructor.

```python
ret = CreateRepository(model=Model)
```

- methods:
    - creator: This code is used to create one or more objects.
        - prams:
            - output_schema_class:
                - type: pydantic.BaseModel
                - required
            - data:
                - type: Union[pydantic.BaseModel, List[pydantic.BaseModel]]
                - required
            - depth:
                - type: int
                - optional
                - default: 1
            - include_fields:
                - type: set
                - optional
                - default: ALL
            - exclude_fields:
                - type: set
                - optional
                - default: EMPTY
    - lister: This method returns a list of objects.
        - params:
            - output_schema_class:
                - type: pydantic.BaseModel
                - required
            - query_params:
                - type: pyelzhen.utils.schemas.QueryParamsSchema
                - required
            - depth:
                - type: int
                - optional
                - default: 1
            - paginate:
                - type: bool
                - optional
                - default: True
    - retriever: This function is used to find a
        - params:
            - output_schema_class:
                - type: pydantic.BaseModel
                - required
            - lookup_field:
                - type: Union[pyelzhen.utils.schemas.LookupFieldSchema, List[pyelzhen.utils.schemas.LookupFieldSchema]]
                - required
            - last_or_first:
                - type: str (FIRST or LAST)
                - optional
                - default: FIRST
            - depth:
                - type: int
                - optional
                - default: 1
    - updater: This function is used to update one or more objects.
        - params:
            - output_schema_class:
                - type: pydantic.BaseModel
                - required
                    - lookup_field:
                        - type: pyelzhen.utils.schemas.LookupFieldSchema
                        - required
                    - data:
                        - type: Union[pydantic.BaseModel, List[pydantic.BaseModel]]
                        - required
                    - update_fields:
                        - type: set
                        - optional
                        - default: ALL
                    - depth:
                        - type: int
                        - optional
                        - default: 1

All classes specified at the beginning of this section have above methods.
Apart from the base class, the rest of the classes have a method called run that can perform an operation according to
the name of that class.

### Interactor

```python
from pyelzhen.apis.interactors import (
    BaseInteractor,
    CreateInteractor,
    ListInteractor,
    RetrieveInteractor,
    UpdateInteractor,
)
``` 

This class is made to model the interactor layer and business logic is created in this layer using this tool. To create
an instance of this class, it is enough to pass an instance of the desired repository in its constructor.

```python
ret = CreateInteractor(repository=repository)
```

- methods:
    - set_params: The parameters of this method are actually the prerequisites for implementing the desired logic.
    - execute: The parameters of this method are used to perform operations related to transactions on the database.

Note: The values of these parameters can be different for each of the classes mentioned above.

### APIView

```python
from pyelzhen.apis.views import (
    BaseAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
``` 
This layer is for validating the input data from the client side and structuring it to be sent to the lower layers, and it also prepares the data received from the lower layers to be sent to the client.

```python
ret = CreateAPIView(
    interactor=interactor,
    input_schema_class=input_schema_class,
    output_schema_class=output_schema_class,
    input_field_name_list=input_field_name_list,
    output_field_name_list=output_field_name_list,
    lookup_field_key=lookup_field_key,
    expected_status_code=expected_status_code,
    default_values=default_values,
    hard_information=hard_information,
)
```
