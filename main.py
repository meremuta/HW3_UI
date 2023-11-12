import json
import ydb
import os
import pandas as pd

driver_config = ydb.DriverConfig(
    endpoint=os.getenv("YDB_ENDPOINT"),
    database=os.getenv("YDB_DATABASE"),
    credentials=ydb.iam.MetadataUrlCredentials()
)

driver = ydb.Driver(driver_config)
# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

def upsert_userinfo(uid, username, email, password):
    text = f"UPSERT INTO userinfo (`id`, `username`, `email`, `password`) VALUES ( '{uid}', '{username}', '{email}', '{password}') ;"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def select_userinfo(uid):
    text = f"SELECT * FROM  userinfo WHERE `id`== '{uid}';"
    user_data_ydb = pool.retry_operation_sync(
        lambda s: s.transaction().execute(
            text,
            commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
        )
    )
    user_data = pd.DataFrame.from_records(user_data_ydb[0].rows)
    return user_data



def handler (event, context):
    response = json.loads(json.dumps(event))
    method = response['httpMethod']
    if method == 'POST':
        try:
            username = response['queryStringParameters']['username']
            email = response['queryStringParameters']['login']
            password = response['queryStringParameters']['password']
            uid = response['headers']['X-Envoy-External-Address']
            upsert_userinfo(uid, username, email, password)
            result = "Succesfully updated"
        except:
            result = 'Something is wrong with parameters'
    else:
        try:
            uid = response['headers']['X-Envoy-External-Address']
            userdata = select_userinfo(uid)
            uname = str(userdata["username"][0])
            result = uname
        except:
            result = 'Something is wrong with address'
        


    print(event)
    return {"statusCode": 200,
    "body": result
    }