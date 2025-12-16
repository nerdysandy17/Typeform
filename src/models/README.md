# Data model

In order to ensure the predicability of api responses, we leverage pydantic's ```BaseModel```.

These models allow to define the schema of expected input / output of an api endpoint in a few line of codes while including features such as data type validators.

## Add a new model

A new model can be defined by subclassig the ```BaseModel``` class.

```python
from pydantic import BaseModel

class NewModel(BaseModel):
    attribute1: str
    attribute2: int
```
