import numpy as np

test_reports = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("input_2", 'r') as f:
    reports = f.readlines()

safe_report = 0
for line in reports:#test_reports.split('\n'):
    #print(line)
    line_diff = np.diff(list(map(int, line.split())))
    if (np.abs(line_diff) < 1).any() or (np.abs(line_diff) > 3).any() or not (np.sign(line_diff) == np.sign(line_diff)[0]).all():
        pass#print("  fail")
    else:
        #print("  safe")
        safe_report += 1

print(f"# of safe reports: {safe_report}")

safe_report = 0
for line in reports:#test_reports.split('\n'):
    #print(line)
    report = np.array(list(map(int, line.split())))
    line_diff = np.diff(report)
    if ((np.abs(line_diff) < 1).any() 
        or (np.abs(line_diff) > 3).any() 
        or not ((np.sign(line_diff) == np.sign(line_diff)[0])).all()):
        #print("  fail")
        dampener = 0
        for _ in range(len(report)):
            idx = np.zeros_like(report)
            idx[_] = 1
            diff = np.diff(report[np.invert(idx.astype(bool))])
            if ((np.abs(diff) < 1).any() 
                or (np.abs(diff) > 3).any() 
                or not ((np.sign(diff) == np.sign(diff)[0])).all()):
                pass
            else:
                dampener += 1
        if dampener:
            #print("    safe with dampener")
            safe_report += 1
    else:
        #print("  safe")
        safe_report += 1

print(f"# of safe reports accounting for dampener: {safe_report}")
