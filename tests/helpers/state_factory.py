def make_state(**overrides) -> dict:
    """
    Docstring for make_state

    :param overrides: Description
    :return: Description
    :rtype: dict[Any, Any]
    """

    base: dict = {
        "jd_text": "JD",
        "master_cv": {"profile": {"title": "Data Scientist"}, "experience": [], "projects": [], "skills_pool": {}},
        "analysis": {"tech_keywords": [], "soft_keywords": [], "role_focus": ""},
        "error": None,
    }
    base.update(overrides)
    return base
