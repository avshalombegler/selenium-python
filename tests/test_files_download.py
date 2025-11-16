from __future__ import annotations
from typing import TYPE_CHECKING
import os
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger
    from pathlib import Path


@allure.feature("Files Download")
@allure.story("Tests Files Download functionality")
@pytest.mark.usefixtures("page_manager")
class TestFilesDownload:
    """Tests Files Download functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @pytest.mark.clean_downloads
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skipif(
        os.getenv("BROWSER") == "firefox",
        reason="Skipping file download test for Firefox due to slow downloading process",
    )
    def test_files_download_functionality(
        self, page_manager: PageManager, logger: Logger, downloads_directory: Path
    ) -> None:
        logger.info("Tests Files Download.")
        page = page_manager.get_file_download_page()

        logger.info("Getring list of downloadable files.")
        file_names = page.get_list_of_downloadable_files()

        logger.info("Downloading all files in page.")
        for file_name in file_names:
            page.download_file_by_filename(file_name)

        logger.info("Verifying downloaded files count equals to files in page.")
        assert len(file_names) == len(page.get_number_of_downloaded_files(downloads_directory))
