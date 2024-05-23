import pytest


@pytest.mark.parametrize("threshold", [10**7, 1.5 * 10**7, 5 * 10**7, 10**8, 5 * 10**8, 10**9, 1.5 * 10**9])
def test_website_popularity(website_data, threshold):
    failed_websites = []
    for website in website_data:
        if website.visitors_per_month < threshold:
            failed_websites.append(
                f"{website.name} (Frontend:{website.frontend}|Backend:{website.backend}) "
                f"has {website.visitors_per_month} unique visitors per month. (Expected more than {threshold})"
            )

    if failed_websites:
        pytest.fail("\n".join(failed_websites))


if __name__ == "__main__":
    pytest.main()
