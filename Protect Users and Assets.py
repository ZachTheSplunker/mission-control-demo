"""
Choose which artifacts to protect.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_values' block
    get_values(container=container)

    return

@phantom.playbook_block()
def get_values(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_values() called")

    get_values__md5 = None
    get_values__incident_id = None
    get_values__user = None
    get_values__device = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    mc_container = phantom.get_container(container['id'])
    get_values__incident_id = mc_container['external_id']
    mc_summary_data = mc_container['data']['summary']
    if isinstance(mc_summary_data, str):
        mc_summary_data = json.loads(mc_summary_data)
    get_values__md5 = mc_summary_data.get('MD5')
    get_values__user = mc_summary_data.get('user')
    get_values__device = mc_summary_data.get('dest')

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_values:md5", value=json.dumps(get_values__md5))
    phantom.save_run_data(key="get_values:incident_id", value=json.dumps(get_values__incident_id))
    phantom.save_run_data(key="get_values:user", value=json.dumps(get_values__user))
    phantom.save_run_data(key="get_values:device", value=json.dumps(get_values__device))

    get_tasks(container=container)
    join_format_1(container=container)

    return


@phantom.playbook_block()
def get_tasks(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_tasks() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    location_formatted_string = phantom.format(
        container=container,
        template="""/incidents/{0}/tasks""",
        parameters=[
            "get_values:custom_function:incident_id"
        ])

    get_values__incident_id = json.loads(_ if (_ := phantom.get_run_data(key="get_values:incident_id")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    if location_formatted_string is not None:
        parameters.append({
            "location": location_formatted_string,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="get_tasks", assets=["mission_control"], callback=get_task_data)

    return


@phantom.playbook_block()
def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    body_formatted_string = phantom.format(
        container=container,
        template="""{{\"title\": \"{0}\", \"content\": {1}}}\n""",
        parameters=[
            "playbook_zts_carbonblack_block_hash_1:playbook_output:note_title",
            "playbook_zts_carbonblack_block_hash_1:playbook_output:note_content"
        ])

    playbook_zts_carbonblack_block_hash_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_block_hash_1:playbook_output:note_title"])
    playbook_zts_carbonblack_block_hash_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_block_hash_1:playbook_output:note_content"])
    get_task_data__urls = json.loads(_ if (_ := phantom.get_run_data(key="get_task_data:urls")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'post_data_1' call
    for playbook_zts_carbonblack_block_hash_1_output_note_title_item in playbook_zts_carbonblack_block_hash_1_output_note_title:
        for playbook_zts_carbonblack_block_hash_1_output_note_content_item in playbook_zts_carbonblack_block_hash_1_output_note_content:
            if get_task_data__urls is not None:
                parameters.append({
                    "body": body_formatted_string,
                    "location": get_task_data__urls,
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []
    playbook_zts_carbonblack_block_hash_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_block_hash_1:playbook_output:note_title"])
    playbook_zts_carbonblack_block_hash_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_block_hash_1:playbook_output:note_content"])
    playbook_zts_carbonblack_block_hash_1_output_note_title_values = [item[0] for item in playbook_zts_carbonblack_block_hash_1_output_note_title]
    playbook_zts_carbonblack_block_hash_1_output_note_content_values = [item[0] for item in playbook_zts_carbonblack_block_hash_1_output_note_content]
    data = []
    for title, content in zip(playbook_zts_carbonblack_block_hash_1_output_note_title_values, playbook_zts_carbonblack_block_hash_1_output_note_content_values):
        
        data.append({
            "title": title,
            "content": content
        })

    if get_task_data__urls is not None:
        for url in get_task_data__urls:
            for item in data:
                parameters.append({
                    "body": json.dumps(item),
                    "location": url,
                })
    phantom.debug(parameters)
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_1", assets=["mission_control"])

    return


@phantom.playbook_block()
def playbook_zts_carbonblack_block_hash_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_zts_carbonblack_block_hash_1() called")

    data_summary_file_hash_value = container.get("data", {}).get("summary", {}).get("file_hash", None)
    get_values__md5 = json.loads(_ if (_ := phantom.get_run_data(key="get_values:md5")) != "" else "null")  # pylint: disable=used-before-assignment

    hash_combined_value = phantom.concatenate(data_summary_file_hash_value, get_values__md5, dedup=True)

    inputs = {
        "hash": hash_combined_value,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "mission-control-demo/zts_carbonblack_block_hash", returns the playbook_run_id
    playbook_run_id = phantom.playbook("mission-control-demo/zts_carbonblack_block_hash", container=container, name="playbook_zts_carbonblack_block_hash_1", callback=post_data_1, inputs=inputs)

    return


@phantom.playbook_block()
def get_task_data(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_task_data() called")

    get_tasks_result_data = phantom.collect2(container=container, datapath=["get_tasks:action_result.data.*.parsed_response_body"], action_results=results)
    get_values__incident_id = json.loads(_ if (_ := phantom.get_run_data(key="get_values:incident_id")) != "" else "null")  # pylint: disable=used-before-assignment

    get_tasks_result_item_0 = [item[0] for item in get_tasks_result_data]

    get_task_data__urls = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    playbook_info = phantom.get_playbook_info()
    current_playbook_name = playbook_info[0]['name']
    get_task_data__urls = []
    for task in get_tasks_result_item_0[0]:
        suggestions = task.get('suggestions', {})
        playbooks = suggestions.get('playbooks', [])
        for playbook in playbooks:
            if playbook['name'] == current_playbook_name:
                get_task_data__urls.append(f"/incidents/{get_values__incident_id}/responseplans/{task['response_plan_id']}/phase/{task['phase_id']}/tasks/{task['id']}/notes")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_task_data:urls", value=json.dumps(get_task_data__urls))

    join_format_1(container=container)

    return


@phantom.playbook_block()
def playbook_zts_azure_disable_user_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_zts_azure_disable_user_1() called")

    get_values__user = json.loads(_ if (_ := phantom.get_run_data(key="get_values:user")) != "" else "null")  # pylint: disable=used-before-assignment

    user_combined_value = phantom.concatenate(get_values__user, dedup=True)

    inputs = {
        "user": user_combined_value,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "mission-control-demo/zts_azure_disable_user", returns the playbook_run_id
    playbook_run_id = phantom.playbook("mission-control-demo/zts_azure_disable_user", container=container, name="playbook_zts_azure_disable_user_1", callback=post_data_2, inputs=inputs)

    return


@phantom.playbook_block()
def playbook_zts_carbonblack_contain_asset_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_zts_carbonblack_contain_asset_1() called")

    get_values__device = json.loads(_ if (_ := phantom.get_run_data(key="get_values:device")) != "" else "null")  # pylint: disable=used-before-assignment

    device_combined_value = phantom.concatenate(get_values__device, dedup=True)

    inputs = {
        "device": device_combined_value,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "mission-control-demo/zts_carbonblack_contain_asset", returns the playbook_run_id
    playbook_run_id = phantom.playbook("mission-control-demo/zts_carbonblack_contain_asset", container=container, name="playbook_zts_carbonblack_contain_asset_1", callback=post_data_3, inputs=inputs)

    return


@phantom.playbook_block()
def join_format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("join_format_1() called")

    if phantom.completed(action_names=["get_tasks"]):
        # call connected block "format_1"
        format_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_1() called")

    template = """Choose which artifacts to contain.\n\nUser: {0}\n\nDevice: {1}\n\nHash: {2}"""

    # parameter list for template variable replacement
    parameters = [
        "get_values:custom_function:user",
        "get_values:custom_function:device",
        "get_values:custom_function:md5"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    protect_prompt(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["protect_prompt:action_result.summary.responses.0", "==", "Yes"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        playbook_zts_carbonblack_block_hash_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["protect_prompt:action_result.summary.responses.1", "==", "Yes"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        playbook_zts_azure_disable_user_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_3() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["protect_prompt:action_result.summary.responses.2", "==", "Yes"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        playbook_zts_carbonblack_contain_asset_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def post_data_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    body_formatted_string = phantom.format(
        container=container,
        template="""{{\"title\": \"{0}\", \"content\": {1}}}""",
        parameters=[
            "playbook_zts_azure_disable_user_1:playbook_output:note_title",
            "playbook_zts_azure_disable_user_1:playbook_output:note_content"
        ])

    playbook_zts_azure_disable_user_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_azure_disable_user_1:playbook_output:note_title"])
    playbook_zts_azure_disable_user_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_azure_disable_user_1:playbook_output:note_content"])
    get_task_data__urls = json.loads(_ if (_ := phantom.get_run_data(key="get_task_data:urls")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'post_data_2' call
    for playbook_zts_azure_disable_user_1_output_note_title_item in playbook_zts_azure_disable_user_1_output_note_title:
        for playbook_zts_azure_disable_user_1_output_note_content_item in playbook_zts_azure_disable_user_1_output_note_content:
            if get_task_data__urls is not None:
                parameters.append({
                    "body": body_formatted_string,
                    "location": get_task_data__urls,
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []
    playbook_zts_azure_disable_user_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_azure_disable_user_1:playbook_output:note_title"])
    playbook_zts_azure_disable_user_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_azure_disable_user_1:playbook_output:note_content"])
    playbook_zts_azure_disable_user_1_output_note_title_values = [item[0] for item in playbook_zts_azure_disable_user_1_output_note_title]
    playbook_zts_azure_disable_user_1_output_note_content_values = [item[0] for item in playbook_zts_azure_disable_user_1_output_note_content]
    data = []
    for title, content in zip(playbook_zts_azure_disable_user_1_output_note_title_values, playbook_zts_azure_disable_user_1_output_note_content_values):
        
        data.append({
            "title": title,
            "content": content
        })

    if get_task_data__urls is not None:
        for url in get_task_data__urls:
            for item in data:
                parameters.append({
                    "body": json.dumps(item),
                    "location": url,
                })
    phantom.debug(parameters)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_2", assets=["mission_control"])

    return


@phantom.playbook_block()
def post_data_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    body_formatted_string = phantom.format(
        container=container,
        template="""{{\"title\": \"{0}\", \"content\": {1}}}""",
        parameters=[
            "playbook_zts_carbonblack_contain_asset_1:playbook_output:note_title",
            "playbook_zts_carbonblack_contain_asset_1:playbook_output:note_content"
        ])

    playbook_zts_carbonblack_contain_asset_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_contain_asset_1:playbook_output:note_title"])
    playbook_zts_carbonblack_contain_asset_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_contain_asset_1:playbook_output:note_content"])
    get_task_data__urls = json.loads(_ if (_ := phantom.get_run_data(key="get_task_data:urls")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'post_data_3' call
    for playbook_zts_carbonblack_contain_asset_1_output_note_title_item in playbook_zts_carbonblack_contain_asset_1_output_note_title:
        for playbook_zts_carbonblack_contain_asset_1_output_note_content_item in playbook_zts_carbonblack_contain_asset_1_output_note_content:
            if get_task_data__urls is not None:
                parameters.append({
                    "body": body_formatted_string,
                    "location": get_task_data__urls,
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []
    playbook_zts_carbonblack_contain_asset_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_contain_asset_1:playbook_output:note_title"])
    playbook_zts_carbonblack_contain_asset_1_output_note_content = phantom.collect2(container=container, datapath=["playbook_zts_carbonblack_contain_asset_1:playbook_output:note_content"])
    playbook_zts_carbonblack_contain_asset_1_output_note_title_values = [item[0] for item in playbook_zts_carbonblack_contain_asset_1_output_note_title]
    playbook_zts_carbonblack_contain_asset_1_output_note_content_values = [item[0] for item in playbook_zts_carbonblack_contain_asset_1_output_note_content]
    data = []
    for title, content in zip(playbook_zts_carbonblack_contain_asset_1_output_note_title_values, playbook_zts_carbonblack_contain_asset_1_output_note_content_values):
        
        data.append({
            "title": title,
            "content": content
        })

    if get_task_data__urls is not None:
        for url in get_task_data__urls:
            for item in data:
                parameters.append({
                    "body": json.dumps(item),
                    "location": url,
                })
    phantom.debug(parameters)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_3", assets=["mission_control"])

    return


@phantom.playbook_block()
def protect_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("protect_prompt() called")

    # set user and message variables for phantom.prompt call

    user = None
    role = "mc_analyst_all_edit"
    message = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "format_1:formatted_data"
    ]

    # responses
    response_types = [
        {
            "prompt": "Block Hash",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No"
                ],
            },
        },
        {
            "prompt": "Disable User",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No"
                ],
            },
        },
        {
            "prompt": "Quarantine Device",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No"
                ],
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=70, name="protect_prompt", parameters=parameters, response_types=response_types, callback=protect_prompt_callback)

    return


@phantom.playbook_block()
def protect_prompt_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("protect_prompt_callback() called")

    
    decision_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    decision_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    decision_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return