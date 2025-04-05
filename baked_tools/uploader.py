import logging
from pathlib import Path

from .lib.shotgrid import SG
from .lib.errors import (
    ProjectNotFoundError, APIKeyNotFoundError, MovieFileNotFoundError,
)


logger = logging.getLogger(__name__)


_sg = None


def _get_sg():
    global _sg

    if _sg is None:
        _sg = SG()
    return _sg


def derive_code(movie_filepath):
    return movie_filepath.stem


def upload_movie(project_id, movie_filepath, is_dry_run):
    movie_filepath = Path(movie_filepath)
    code = derive_code(movie_filepath)
    logger.info(f"Creating version {code} with media at {movie_filepath}.")

    if not movie_filepath.exists():
        raise MovieFileNotFoundError(movie_filepath)

    if not is_dry_run:
        sg = _get_sg()
        shot = sg.create_shot(project_id, code)
        version = sg.create_version(project_id, shot["id"], code)
        sg.upload_version_movie(project_id, version["id"], movie_filepath)
        logger.info("Done.")
    else:
        logger.info("Skipped upload since is_dry_run is true.")

    return code


def upload_movies(project_name, movie_filepaths, is_dry_run):
    try:
        sg = _get_sg()
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

    total_count = len(movie_filepaths)
    for i, path in enumerate(movie_filepaths):
        print(
            f'({i+1}/{total_count}) Uploading media at "{path}"...',
            end="",
            flush=True,
        )

        try:
            code = upload_movie(project_id, path, is_dry_run)
        except MovieFileNotFoundError as e:
            logger.error(e)
            print("\n" + str(e))
            return False
        else:
            print(f".........Created version {code}.\n", end="", flush=True)

    return True
