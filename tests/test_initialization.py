from climt import (
    get_default_state)

from sympl import SharedKeyException
import numpy as np
import pytest
from .test_classes import (MockPrognostic,
                           MockPrognosticWithExtraDimensions,
                           MockPrognosticWithExtraQuantities,
                           MockPrognosticWithMalformedExtraQuantities)


def test_no_components():

    with pytest.raises(ValueError) as excinfo:
        get_default_state([])
    assert 'at least one' in str(excinfo.value)


def test_input_state_has_overlapping_keys():

    dummy = MockPrognostic()
    with pytest.raises(SharedKeyException):
        get_default_state([dummy], input_state={'air_temperature': 0})


def test_basic_case_for_two_inputs():

    dummy = MockPrognostic()
    state = get_default_state([dummy])

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['longitude',
                               'latitude',
                                'mid_levels',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities

    assert state['mole_fraction_of_oxygen_in_air'].dims == ('longitude', 'latitude', 'mid_levels')


def test_case_for_x_dim_defined():

    dummy = MockPrognostic()
    state = get_default_state([dummy], x=dict(
        label='along_shore', values=np.linspace(0, 10, 10),
        units='degrees_east'))

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['along_shore',
                               'latitude',
                                'mid_levels',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities

    assert state['air_temperature'].dims == ('along_shore', 'latitude', 'mid_levels')


def test_case_for_y_dim_defined():

    dummy = MockPrognostic()
    state = get_default_state([dummy], y=dict(
        label='along_shore', values=np.linspace(0, 10, 10),
        units='degrees_north'))

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['longitude',
                               'along_shore',
                                'mid_levels',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities

    assert state['air_temperature'].dims == ('longitude', 'along_shore', 'mid_levels')


def test_case_for_z_dim_defined():

    dummy = MockPrognostic()
    state = get_default_state([dummy], z=dict(
        label='along_shore', values=np.linspace(0, 10, 10),
        units='degrees_east'))

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['longitude',
                               'latitude',
                                'along_shore',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities

    assert state['air_temperature'].dims == ('longitude', 'latitude', 'mid_levels')


def test_with_extra_dimensions():

    dummy = MockPrognosticWithExtraDimensions()
    state = get_default_state([dummy], z=dict(
        label='along_shore', values=np.linspace(0, 10, 10),
        units='degrees_east'))

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['longitude',
                               'latitude',
                                'along_shore',
                                'some_other_dimension',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities


def test_with_extra_quantities():

    dummy = MockPrognosticWithExtraQuantities()
    state = get_default_state([dummy], z=dict(
        label='along_shore', values=np.linspace(0, 10, 10),
        units='degrees_east'))

    required_quantities = list(dummy.inputs.keys())
    required_quantities.extend(['longitude',
                               'latitude',
                                'along_shore',
                                'some_quantity',
                                'x',
                                'y',
                                'z'])

    for quantity in state.keys():
        assert quantity in required_quantities


def test_with_malformed_extra_quantity():

    dummy = MockPrognosticWithMalformedExtraQuantities()

    with pytest.raises(ValueError) as excinfo:
        get_default_state([dummy])
    assert 'Malformed' in str(excinfo.value)


def test_different_dimension_units():

    dummy = MockPrognostic()
    with pytest.raises(ValueError) as excinfo:
        get_default_state([dummy], y=dict(
            label='along_shore', values=np.ones((2, 2)),
            units='degrees_north'))
    assert 'must have the same shape' in str(excinfo.value)


if __name__ == '__main__':
    pytest.main([__file__])