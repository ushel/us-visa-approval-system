# us-visa-approval-system

'''bash

git add .

git commit -m "updated"

git push origin master

'''

# How to run?

'''bash
conda update -n base -c defaults conda

conda create -n visa python=3.8 -y

conda activate visa

pip install -r requirements.txt
'''

#Workflow
1. Constant
2. Config -> entity
3. Artifact -> entity
4. Component
5. Pipeline
6. app.py ->Endpoint


git bash... to set env variables

export MONGODB_URL = ""
export AWS_ACCESS_KEY_ID ="AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY ="AWS_SECRET_ACCESS_KEY"

instead of demo.py have to run app.py to predict.