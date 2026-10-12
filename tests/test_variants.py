import pytest

from jev_zoo.adapters import Mock
from jev_zoo.storage import write_json
from jev_zoo.tasks import synthetic
from jev_zoo.variants import Variants


def test_rotation_keeps_ids_and_gold_outside_inference():
    e = synthetic()[0]
    original = e.inference_payload()
    adapter = Variants(Mock({}), {}, rotations=3)
    r = adapter.predict(e.request)
    r.validate_against(e.request)
    assert r.answers[0].selected_option_id == str(e.request.state["selected"])
    assert e.inference_payload() == original
    assert r.forward_count == 0


def test_temperature_is_checkpoint_bound(tmp_path):
    artifact = tmp_path / "cal.json"
    write_json(
        artifact, {"partition": "calibration", "checkpoint_revision": "old", "temperature": 2}
    )
    with pytest.raises(ValueError):
        Variants(Mock({}), {"revision": "new"}, calibration=artifact)
