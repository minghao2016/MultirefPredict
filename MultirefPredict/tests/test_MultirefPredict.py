"""
Unit and regression test for the MultirefPredict package.
"""

# Import package, test suite, and other packages as needed
import MultirefPredict
import pytest
import sys
import os
from qcelemental.testing import compare_recursive

def test_MultirefPredict_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "MultirefPredict" in sys.modules

def test_diagnostic_factory_B1(qcelemental_water):
    calculator = MultirefPredict.diagnostic_factory("B1", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    B1Thre = 1e-6
    expected = 0.006334860365228678
    assert compare_recursive(diag, expected, atol = B1Thre)

def test_diagnostic_factory_A25PBE(qcelemental_water):
    calculator = MultirefPredict.diagnostic_factory("A25PBE", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    A25PBEThre = 1e-6
    expected = 0.1626572016077259
    assert compare_recursive(diag, expected, atol = A25PBEThre)

def test_diagnostic_factory_TAE(qcelemental_water):
    calculator = MultirefPredict.diagnostic_factory("TAE", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    TAEThre = 1e-6
    expected = 0.28078682517214126
    assert compare_recursive(diag, expected, atol = TAEThre)

def test_diagnostic_factory_CCBased(qcelemental_water):
    Thre = 1e-6
    calculator = MultirefPredict.diagnostic_factory("CCBased", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    expected = {'T1': 0.005903453140867589, 'D1': 0.012965638464472996, 'D2': 0.12885433260716933, 'New D1': 0.012965638464472996}
    print(diag)
    assert compare_recursive(diag, expected, atol = Thre)

def test_diagnostic_factory_T1(qcelemental_water):
    Thre = 1e-6
    calculator = MultirefPredict.diagnostic_factory("T1", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    expected = {'T1': 0.005903453140867589, 'D1': 0.012965638464472996, 'D2': 0.12885433260716933, 'New D1': 0.012965638464472996}
    print(diag)
    assert compare_recursive(diag, expected, atol = Thre)

def test_diagnostic_factory_D1(qcelemental_water):
    Thre = 1e-6
    calculator = MultirefPredict.diagnostic_factory("D1", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    expected = {'T1': 0.005903453140867589, 'D1': 0.012965638464472996, 'D2': 0.12885433260716933, 'New D1': 0.012965638464472996}
    print(diag)
    assert compare_recursive(diag, expected, atol = Thre)

def test_diagnostic_factory_D2(qcelemental_water):
    Thre = 1e-6
    calculator = MultirefPredict.diagnostic_factory("D2", molecule=qcelemental_water)
    diag = calculator.computeDiagnostic()
    expected = {'T1': 0.005903453140867589, 'D1': 0.012965638464472996, 'D2': 0.12885433260716933, 'New D1': 0.012965638464472996}
    print(diag)
    assert compare_recursive(diag, expected, atol = Thre)

