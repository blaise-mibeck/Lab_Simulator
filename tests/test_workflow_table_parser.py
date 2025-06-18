from lab_simulation.core.workflow_table_parser import parse_workflow_csv, build_workflow_graph

def test_parse_and_graph():
    # Example CSV path
    path = 'example_workflow.csv'
    # Write a sample CSV for testing
    with open(path, 'w', encoding='utf-8') as f:
        f.write('Step Name,Previous Task,Dependencies,Next Task,Task Type,Time (min),Tool/Instrument,Attended,Batch?,Max Batch Size\n')
        f.write('Sample Entry,,,Prep,sample entry,5,,Yes,Yes,20\n')
        f.write('Prep,Sample Entry,,XRF;XRD,sample prep,15,Rock Saw,Yes,Yes,10\n')
        f.write('XRF,Prep,,DataAnalysis,instrument analysis,10,XRF,No,Yes,40\n')
        f.write('XRD,Prep,,DataAnalysis,instrument analysis,60,XRD,No,Yes,20\n')
        f.write('DataAnalysis,XRF;XRD,,Review,data analysis,45,,Yes,Yes,10\n')
        f.write('Review,DataAnalysis,,Report,data review,20,,Yes,Yes,20\n')
        f.write('Report,Review,,,reporting,90,,Yes,Yes,100\n')
    steps = parse_workflow_csv(path)
    assert len(steps) == 7
    graph = build_workflow_graph(steps)
    assert 'Prep' in graph['Sample Entry']
    assert 'XRF' in graph['Prep'] and 'XRD' in graph['Prep']
    print('Parsed steps:', [s.name for s in steps])
    print('Graph:', dict(graph))
