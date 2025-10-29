import pytest
import allure
from pages.base.page_manager import PageManager


@allure.feature("Digest Authentication")
@allure.story("Verify Digest Authentication scenarios")
@pytest.mark.usefixtures("page_manager")
class TestDigestAuth:
    """Tests Digest Authentication scenarios"""

    @pytest.mark.parametrize(
        "username, password",
        [
            ("admin", "admin"),
            ("wrong", "admin"),
            ("admin", "wrong"),
        ],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_digest_auth_login_scenarios(self, page_manager: PageManager, logger, username, password):
        page = page_manager.get_digest_auth_page(username, password)

        success = page.is_login_successful()
        if not success:
            logger.info(f"Page source: {page.get_page_source_snippet()}")
