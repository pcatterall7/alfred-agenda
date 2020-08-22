#!/usr/bin/python
# encoding: utf-8

"""
Defines queries and execution functions for calling the Bear sqlite DB.
"""

import sqlite3
import os

DB_LOCATION = (
    "/Library/Group Containers/WRBK2Z2EG7.group.com.momenta.agenda.macos/"
    "Release/Application/DerivedInfo/UI Database/UIDatabase.db")
DB_KEY = 'db_path'

NOTES_BY_TITLE = (
    "SELECT "
    "   ZIDENTIFIER, ZTITLE, ZPROPERTIES "
    "FROM ZSECTION "
    "WHERE "
    "   lower(ZTITLE) like lower('%{0}%') "
    "ORDER BY ZSTARTDATE desc"
)

PROJECTS_BY_TITLE = (
    "SELECT "
    "   ZIDENTIFIER, ZTITLE "
    "FROM ZDOCUMENT "
    "WHERE "
    "   (Z_OPT != 2 OR ZISHIDDEN != 1) "
    "   AND lower(ZTITLE) LIKE lower('%{0}%')"
)

NOTES_BY_PROJECT_TITLE = (
    "SELECT DISTINCT"
    "   n.ZIDENTIFIER, n.ZTITLE, n.ZPROPERTIES "
    "FROM "
    "   ZSECTION n "
    "   LEFT JOIN ZDOCUMENT p ON n.ZSTOREIDENTIFIER = p.ZSTOREIDENTIFIER "
    "WHERE "
    "   lower(p.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   n.ZSTARTDATE DESC")

def search_notes_by_title(workflow, log, query):
    """
    Searches for Agenda notes by the title of the note.
    """

    sql_query = NOTES_BY_TITLE.format(query)
    return run_query(workflow, log, sql_query)

def search_projects_by_title(workflow, log, query):
    """
    Searches for Agenda projects by project name.
    """

    sql_query = PROJECTS_BY_TITLE.format(query)
    return run_query(workflow, log, sql_query)

def search_notes_by_project_title(workflow, log, query):
    """
    Searches for Agenda notes by project name.
    """

    sql_query = NOTES_BY_PROJECT_TITLE.format(query)

    return run_query(workflow, log, sql_query)


def run_query(workflow, log, sql):
    """
    Takes a SQL command, executes it, and returns the results.
    """

    db_path = workflow.stored_data(DB_KEY)
    if not db_path:
        db_path = find_agenda_db(log)
        workflow.store_data(DB_KEY, db_path)
    else:
        log.debug(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    log.debug(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    log.debug("Found {0} results".format(len(results)))
    cursor.close()
    return results

def find_agenda_db(log):
    """
    Finds the Agenda sqlite3 DB.
    """

    home = os.path.expanduser("~")
    db_file = "{0}{1}".format(home, DB_LOCATION)
    if not os.path.isfile(db_file):
        log.debug(
            "Agenda db not found at {0}".format(db_file))

    log.debug(db_file)
    return db_file
