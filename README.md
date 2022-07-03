# address_book
Address Book api that uses django rest framework & sqllite

Functionality

1. User is able to create a new address
	○  User will not be able to add a duplicated address to their account
2. User is able to retrieve all their postal addresses
	○  Pagination functionality (default page size = 20)
3. User is able to update existing addresses
4. User is able to delete one address

## Setup Instructions:

### Clone repository:

```console
$ git clone https://github.com/faic/address_book
```

### Install library and dependency requirements:

```console
$ pip install -r requirements.txt
```

### Set up DB:

```console
$ python manage.py makemigrations
$ python manage.py migrate
```

### Run the app:

```bash
$ python manage.py runserver
```

### Run tests:

```bash
$ python manage.py test
```

### Create users:
Use the following commands to create super users in the system
```bash
$ python manage.py createsuperuser --username=username1 --email=email1@example.com
```

## API Usage:
### Login
User needs to login to perform any kind of requests. The login use email and
password fields of user. In return for login call you will receive authentication
token which should be used in other api calls. If no authentication params provided,
403 status would be returned for address requests.

#### HTTP request
```bash
POST http://{url}/api/login
```

#### Request headers
| Header | Value |
|--------|-------|
| Content-Type | application/json |

#### Request body
In the request body, supply a JSON representation of a user object with required `username`, `password`fields.

#### Response
If successful,  this method returns 200 ok response code and json object with `token` field in the response body

#### Example
Request
Here is an example of a request
```json
POST http://{url}/api/login
Content-type: application/json

{
"token": "9351a6e43a50d6bb7429f1ace7b2068b6f127567"
}
```

### Create Address
Create an address using api.
Note: Duplicate address with same `country, state, city, address_1, address_2` fields are not allowed.
Also there is validation for correct country/country code & email format.

#### HTTP request
```bash
POST http://{url}/addresses/
```

#### Request headers
| Header | Value |
|--------|-------|
| Authorization | Token {token_value} |
| Content-Type | application/json |

#### Request body
In the request body, supply a JSON representation of an items object.


#### Response
If successful, this method returns `201 Created` response code and returns the
item  in the response body

#### Example
##### Request
Here is an example of a request.
```json
POST http://{url}/addresses/
Content-type: application/json

{
	"name": "address 1", 
	"country": "US", 
	"state": "CA", 
	"city": "Los Angeles", 
	"postal_code": "90210", 
	"address_1": "Beverly Hills",
	"email": "test_email001@gmail.com"
}
```

##### Response
Here is an example of the response.
```json
{
	"id": 1, 
	"name": "address 1", 
	"country": "US", 
	"state": "CA", 
	"city": "Los Angeles", 
	"postal_code": "90210", 
	"address_1": "Beverly Hills", 
	"address_2": "", 
	"phone_number": "", 
	"email": "test_email001@gmail.com"
}

```

### Get Address
Fetch addresses api


#### HTTP request
Get all addresses from database. This api call uses pagination. Default page size is 20.


```bash
GET http://{url}/addresses/
```

#### Request headers
| Header | Value |
|--------|-------|
| Authorization | Token {token_value} |
| Content-Type | application/json |


#### Response
If successful, this method returns 200 OK response code and returns 
json object with paginated list of addresses in `results` list field,
total number of addresses in `count` field and possible link to previous/next page in
`next`, `previous`' fields, with possible `null` value.

#### Example
##### Request
Here is an example of a request.
```json
GET http://{url}/addresses/
Content-type: application/json
```

##### Response
Here is an example of the response.
```json
{
	"count": 3, 
	"next": "http://testserver/addresses/?page=2", 
	"previous": null, 
	"results": [
		{
			"id": 1, 
			"name": "address 0", 
			"country": "US", 
			"state": "CA", 
			"city": "Los Angeles", 
			"postal_code": "90210", 
			"address_1": "Beverly Hills 0", 
			"address_2": "", 
			"phone_number": "", 
			"email": ""
		}, 
		{
			"id": 2, 
			"name": "address 1", 
			"country": "US", 
			"state": "CA", 
			"city": "Los Angeles", 
			"postal_code": "90210", 
			"address_1": "Beverly Hills 1", 
			"address_2": "", 
			"phone_number": "", 
			"email": ""
		}
	]
}

```

Get an address with database id

```bash
GET http://{url}/addresses/{id}
```

#### Request headers
| Header | Value |
|--------|-------|
| Authorization | Token {token_value} |
| Content-Type | application/json |


#### Response
If successful, this method returns 200 OK response code and returns the
item  in the response body

#### Example
##### Request
Here is an example of a request.
```json
GET http://{url}/addresses/{id}
Content-type: application/json
```

##### Response
Here is an example of the response.
```json
{
	"id": 1, 
	"name": "address 1", 
	"country": "US", 
	"state": "CA", 
	"city": "Los Angeles", 
	"postal_code": "90210", 
	"address_1": "Beverly Hills", 
	"address_2": "", 
	"phone_number": "", 
	"email": "test_email001@gmail.com"
}
```

### Update Address
Update an address api

#### HTTP request

```bash
PUT http://{url}/addresses/{id}
```

#### Request headers
| Header | Value |
|--------|-------|
| Authorization | Token {token_value} |
| Content-Type | application/json |

#### Request body
In the request body, supply a JSON representation of an items object.

#### Response
If successful, this method returns 200 OK response code and returns the
item  in the response body

#### Example
##### Request
Here is an example of a request.
```json
PUT http://{url}/addresses/{id}
Content-type: application/json

{
	"name": "address 1 updated", 
	"country": "US", 
	"state": "CA", 
	"city": "Los Angeles", 
	"postal_code": "90210", 
	"address_1": "Beverly Hills", 
	"address_2": "apt. 1", 
	"phone_number": "", 
	"email": "test_email001@gmail.com"
}
```

##### Response
Here is an example of the response.
```json
{
	"id": 1, 
	"name": "address 1 updated", 
	"country": "US", 
	"state": "CA", 
	"city": "Los Angeles", 
	"postal_code": "90210", 
	"address_1": "Beverly Hills", 
	"address_2": "apt. 1", 
	"phone_number": "", 
	"email": "test_email001@gmail.com"
}
```

### Delete Address
Delete addresses api

#### HTTP request
Delete single record using id
```bash
DELETE http://{url}/adresses/{id}
```


##### Record delete
##### Request
Here is an example of a request.
```json
DELETE http://{url}/addresses/{id}
Content-type: application/json

```

###### Response
Successful call returns no body in response, just 2xx status code.


## Errors
Errors are signaled with corresponding status code. Some custom errors also may have explanatory text as value in json 
`error` field. 

#### Example
###### Response
```json
{
  "error": "Duplicated address"
}
```
