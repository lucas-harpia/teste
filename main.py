import uvicorn
import time
from fastapi import FastAPI
from routes.api import router as api_router

def create_app() -> FastAPI:
    current_app = FastAPI(title="Plugin de dados - CNPJ",
                          description="",
                          version="1.0.0", )

    current_app.include_router(api_router)
    return current_app

app = create_app()


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8089,
                log_level="info", reload=True)
    print("running")
