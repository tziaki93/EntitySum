# EntitySum

EntitySum is a framework for summarizing entities .  

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tziaki93/EntitySum.git
   cd EntitySum

Install the required libraries:

pip install -r requirements.txt

Setup
1. Configure Paths

Make sure to update all paths in your configuration files and scripts.

2. Remove Old Results file

Before running experiments, clear previous results:

rm -rf results.txt runs/*


3. Setup Virtuoso

Install and configure OpenLink Virtuoso.


4. Upload the LMDB Knowledge Graph

Load the LMDB KG located in:EntitySum-main/data


After setup, run the main pipeline scripts. Example:

python main.py

