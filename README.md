# Ticket-Selling
Ticket selling web application using Django, Django Rest Framework, Celery and Redis.

# API Reference
## Tickets App
### Base URL: 
`tickets/api/`
### APIs
* create and event: 
  * URL: 
   `/events`  
  * example data:  
    `{         
        'name': 'Expo',            
        'date': '2021-06-29T12:00:00Z',       
        'address': 'dubai'        
    }`       
  * method: POST
* list of events: 
  * URL: 
          `/events`
  * method: GET
* create ticket type for an event: 
  * URL: 
   `/events/<evnet_pk>/ticket-types`  
  * example data:  
    `{
            'quantity': 40,
            'name': 'Economic',
            'price': 10,
            'event': 1,
     }`       
  * method: POST
* ticket type list of an event: 
  * URL: 
          `/events/<evnet_pk>/ticket-types`
  * method: GET
* reserve a ticket for an event: 
  * URL: 
   `/events/<evnet_pk>/ticket-types/<pk>/tickets`  
  * example data:  
    `{
            'ticket_type': 1,
     }`       
  * method: POST
* ticket list of an event: 
  * URL: 
          `/events/<evnet_pk>/ticket-types/<pk>/tickets`
  * method: GET
 
## Users App
### Base URL: 
 `users/api/`
### APIs
* register a user: 
  * URL: 
   `/register`  
  * example data:  
    `{
            'username': 'john_doe',
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'john@example.com',
            'password': '123456'
     }`       
  * method: POST

## Payment App 
### Base URL: 
`payment/api/`
### APIs
* pay for a ticket: 
  * URL: 
   `/<pk>/pay`  
  * example data:  
    `{
        'ticket_id': 1, 
        'amount': 20,
        'currency': 'EUR',
        'token': 'card_info_customer_info_order_info'
     }`       
  * method: POST

