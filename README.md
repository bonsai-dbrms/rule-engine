
## Bonsai : Business Intelligence Automation

For every business , there are a set of rules which define all actions and behaviours. Products which leverage technology for its distribution and usage may contain millions of rules , which are usually tightly coupled with multiple if-else statements within code or configuration files across services

Bonsai is a platform to store, evaluate and analyse all your business decisions/rules at a single place.

### Architecture

![BonsaiHLD](https://i.imgur.com/TKhjxvG.jpeg)

 - On a high level , the platform has two components 
	 - Bonsai Decision Service :  hosts and evaluates business rules pertaining to  particular namespace. Uses RedisJSON as the underlying storage for all the rules
	 -  Bonsai UI :  Interface for authoring and previewing all business rules . Interacts with the decision service for all operations
