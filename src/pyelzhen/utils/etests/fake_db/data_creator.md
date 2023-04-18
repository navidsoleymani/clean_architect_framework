# Data Creator

Using this tool, you can create temporary data to use this data for your tests.
- properties:
  - app_name: This property represents the name of the Django app that must be set as required. The type format of this is this property string.
  - model_name: This property represents the name of the Django model that must be set as required. The type format of this is this property string.
  - schema: This property represents schema-class that must be set as required. The type format of this is this property pydantic.BaseModel.
  - default_values: This property represents default values that must be set as optional. The type format of this is this property dictionary.
  - dependencies: This property represents the prerequisites for building a model, which itself is a class of the same type that must be set arbitrarily. But keep in mind that filling these prerequisites, although optional, causes a camera. The type format of this is a list of classes with the same type.

- tools:
  - get: This tool helps you to produce an object of your choice.
  - create: This tool helps you get an object that you have already created.
  - orphan: This tool helps you to create and receive an object without considering a specific dependency.

## usage
