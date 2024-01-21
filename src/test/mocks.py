from fastapi import HTTPException


async def run_model(model_type: str):
    class OutputMock:
        stdout = '{"some": "data"}'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def run_model_for_user(user_id: int):
    class OutputMock:
        stdout = '["data"]'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def run_model_error():
    raise HTTPException(status_code=404, detail="File Not Found")
