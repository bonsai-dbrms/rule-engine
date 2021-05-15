
## Bonsai : Business Intelligence Automation

  

For every business , there are a set of rules which define all actions and behaviours. Products which leverage technology for its distribution and usage may contain millions of rules , which are usually tightly coupled with multiple if-else statements within code or configuration files across services

  

Bonsai is a platform to store, evaluate and analyse all your business decisions/rules at a single place.

  

### Architecture

  

![BonsaiHLD](https://i.imgur.com/TKhjxvG.jpeg)

  

## On a high level , the platform has two components

- Bonsai Decision Service : hosts and evaluates business rules pertaining to particular namespace. Uses RedisJSON as the underlying storage for all the rules

- Bonsai UI : Interface for authoring and previewing all business rules . Interacts with the decision service for all operations
- 
### Examples of bonsai being used for 
- Loyalty Management System 
- Codless API's
- Pricing System 
- Insurance premium calculation 
- and many more...
# How it Works
### keywords 
- Namespace
- Rules
- entity

#### Namespace
The top most logical seperation of rules are on the basis of namespace. Namespace is one set of rules which are to be evaluated on some data. For example you are will build a namespace for a loyalty management system and all the rules regarding that will be saved under that namespace. 
 - The structure for saving our data is 
 ```
 {
  "tax_system": {}
 }
 ```
 Here namespace is : tax_system .
 #### Command used to create namespace is :
 ``````
JSON.SET namespace_name . {}
``````
#### Entity
Each Entity means the input into a namespace which inturn will be given an out put after  evaluation of the rules present in that namespace and 
#### Rules
##### sub keywords
- predicates: this just means the input conditions for your rules.
- results: this means the output conditions for your rules
- operators: we have 7 operators :
       - `eq` which means `=`
       - `range` which means the value should lie between the given range(upper limit not included)
       - `contains` which means that the string should contain the input value given.
       - `gt` which means greater than or `>`
       - `gte` which means greater than or equal to `>=`
       - `lt` which means lesser than `<`
       - `lte` which means lesser than or equal to `<=`


For example we want to create a rule for a customer who has places 5 orders or less and has prime membership of my ecommerce site i want to give him a 10% discount. 

So in this case i have two inputs `orders` and `member_type` and one output `discount_value`. 
so in our case one example predicate(input) of `province is Ontario` can be
a predicate consists of 4 parts : 
```
{
          "attribute_name": "Province", # the name of your input
          "operator": "eq", # type of operation
          "type": "string", # type of input such as INT or STRING
          "value": "Ontario" # value of the input you want to gove 
 }
```

Each rules is  a command which decides what should be the output to any particular input ( `entity` )

Every rule gets saved into a namespace via the following format . 
  example used in this rule is if province is` Ontario and city is Toronto the tax rate will be 35`
  ```
  this is the rule object: 
 {
  "tax_system": {
    "123456": {
      "id": 123456,
      "namespace": "tax_system",
      "rule_description": "this is a test rule",
      "predicates": [
        {
          "attribute_name": "Province",
          "operator": "eq",
          "type": "string",
          "value": "Ontario"
        },
        {
          "attribute_name": "City",
          "operator": "eq",
          "type": "string",
          "value": "Toronto"
        }
      ],
      "result": {
        "attribute_name": "tax_rate",
        "operator": "eq",
        "type": "string",
        "value": "35"
      }
    }
  }
}
```
Here namespace is : `loyalty_system` and rule_id is : `123456`.
 #### Command used to create namespace is :
 ``````
JSON.SET namespace_name .rule_id rule_object
``````

## Features

#### Rule creation 
 ![CREATION GIF](https://i.imgur.com/5dilrfg.gifv)
A very easy to use USER EXPERIENCE to add inputs and configure outputs as seen in the gif above.

#### Rule Visualization
![VISUALIZATION GIF](https://i.imgur.com/5dilrfg.gifv)
Once rule is created you can easily visualize in the form of a flow chart which makes it even easier to debug for business teams `which is one of the main disadvantages of a traditional rule engine`

#### Rule Evaluation
![VISUALIZATION GIF](https://i.imgur.com/5dilrfg.gifv)
The code uses pattern matching algorithms to see which rule fits the entity best and also emits the order in which rules were executed (in other words chained rule execution is also possible)

#### Rule Analysis
![Analysis GIF](https://i.imgur.com/5dilrfg.gifv)
We have used `redis Timeseries database` to publish basic telemetery of rule excution and evaluation processes to give the business users capabilities to make data driven decisions on the basis of performance of rules in their namespace.
