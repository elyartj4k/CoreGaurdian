from coregaurdian.parser import read_input, find_crashes, extract_call_traces


def test_parse_sample():
    text = open('tests/sample_oops.log','r',encoding='utf-8').read()
    sections = find_crashes(text)
    assert sections, 'Should find at least one crash'
    stacks = extract_call_traces(sections[0][2])
    assert isinstance(stacks, list)