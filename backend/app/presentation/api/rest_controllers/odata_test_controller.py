from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.fetch_odata_data import FetchODataDataUseCase
from app.adapters.api_clients.new_odata_api_client import NewODataAPIClient
import os
import logging

router = APIRouter()

# Dependency Injection
def get_external_service() -> NewODataAPIClient:
    base_url = os.getenv("ODATA_WM_LDI_URL")
    username = os.getenv("CREDENTIALS_USERNAME")
    password = os.getenv("CREDENTIALS_PASSWORD")
    print(f"[get_external_service] Called. base_url={base_url}, username={username}, password={password}")
    client = NewODataAPIClient(url=base_url, username=username, password=password)
    print(f"[get_external_service] NewODataAPIClient instance created: {client}")
    return client

@router.get("/odata_test")
async def odata_test(external_service: NewODataAPIClient = Depends(get_external_service)):
    print("[odata_test] /odata_test endpoint called")
    fetch_data_use_case = FetchODataDataUseCase(api_client=external_service)
    print(f"[odata_test] FetchODataDataUseCase instance created: {fetch_data_use_case}")
    try:
        processed_data = fetch_data_use_case.execute()
        print(f"[odata_test] Data processed and saved successfully: {processed_data}")
        return {"message": "Data processed and saved successfully", "data": processed_data}
    except Exception as e:
        print(f"[odata_test] Error processing OData: {e}")
        logging.error(f"Error processing OData: {e}")
        raise HTTPException(status_code=500, detail="Failed to process OData")

odata_test_controller = router
