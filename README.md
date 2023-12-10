# my-calendly
A calendly like app server with basic capabilites to set, get and find overlapping availabilities for users. 

## APIs
### Add User
```
path: POST /user
accept: application/json
example request data:
{
    "name": "Neha Agarwal",
    "organization": "Paytm",
    "timezone": "Asia/Kolkata",
    "working_days": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
}
```
### Get User Availability
```
path: GET user/<user_id>/get_availabilityfilter={"type": "NAME", "value": "CURRENT_MONTH"}
query params:
  name: filter
  type: json
filter schema:
  type: NAME
  value: TODAY | TOMORROW | CURRENT_WEEK | NEXT_WEEK | CURRENT_MONTH
```
### Set User Availability
```
path: POST /user/<user_id>/set_availability
accept: application/json
example request data:
{
    "availability_slots": {
        "type": "PER_DATE",
        "dates_slots": [
            {
            "date": "2023-12-11",
            "slots": [[10, 11], [11, 12], [16, 17], [17, 18]]
            }
        ]
    }
}
```
### Get Overlapping Available Slots For Two Users
```
path: GET /user/<user_id1>/overlapping_slots/<user_id2>?filter={"type": "NAME", "value": "CURRENT_MONTH"}
query params:
  name: filter
  type: json
filter schema:
  type: NAME
  value: TODAY | TOMORROW | CURRENT_WEEK | NEXT_WEEK | CURRENT_MONTH
```
### Book Available Slots (To be implemented)
```
path: POST /user/<user_id1>/book_slots
```
### Remove Available Slots (To be implemented)
```
path: POST /user/<user_id1>/remove_availability
```
