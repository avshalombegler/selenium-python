from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
import allure

if TYPE_CHECKING:
    from pages.base.page_manager import PageManager
    from logging import Logger


@allure.feature("Digest Authentication")
@allure.story("Verify Digest Authentication scenarios")
@pytest.mark.usefixtures("page_manager")
class TestDigestAuth:
    """Tests for Digest Authentication scenarios"""

    @pytest.mark.parametrize(
        "username, password",
        [
            ("admin", "admin"),
            ("wrong", "admin"),
            ("admin", "wrong"),
        ],
    )
    @pytest.mark.full
    @allure.severity(allure.severity_level.NORMAL)
    def test_digest_auth_login_scenarios(
        self, page_manager: PageManager, logger: Logger, username: str, password: str
    ) -> None:
        logger.info("Tests for Digest Authentication scenarios.")
        page = page_manager.get_digest_auth_page(username, password)

        logger.info("Check if login succeeded.")
        success = page.is_login_successful()
        if not success:
            logger.info(f"Page source: {page.get_page_source_snippet()}")
