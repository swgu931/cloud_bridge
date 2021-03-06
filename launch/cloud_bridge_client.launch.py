#
# LGE Advanced Robotics Laboratory
# Copyright (c) 2020 LG Electronics Inc., LTD., Seoul, Korea
# All Rights are Reserved.
#
# SPDX-License-Identifier: MIT
#
import os
import sys

import launch.actions
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from cloud_bridge_launch_common import *

def generate_launch_description():

    # Set remapping topic list
    remap_topic_list = ['tf', 'tf_static']

    # Set nodename need to modify model with robot_name
    modify_model_node_list = []

    # Get the launch directory
    config_dir = os.path.join(get_package_share_directory("cloud_bridge"), 'config')

    # Get config filename
    config_filename = os.path.join(config_dir, 'client.yaml')
    param_filename = os.path.join(config_dir, 'params.yaml')
    
    # Create our own temporary YAML files that include substitutions
    rewritten_list = ['cloud_ip', 'manage_port']
    configured_params = get_configured_params(config_filename, rewritten_list)

    # Get namespace in argument
    namespace = find_robot_name()
    
    # Set remapping topic tuple list
    remapping_list = set_remapping_list(remap_topic_list)

    # Create environment variables
    stdout_linebuf_envvar = launch.actions.SetEnvironmentVariable(
        'RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1')

    # Create actions nodes
    cloud_trans_client_node = launch_ros.actions.Node(
        package='cloud_bridge',
        node_executable='cloud_bridge_client',
        node_namespace=namespace,
        remappings=remapping_list,
        parameters=[configured_params, param_filename],
        output='screen')

    # Create the launch description and populate
    ld = launch.LaunchDescription()

    ld.add_action(stdout_linebuf_envvar)
    ld.add_action(cloud_trans_client_node)

    return ld
