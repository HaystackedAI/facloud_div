import azure.functions as func
from azure.functions import TimerRequest

import logging, requests
from datetime import date

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="http_trigger")
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.function_name(name="daily_dividend_job")
@app.schedule(
    schedule="0 0 20 * * *",  # 09:00 UTC = 04:00 EST
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def daily_dividend_job(timer: TimerRequest):
    url = "https://divapp.fastapicloud.dev/div2pg/div_dailyrun"

    try:
        requests.post(url, timeout=5)  # fire & forget
        logging.info("Daily dividend job triggered")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to trigger daily job: {e}")
