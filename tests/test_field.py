def test_init_size(field):
    assert field.height == 12
    assert field.width == 12


def test_init_base_point(field):
    for line in field.base_point:
        for value in line:
            assert -16 <= value <= 16
            assert isinstance(value, int)


def test_init_status(field):
    for line in field.status:
        for st in line:
            assert st == "*"
