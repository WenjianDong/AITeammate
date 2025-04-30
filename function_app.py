import azure.functions as func
import logging
import os
from openai import OpenAI

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    project_description = req_body.get('project_description')

    # Construct prompt
    prompt = f"""
    I'm working on this personal project: {project_description}. 
    Please give me some encouraging words to stay motivated and accomplish it.
    Please following the output format: a timestamp of every 15 minutes, with some encouraging words. 
    Example:
    0 hour 15 min: <some encouraging words>
    0 hour 30 min: <some encouraging words>
    0 hour 45 min: <some encouraging words>
    1 hour 0 min: <some encouraging words>
    1 hour 15 min: <some encouraging words>
    ...

    Please generate 12 encouragement. 
    """

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )
    response.output_text
  

    if response.output_text:
        return func.HttpResponse(response.output_text)
    else:
        return func.HttpResponse(
             "This HTTP triggered the function, but some error happened when executing function app.",
             status_code=200
        )