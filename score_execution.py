import requests

from pathlib import Path
import json
from typing import Union

from sasctl import Session
#from sasctl._services.cas_management import CASManagement as cas
from .score_definition import ScoreDefinitions as sd
from .service import Service

class ScoreExecutions(Service):
    """
    The Score Execution API is used to produce a score by 
    executing the mapped code generated by score objects using the score definition.
    
    See Also
    --------
    `REST Documentation <https://developers.sas.com/rest-apis/scoreExecution-v2>`
    """
    
    _SERVICE_ROOT = "/scoreExecution"
    
    list_executions, get_execution, update_execution, delete_execution = Service._crud_funcs(
        "/executions", "execution")

@classmethod
def score_execution(cls, score_definition_id: str,  description: str = "", output_server_name: str = "cas-shared-default", output_library_name: str = "Public", output_table_name: str = ""):
    """Creates the score definition service.
     
    Parameters
    --------
    score_definition_id: str
        A score definition id representing score definition existing on the server that needs to be executed.
    description: str, optional
        Description of score execution. Defaults to an empty string.
    output_server_name: str, optional
        The name of the output server the output table and output library is stored in. Defaults to "cas-shared-default".
    output_library_name: str, optional
        The name of the output library the output table is stored in. Defaults to "Public".
    output_table_name: str, optional
        The name of the output table the score execution or analysis output will be stored in. Defaults to an empty string.
    
    Returns
    -------
    RestObj

    """

    try:
        score_definition = sd.get_definition(score_definition_id)
        score_exec_name = score_definition.json()["name"]
        model_uri = score_definition.json()["objectDescriptor"]["uri"]
        model_name = score_definition.json()["objectDescriptor"]["name"]
        model_input_library = score_definition.json()["inputData"]["libraryName"]
        model_input_server = score_definition.json()["inputData"]["serverName"]
        model_table_name = score_definition.json()["inputData"]["tableName"]
    except:
        raise Exception('The score definition may not exist.')
    # Gets information about the scoring object from the score definition and raises an exception if the score definition does not exist
            
    if output_table_name == "":
        output_table_name = f"{model_name}_{score_definition_id}"
    # Defining a default output table name
    try:
        score_execution = sess.get(f"/scoreExecution/executions?filter=eq(scoreExecutionRequest.scoreDefinitionId,%27{score_definition_id}%27)") # how to use crud functions on something with such a specifc filter
        execution_count = score_execution.json()['count']
        if execution_count == 1:
            execution_id = score_execution.json()["items"][0]["id"]
            deleted_score_execution = cls.delete_execution(execution_id)
            print(deleted_score_execution)
    except:
        print("There may not be a score execution already running.")
    
    # Deleting any score executions that are already executing the same score definition

    headers_score_exec = {
    "Content-Type": "application/json"
    }

    create_score_exec = {"name": score_exec_name,
            "description": description,
            "hints": {"objectURI":model_uri,
                      "inputTableName":model_table_name,
                      "inputLibraryName": model_input_library},
            "scoreDefinitionId": score_definition_id,
            "outputTable": {"tableName": output_table_name,
                            "libraryName": output_library_name,
                            "serverName": output_server_name}}
    
    # Creating the score execution
    
    new_score_execution = cls.post("scoreExecution/executions", data=json.dumps(create_score_exec), headers=headers_score_exec)
    return new_score_execution            