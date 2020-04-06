

import urllib
import quantumflow as qf
from quantumflow.xquirk import quirk_url, circuit_to_quirk

import pytest


def test_circuit_to_quirk():
    # 2-qubit gates

    quirk = "https://algassert.com/quirk#circuit={%22cols%22:[[1,%22X%22,%22%E2%80%A2%22],[%22%E2%80%A2%22,1,%22Z%22],[1,%22%E2%80%A2%22,%22Y%22],[%22Swap%22,1,%22Swap%22]]}"  # noqa: E501
    circ = qf.Circuit([qf.CNOT(2, 1), qf.CZ(0, 2), qf.CY(1, 2), qf.SWAP(0, 2)])
    print()
    print(urllib.parse.unquote(quirk))
    print(quirk_url(circuit_to_quirk(circ)))
    assert urllib.parse.unquote(quirk) == quirk_url(circuit_to_quirk(circ))

    # 3-qubit gates
    quirk = "https://algassert.com/quirk#circuit={%22cols%22:[[%22%E2%80%A2%22,%22%E2%80%A2%22,%22X%22],[%22%E2%80%A2%22,%22%E2%80%A2%22,%22Z%22],[%22%E2%80%A2%22,%22Swap%22,%22Swap%22]]}"  # noqa: E501
    circ = qf.Circuit([qf.CCNOT(0, 1, 2), qf.CCZ(0, 1, 2), qf.CSWAP(0, 1, 2)])
    print()
    print(urllib.parse.unquote(quirk))
    print(quirk_url(circuit_to_quirk(circ)))
    assert urllib.parse.unquote(quirk) == quirk_url(circuit_to_quirk(circ))

    test0 = "https://algassert.com/quirk#circuit={%22cols%22:[[%22Z%22,%22Y%22,%22X%22,%22H%22]]}"  # noqa: E501
    test0 = urllib.parse.unquote(test0)
    circ = qf.Circuit([qf.Z(0), qf.Y(1), qf.X(2), qf.H(3)])
    print(test0)
    print(quirk_url(circuit_to_quirk(circ)))
    assert test0 == quirk_url(circuit_to_quirk(circ))

    test_halfturns = "https://algassert.com/quirk#circuit={%22cols%22:[[%22X^%C2%BD%22,%22Y^%C2%BD%22,%22Z^%C2%BD%22],[%22X^-%C2%BD%22,%22Y^-%C2%BD%22,%22Z^-%C2%BD%22]]}"  # noqa: E501
    test_halfturns = urllib.parse.unquote(test_halfturns)
    circ = qf.Circuit([qf.V(0), qf.SqrtY(1), qf.S(2), qf.V(0).H,
                       qf.SqrtY(1).H, qf.S(2).H])
    print(test_halfturns)
    print(quirk_url(circuit_to_quirk(circ)))
    assert test_halfturns == quirk_url(circuit_to_quirk(circ))

    quarter_turns = "https://algassert.com/quirk#circuit={%22cols%22:[[%22Z^%C2%BC%22],[%22Z^-%C2%BC%22]]}"  # noqa: E501
    s = urllib.parse.unquote(quarter_turns)
    circ = qf.Circuit([qf.T(0), qf.T(0).H])
    assert s == quirk_url(circuit_to_quirk(circ))

    # GHZ circuit
    quirk = "https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22],[1,%22%E2%80%A2%22,%22X%22]]}"  # noqa: E501
    circ = qf.Circuit([qf.H(0), qf.CNOT(0, 1), qf.CNOT(1, 2)])
    print(urllib.parse.unquote(quirk))
    print(quirk_url(circuit_to_quirk(circ)))
    assert urllib.parse.unquote(quirk) == quirk_url(circuit_to_quirk(circ))

    test_formulaic = "https://algassert.com/quirk#circuit={%22cols%22:[[{%22id%22:%22X^ft%22,%22arg%22:%220.1%22},{%22id%22:%22Y^ft%22,%22arg%22:%220.2%22},{%22id%22:%22Z^ft%22,%22arg%22:%220.3%22}],[{%22id%22:%22Rxft%22,%22arg%22:%220.4%22},{%22id%22:%22Ryft%22,%22arg%22:%220.5%22},{%22id%22:%22Rzft%22,%22arg%22:%220.6%22}]]}"  # noqa: E501
    s = urllib.parse.unquote(test_formulaic)
    circ = qf.Circuit([qf.TX(0.1, 0), qf.TY(0.2, 1), qf.TZ(0.3, 2),
                       qf.RX(0.4, 0), qf.RY(0.5, 1), qf.RZ(0.6, 2)])
    assert s == quirk_url(circuit_to_quirk(circ))


def test_fail():
    with pytest.raises(ValueError):
        circ = qf.Circuit([qf.CAN(0.1, 0.2, 0.3)])
        quirk_url(circuit_to_quirk(circ))


def test_url_escape():
    circ = qf.Circuit([qf.X(0)])
    quirk_url(circuit_to_quirk(circ), escape=True)
