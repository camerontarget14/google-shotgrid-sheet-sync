from datetime import datetime
import logging

from .lib.shotgrid import SG
from .lib.errors import (
    ProjectNotFoundError, APIKeyNotFoundError
)

import gspread


SERVICE_ACCOUNT_JSON_KEYFILE_PATH = "./service_account.json"


logger = logging.getLogger(__name__)


def _load_gsheet():
    try:
        g = gspread.service_account(filename=SERVICE_ACCOUNT_JSON_KEYFILE_PATH)
    except FileNotFoundError as e:
        print("Could not find service account JSON keyfile.")
        print(f"Expected to find file at path: {SERVICE_ACCOUNT_JSON_KEYFILE_PATH}")
        return None

    return g


def _update_spreadsheet(project_name, shots):
    g = _load_gsheet()
    if not g:
        return

    spreadsheet_name = f"{project_name}_Baked_Live_Tracking"

    logging.info(f"Updating spreadsheet {spreadsheet_name}...")

    try:
        spreadsheet = g.open(spreadsheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet not found: {spreadsheet_name}", file=sys.stderr)
        sys.exit(1)

    sheet_name = 'Sheet2'
    worksheet = spreadsheet.worksheet(sheet_name)

    # Clear the existing data from the worksheet
    worksheet.clear()

    # Populate the Google Sheet with the ShotGrid data
    header_row = [
        "Code",
        "Description",
        "Status",
        "Turnover Notes",
        "Delivery Notes",
    ]
    worksheet.append_row(header_row)

    for shot in shots:
        row = [
            shot["code"],
            shot["description"],
            shot["sg_status_list"],
            shot["sg_turnover_notes"],
            shot["sg_delivery_notes"],
        ]
        worksheet.append_row(row)

    # Add a timestamp to the bottom of the data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row(
        ["", "", "", "", "", "", f"Last updated on {timestamp}"]
    )


def sync(project_name):
    logger.info("Fetching shots from Shotgrid...")

    try:
        sg = SG()
    except APIKeyNotFoundError as e:
        logger.error(e)
        print("Could not find API key.")
        print(f"You must set specify you API key using the environment variable: {e.env_var_name}.")
        return False

    try:
        project_id = sg.resolve_project_id(project_name)
    except ProjectNotFoundError as e:
        logger.error(e)
        print(f'Could not find a project named "{e.project_name}".')
        print("Here are the available projects:")
        for p in sorted(e.existing_projects):
            print(f"- {p}")

        return False

    shots = sg.list_shots(project_id)

    logger.info("Updating spreadsheet...")
    _update_spreadsheet(project_name, shots)
    logger.info("Done.")
