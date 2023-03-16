"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'disable_user_1' block
    disable_user_1(container=container)
    # call 'disable_tokens_1' block
    disable_tokens_1(container=container)

    return

@phantom.playbook_block()
def disable_user_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("disable_user_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    playbook_input_user = phantom.collect2(container=container, datapath=["playbook_input:user"])

    parameters = []

    # build parameters list for 'disable_user_1' call
    for playbook_input_user_item in playbook_input_user:
        if playbook_input_user_item[0] is not None:
            parameters.append({
                "user_id": playbook_input_user_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("disable user", parameters=parameters, name="disable_user_1", assets=["azure_ad"], callback=join_format_1)

    return


@phantom.playbook_block()
def disable_tokens_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("disable_tokens_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    playbook_input_user = phantom.collect2(container=container, datapath=["playbook_input:user"])

    parameters = []

    # build parameters list for 'disable_tokens_1' call
    for playbook_input_user_item in playbook_input_user:
        if playbook_input_user_item[0] is not None:
            parameters.append({
                "user_id": playbook_input_user_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("disable tokens", parameters=parameters, name="disable_tokens_1", assets=["azure_ad"], callback=join_format_1)

    return


@phantom.playbook_block()
def join_format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("join_format_1() called")

    if phantom.completed(action_names=["disable_user_1", "disable_tokens_1"]):
        # call connected block "format_1"
        format_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_1() called")

    template = """User and tokens have been disabled for user {0}\n"""

    # parameter list for template variable replacement
    parameters = [
        "playbook_input:user"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    format_1 = phantom.get_format_data(name="format_1")

    output = {
        "note_title": ["User Containment"],
        "note_content": format_1,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return