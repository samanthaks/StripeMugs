# Project 1

### Design
All requirements implemented and work as expected. Live at http://flask-env.ewci6eha2v.us-west-2.elasticbeanstalk.com/

Our stack is Flask for back-end, Jinja for templating, DynamoDB for storage, flask_jwt_extended for auth, and Stripe for payments.

We have a few architectural improvements that we will implement moving forwards such as:
- Splitting routes into /services and /client
- Running each service as an independent application process
- Placing the DB query code in the connector rather than the services



### Developing
```bash
virtualenv venv
source venv/bin/activate
pip install -r config/requirements.txt
python run.py
```


### Team
- Raymond Xu, rx2125
- Eunice Kokor, eek2138
- Samantha Stultz, sks2200
- Jake Kwon, jk3655
- Michelle Lu, ml3720