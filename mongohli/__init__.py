import logging
from sh import mongocli
import os
import azure.functions as func
import tempfile

# 'function pointers to mongocli top-level commands'
supported_commands ={ "iam" : mongocli.iam,
                      "config" : mongocli.config,
                      "atlas" : mongocli.atlas
}

def help(msg):
    help = """
mongohli:mongocli hosted over http
Usage:
curl http://::/api/mongohli?iam%20projects%20
runs 'mongocli iam projects list'
"""
    return f"Message:{msg}\n{help}"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('mongohli:hosted mongocli')
    command = req.params.get('command')
    logging.info(f"command:{command}")
    if command:
        commands = command.split()
        logging.info(f"commands:{commands}")
        try:
           req_body = req.get_json()
           if len(req_body):
               logging.info(f"req_body:{req_body}")
               fp = tempfile.TemporaryFile()
               fp.write(b'{req_body}')
               commands.append("--file")
               commands.append(fp.name)
               logging.info(f"wrote request body to {fp.name}")
               fp.close()
        except Exception as err:
            logging.error(f"{err}")
        try:
            result = supported_commands.get( commands[0] )(commands[1:])
            logging.info(f"result={result}")
            return func.HttpResponse(f"{result}")
        except Exception as err:
            return func.HttpResponse(f"{err}", status_code=500)

    else:
        msg = "monohli:command not found"
        return func.HttpResponse(
             help(msg),
             status_code=200
        )


pubkey = os.environ.get("ATLAS_PUBLIC_KEY","XXX")
pvtkey = os.environ.get("ATLAS_PRIVATE_KEY","YYY")
orgidkey = os.environ.get("ATLAS_ORG_ID","ZZZ")
logging.info(f"pubkey={pubkey}, pvtkey={pvtkey}, orgidkey={orgidkey}")
r = mongocli.config("set","public_api_key",pubkey)
logging.info(f"set pubkey:{r}")
r = mongocli.config("set","private_api_key",pvtkey)
logging.info(f"set pvtkey:{r}")
#r = mongocli.config("set","org_id",orgidkey)
#logging.info(f"set org_id:{r}")

