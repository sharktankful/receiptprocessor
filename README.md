# Receipt Processor Web Service Instructions

To begin using the receipt processor (API Webservice) to take your JSON RECEIPT and return an ID and point total at the specific endpoints, just follow the directions in the instructions below.

***NOTE***: ***BEFORE READING THE INSTRUCTIONS, THESE ARE THE TWO ENDPOINTS FOR THE API LISTED BELOW (I'LL ALSO RESTATE THEM IN THE INSTRUCTIONS)***

- ***ENDPOINT JSON OBJECT ID:*** ```http://localhost:8000/receipts/process```
- ***ENDPOINT FOR RECEIPT OBJECT POINTS:*** ```http://localhost:8000/receipts/{id}/points```

INSTRUCTIONS:
1. Make sure you have Docker installed on your system and that it's running in the background
 
2. Go over to my GitHub repository which contains all of the Django project files, including the Dockerfile in the link provided.(https://github.com/sharktankful/receiptprocessor)
 
3. Once the repository has been downloaded, using the command line of your choice, navigate to the root folder of the repository to create a docker image. ***This will install all the needed dependencies and software to run the service***.
   
6. Run this command in the terminal to create the image: ```docker build -t your-image-name .```
   - ***Replace 'your-image-name' with the name of your choice***
   
   - ***MAKE SURE NOT TO REMOVE THE  '.'  AT THE END!!!***

8. Once the image is built, run this command to activate a Docker container from it: ```docker run -p 8000:8000 your-image-name``` .
9. Your Docker container should be running and you'll have access to your API web service from http://localhost:8000
     -To close your server hit ***'CRTL+C'***.
10. To send a submit a JSON receipt (HTTP Response) in a separate command line (But in the same directory) you can either use the curl command listed below or another method of your choice.
    - ```curl -X POST -H "Content-Type: application/json" -d '{YOUR JSON RECEIPT GOES HERE}' http://localhost:8000/receipts/process/```
11. The command line will send you back a unique JSON ID object
12. With the JSON ID, append the unique ID to the ```http://localhost:8000/receipts/{id}/points``` endpoint and the URL will direct you to a JSON Object containing the total points calculated from the receipt based on the set criteria.
    - Replace the curly braces in ***"{id}"*** and insert the unique ID generated for your JSON Receipt. Example: ```http://localhost:8000/receipts/2516d050-bc08-4bb4-966a-98f45d18bb13/points```
