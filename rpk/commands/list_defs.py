#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The 'list-defs' command for rpk."""

import sys
from rpk.common import Colors, get_skill_definitions


def add_list_defs_parser(subparsers):
    """Add the 'list-defs' subparser to the argument parser."""
    list_defs_parser = subparsers.add_parser(
        "list-defs", help="List available skill definitions"
    )
    return list_defs_parser


def run_list_defs(args):
    """Execute the 'list-defs' command."""
    try:
        data = get_skill_definitions()
    except Exception as e:
        print(f"{Colors.RED}Error:{Colors.RESET} {e}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}{Colors.CYAN}Available Skill Definitions:{Colors.RESET}")
    
    # Sort skills by ID for consistent output
    skills = sorted(data.get('skills', []), key=lambda x: x.get('id', ''))
    
    for skill in skills:
        skill_id = skill.get('id', 'unknown')
        description = skill.get('description', '').split('\n')[0] # First line of desc
        print(f" - {Colors.GREEN}{skill_id}{Colors.RESET}: {description}")
    print()
