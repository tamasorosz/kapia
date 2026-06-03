import json

from kapia import RunArchive


def test_archive_logs_evaluation(tmp_path):
    archive = RunArchive(tmp_path / "run")
    archive.save_metadata()
    archive.log_evaluation(
        design={"x": 1.0},
        objectives={"loss": 2.0},
        constraints={"temperature": -5.0},
    )

    evaluations = archive.evaluations_path.read_text(encoding="utf-8").splitlines()
    assert len(evaluations) == 1

    record = json.loads(evaluations[0])
    assert record["design"]["x"] == 1.0
    assert record["objectives"]["loss"] == 2.0
    assert record["constraints"]["temperature"] == -5.0
