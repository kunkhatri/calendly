# my-calendly
A calendly like app server with basic capabilites to set, get and find overlapping availabilities for users. 

## APIs
### Add User
```
Path: POST /user
Accept: application/json
Example request data:
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
