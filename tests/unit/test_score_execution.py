#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2024, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import os
import pickle
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd
import pytest
from requests import HTTPError

import sasctl.pzmm as pzmm
from sasctl import current_session
from sasctl.core import RestObj, VersionInfo
from sasctl._services.score_definitions import ScoreDefinitions as sd
from sasctl._services.score_execution import ScoreExecution as se


def test_create_score_execution():
    """
    Test Cases:
    - Valid score definition id?
        -yes
        -no
    - Valid execution id?

    -Valid count key? -> treated like input mapping -> no because i think it's required
    - output table -> treat like input mapping but within the create_score_execution step (do I for library and server in score definition thought?)

    """
    with mock.patch("sasctl.core.Session._get_authorization_token"):
        current_session("example.com", "username", "password")    

    with mock.patch(
        "sasctl._services.score_definitions.ScoreDefinitions.get_definition"
    ) as get_definition:
        with mock.patch(
            "sasctl._services.score_execution.ScoreExecution.get_execution"
        ) as get_execution:
            with mock.patch(
                "sasctl._services.score_execution.ScoreExecution.delete_execution"
            ) as delete_execution:
                with mock.patch(
                   "sasctl._services.score_execution.ScoreExecution.post" 
                ) as post:
                    get_definition.return_value.status_code = 404
                    with pytest.raises(HTTPError):
                        se.create_score_execution(
                            score_definition_id="12345",
                        )
                    get_definition.return_value.status_code = 200
                    get_execution.return_value.status_code = 400 #we might need a separate try except here to show that 404 statement is weird and should exit the program
                    with pytest.raises(HTTPError):
                        se.create_score_execution(
                            score_definition_id="12345",
                        )
                    #stdout or pytest.raises but without ending program?
                
                #pytest.skip()
                # raise HTTP error?
