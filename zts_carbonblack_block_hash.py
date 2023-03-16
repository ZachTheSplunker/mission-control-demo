"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'block_hash_1' block
    block_hash_1(container=container)

    return

@phantom.playbook_block()
def block_hash_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("block_hash_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    playbook_input_hash = phantom.collect2(container=container, datapath=["playbook_input:hash"])

    parameters = []

    # build parameters list for 'block_hash_1' call
    for playbook_input_hash_item in playbook_input_hash:
        if playbook_input_hash_item[0] is not None:
            parameters.append({
                "hash": playbook_input_hash_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("block hash", parameters=parameters, name="block_hash_1", assets=["carbon black"], callback=format_1)

    return


@phantom.playbook_block()
def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_1() called")

    template = """The Hash has been blocked by Carbon Black Successfully: {0}\n"""

    # parameter list for template variable replacement
    parameters = [
        "block_hash_1:action_result.parameter.hash"
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
        "note_title": ["Hash Containment"],
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