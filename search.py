#!/usr/bin/python
# encoding: utf-8

"""
Main search script for alfred-bear workflow.
"""

import sys
import argparse
import queries
from workflow import Workflow, ICON_SYNC

TITLE = "i"
PROJECT = "p"

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"

LOGGER = None

# Update workflow from GitHub repo
UPDATE_SETTINGS = {'github_slug': 'chrisbro/alfred-bear'}
SHOW_UPDATES = True


def main(workflow):
    """
    I'm just here so I don't get fined by pylint
    """

    if SHOW_UPDATES and workflow.update_available:
        workflow.add_item('A new version is available',
                          'Action this item to install the update',
                          autocomplete='workflow:update',
                          icon=ICON_SYNC)

    LOGGER.debug('Started search workflow')
    args = parse_args()

    if args.query:
        query = args.query[0]
        LOGGER.debug("Searching notes for %s", format(query))
        execute_search_query(args)

    workflow.send_feedback()


def parse_args():
    """
    Parses out the arguments sent to the script in the Alfred workflow.
    """

    parser = argparse.ArgumentParser(description="Search Agenda Notes")
    parser.add_argument('-t', '--type', default=TITLE,
                        choices=[TITLE, PROJECT],
                        type=str, help='What to search for: t(i)tle, or (p)roject?')
    parser.add_argument('query', type=unicode,
                        nargs=argparse.REMAINDER, help='query string')

    LOGGER.debug(WORKFLOW.args)
    args = parser.parse_args(WORKFLOW.args)
    return args


def execute_search_query(args):
    """
    Decides what search to run based on args that were passed in and executes the search.
    """
    query = None
    if args.query:
        query = args.query[0]
        query = query.encode('utf-8')

        if SINGLE_QUOTE in query:
            query = query.replace(SINGLE_QUOTE, ESC_SINGLE_QUOTE)

    if args.type == PROJECT:
        LOGGER.debug('Searching projects')
        query = query.replace('#', '')
        project_results = queries.search_projects_by_title(WORKFLOW, LOGGER, query)
        if not project_results:
            WORKFLOW.add_item('No search results found.')
        else:
            for project_result in project_results:
                LOGGER.debug(project_result)
                WORKFLOW.add_item(title=project_result[1], subtitle="Open tag",
                                  arg=project_result[0], valid=True)
            #TODO: show notes within the project too
            # for note_result in note_results:
            #     LOGGER.debug(note_results)
            #     note_arg = ':n:' + note_result[0]
            #     WORKFLOW.add_item(title=note_result[1], subtitle="Open note",
            #                       arg=note_arg, valid=True)

    else:
        LOGGER.debug('Searching notes')
        title_results = queries.search_notes_by_title(WORKFLOW, LOGGER, query)
        if not title_results:
            WORKFLOW.add_item('No search results found.')
        else:
            note_ids = []
            for title_result in title_results:
                LOGGER.debug(title_result)
                WORKFLOW.add_item(title=title_result[1], subtitle="Open note", arg=title_result[0], valid=True)
                note_ids.append(title_result[0])


if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
