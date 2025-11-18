from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Files Upload")
@allure.story("Tests Files Upload functionality")
@pytest.mark.usefixtures("page_manager")
class TestFilesUpload:
    """Tests Files Upload functionality"""

    TEST_FILES_DIR = Path(__file__).parent / "files"

    FILES_NAMES = [
        "audio-first.mp3",
        "CATE-CHAPTER_1-QUALITY.ppt",
        "Company_Portal_Installer.exe",
        "Screenshot_2025-11-16_at_9.23.28_PM.png",
        "test1.json",
        "TestingFile.pdf",
    ]

    @pytest.mark.full
    @pytest.mark.ui
    @pytest.mark.parametrize("filename", FILES_NAMES)
    @allure.severity(allure.severity_level.NORMAL)
    def test_files_upload_functionality(self, page_manager: PageManager, logger: Logger, filename: str) -> None:
        logger.info("Tests Files Upload.")
        page = page_manager.get_file_upload_page()

        file_path = str(self.TEST_FILES_DIR / filename)

        logger.info("Upload file using the Upload button.")
        page.select_file_to_upload(file_path)
        file_uploaded_page = page.click_upload_file()

        logger.info("Verifying file uploaded sucessfully.")
        assert file_uploaded_page.get_uploaded_file_name() == filename
