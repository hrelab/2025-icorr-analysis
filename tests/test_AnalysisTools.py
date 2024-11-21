from analysis_tools.PatientDataExtractor import get_subjects


def test_get_subjects():
    assert len(get_subjects("../proc_data")) == 12
