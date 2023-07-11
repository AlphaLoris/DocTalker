import sys
import trace
from main import main  # Assuming main() is your entry function in your 'main' module

# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=1,
    count=1)

# run the new command using the given tracer
tracer.run('main()')

# Get the results
r = tracer.results()

# Open your file in write mode
with open(r"C:\Users\glenn\OneDrive\Desktop\Agg_DocTalker_code\Agg_DocTalker_code.py", "w") as f:
    # Redirect the standard output to your file
    sys.stdout = f
    # Write the results to the file
    r.write_results(show_missing=True)
