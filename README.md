# StripeMugs

### Developing
```bash
virtualenv venv
source venv/bin/activate
pip install -r config/requirements.txt
python run.py
```



### Spec

1. Sign up for a Stripe test account (one per team).

2. Implement three simple pages:
  - Logon to your projects customer server (UID/password),
  - Get a list of “things” for which you can pay,
  - Simulated credit card transaction via Stripe,
  - Result flows from UI to your servers,

3. Three simple serverless/microservices:
  - (Gateway) Validate the credit card token/info,
  - (User) Verify UID/PW; record customer payment,
  - (Payments) Update payment records,

4. Integrate into an end-to-end flow

5. As-A-Service platforms:
  - Amazon S3 for web site,
  - One:
    - Service on Elastic Beanstalk,
    - Table/DB in Aurora,
    - You may use local servers for the others,

  - JWT token between:
    - UI,
    - User service,

  - Basic REST API, but do not need to use API Gateway (yet).