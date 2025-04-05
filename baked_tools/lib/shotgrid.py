import os
import logging

import shotgun_api3

from .errors import ProjectNotFoundError, APIKeyNotFoundError


logger = logging.getLogger(__name__)


API_KEY_ENV_VAR_NAME = "SHOTGRID_API_KEY"

_HOSTNAME = "https://baked.shotgunstudio.com"
_SCRIPT_NAME = "baked-tools"


class SG:
    def __init__(self, hostname=_HOSTNAME, api_key=None):
        self._hostname = hostname

        try:
            self._api_key = (
                api_key or os.environ[API_KEY_ENV_VAR_NAME]
            )
        except KeyError as e:
            raise APIKeyNotFoundError(API_KEY_ENV_VAR_NAME) from e

        self._api = shotgun_api3.Shotgun(
            self._hostname,
            script_name=_SCRIPT_NAME,
            api_key=self._api_key,
        )

    def list_all_projects(self):
        return self._api.find("Project", [], ["id", "name"])

    def resolve_project_id(self, name):
        projects = { p["name"].lower(): p for p in self.list_all_projects() }

        if name.lower() not in projects:
            raise ProjectNotFoundError(
                name, list(p["name"] for p in projects.values()),
            )

        return projects[name.lower()]["id"]

    def list_shots(self, project_id):
        return self._api.find(
            "Shot",
            [["project", "is", { "type": "Project", "id": project_id }]],
            [
                "id",
                "cached_display_name",
                "project",
                "code",
                "sg_status_list",
                "sg_turnover_notes",
                "sg_delivery_notes",
                "created_at",
                "created_by",
                "updated_at",
                "updated_by",
                "description",
                "sg_latest_version",
                "sg_versions",
                "version_sg_link_to_shot_versions",
                "user",
            ],
        )

    def list_versions(self, project_id):
        return self._api.find(
            "Version",
            [["project", "is", { "type": "Project", "id": project_id }]],
            [
                "id",
                "cached_display_name",
                "project",
                "code",
                "created_at",
                "created_by",
                "updated_at",
                "updated_by",
                "description",
                "sg_link_to_shot",
                "sg_uploaded_movie",
                "user",
            ]
        )

    def create_shot(self, project_id, code):
        logger.info(f"Creating shot {code} for project {project_id}.")

        data = {
            "project": { "type": "Project", "id": project_id },
            "code": code,
        }
        return self._api.create("Shot", data)

    def create_version(self, project_id, shot_id, code):
        logger.info(f"Creating version {code} for project {project_id}.")

        data = {
            "project": { "type": "Project", "id": project_id },
            "code": code,
            "description": "source",
            "entity": { "type": "Shot", "id": shot_id },
        }
        return self._api.create("Version", data)

    def upload_version_movie(self, project_id, version_id, movie_filepath):
        logger.info(f"Uploading movie.")

        self._api.upload(
            "Version",
            version_id,
            movie_filepath,
            field_name="sg_uploaded_movie",
        )

