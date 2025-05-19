from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.fetch_odata_data import FetchODataData
from app.adapters.api_clients.odata_api_client import ODataAPIClient
import os

router = APIRouter()

# Dependency Injection
def get_external_service() -> ODataAPIClient:
    base_url = os.getenv("ODATA_WM_LDI_URL")
    print(f"Initializing ODataAPIClient with base_url: {base_url}")
    return ODataAPIClient(base_url=base_url)

@router.get("/odata_test")
async def odata_test(external_service: ODataAPIClient = Depends(get_external_service)):
    # Get credentials from environment variables (handled inside execute)
    fetch_data_use_case = FetchODataData(external_service)
    try:
        data = await fetch_data_use_case.execute("")  # Only pass endpoint
        print(f"Data fetched successfully: {data}")
        return data
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

odata_test_controller = router
