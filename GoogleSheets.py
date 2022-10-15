import oauth2client
import oauthlib
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


#для парсинга таблицы гугловской с базой вопросов и ответов, если не установлена изначально
def get_service_sacc(filename):
    creds_json=filename
    scopes=['https://www.googleapis.com/auth/spreadsheets']
    creds_service=ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)
def prepare_file(filename, gtoken):
    resp=get_service_sacc(filename).spreadsheets().values().batchGet(spreadsheetId=gtoken, ranges=["FAQ.xlsx"]).execute()
    new=resp.get("valueRanges")[0].get("values")[1::]
    file=open('FAQ11.csv', 'w')
    file.write("questions,"+'"answers"'+'\n')
    for item in new:
        if(item[0]!="questions,"):
            file.write('"'+item[0]+'","'+item[1]+'"\n')
    file.close()