import json
import os
from datetime import datetime, timedelta
from services.acquisition_service import AcquisitionService
from db_connection.MongoDBConnection import MongoDBConnection

import requests

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

LIST_API = "http://e-licitatie.ro/api-pub/DirectAcquisitionCommon/GetDirectAcquisitionList/"
VIEW_API = "http://e-licitatie.ro/api-pub/PublicDirectAcquisition/getView/"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://e-licitatie.ro/pub/notices/contract-notices/list/0/0"
}
headers_view = {
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://e-licitatie.ro/pub/notices/contract-notices/list/0/0"
}

PAGE_SIZE = 20


def get_body(fin_start, fin_end, page_index):
    return json.dumps({
        "pageSize": PAGE_SIZE,
        "showOngoingDa": False,
        "cookieContext": None,
        "pageIndex": page_index,
        "sysDirectAcquisitionStateId": 7,
        "publicationDateStart": None,
        "publicationDateEnd": None,
        "finalizationDateStart": f"{fin_start}",
        "finalizationDateEnd": f"{fin_end}",
    })


def get_acquisition(item, view_data):
    item['publicationDate'] = datetime.strptime(item['publicationDate'], "%Y-%m-%dT%H:%M:%S%z")
    item['finalizationDate'] = datetime.strptime(item['finalizationDate'], "%Y-%m-%dT%H:%M:%S%z")
    acquisition_data = {
        "name": item['directAcquisitionName'],
        "description": view_data['directAcquisitionDescription'],
        "identification_code": item['uniqueIdentificationCode'],
        "aquisition_id": f"{item['directAcquisitionId']}",
        "publication_date": item['publicationDate'],
        "finalization_date": item['finalizationDate'],
        "cpv_code_id": view_data['cpvCode']['id'],
        "cpv_code_text": item['cpvCode'],
    }
    return acquisition_data


def get_items(view_data):
    items_data = []
    for i in range(len(view_data['directAcquisitionItems'])):
        float_quantity = float(view_data['directAcquisitionItems'][i]['itemQuantity'])
        float_closing_price = float(view_data['directAcquisitionItems'][i]['itemClosingPrice'])
        cpv_locale = view_data['directAcquisitionItems'][i]['cpvCode']['localeKey']
        cpv_text = view_data['directAcquisitionItems'][i]['cpvCode']['text']
        cpv_code_text = f"{cpv_locale} - {cpv_text}"
        items_data.append({
            "name": view_data['directAcquisitionItems'][i]['catalogItemName'],
            "description": view_data['directAcquisitionItems'][i]['catalogItemDescription'],
            "unit_type": view_data['directAcquisitionItems'][i]['itemMeasureUnit'],
            "quantity": float_quantity,
            "closing_price": float_closing_price,
            "cpv_code_id": view_data['directAcquisitionItems'][i]['cpvCode']['id'],
            "cpv_code_text": cpv_code_text,
        })
    return items_data


def get_start_end_dates():
    start_time = datetime.strptime("2024-01-03", "%Y-%m-%d")
    end_time = datetime.strptime("2024-01-03", "%Y-%m-%d")
    return start_time, end_time


def main():
    finalization_date_start, finalization_date_end = get_start_end_dates()
    page_index = 0
    has_more_data = True
    print(f"Getting data for {finalization_date_start} - {finalization_date_end}")

    while has_more_data:
        body = get_body(finalization_date_start, str(finalization_date_end), str(page_index))
        response = requests.post(LIST_API, headers=headers, data=body)

        if response.status_code == 200:
            data = response.json()
            print(f"Page {page_index + 1}: {len(data.get('items', []))} items")
            for item in data.get("items", []):
                    print(item['sysDirectAcquisitionState']['id'])
                    url_view = f"{VIEW_API}{item['directAcquisitionId']}"
                    view_response = requests.get(url_view, headers=headers_view)
                    if view_response.status_code == 200:
                        view_data = view_response.json()
                        acquisition_data = get_acquisition(item, view_data)
                        items_data = get_items(view_data)
                        acquisition = AcquisitionService.create_acquisition_with_items(acquisition_data, items_data)
                    else:
                        print(f"Error: {view_response.status_code}")
            if len(data.get('items', [])) == 0:
                has_more_data = False
            else:
                page_index += 1
        else:
            print(f"Error: {response.status_code}")
            has_more_data = False


if __name__ == "__main__":
    db_connection = MongoDBConnection(env_file=ENV_FILE_PATH)
    db_connection.connect()
    main()
    db_connection.disconnect()
