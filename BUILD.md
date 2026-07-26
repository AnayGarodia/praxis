# Build notes (Ubuntu 22.04)

```
sudo apt-get update
sudo apt-get install -y cmake libboost-all-dev libgmp-dev nauty python3-pip
pip3 install python-sat
git clone https://github.com/markirch/sat-modulo-symmetries
cd sat-modulo-symmetries
git checkout 464f12f1fd36b496e7ba9dcbb622b079de02dce4
# apply sms_gmp_link.patch if the plain build fails to link (undefined gmp
# symbols); it adds to src/CMakeLists.txt:
#   target_link_libraries(smsg PRIVATE sms_static gmp gmpxx)
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGLASGOW=ON && cmake --build build -j
# binary: build/src/smsg  (install to ~/.local/bin)
```

The Glasgow subgraph solver is required (forbidden-subgraph propagators).

Sanity check after building (should output exactly 1 graph, then 0 graphs):

```
python3 encode.py 13 5 --no-indep -o /tmp/t13.cnf
smsg --vertices 13 --all-graphs --dimacs /tmp/t13.cnf \
  --forbidden-subgraph-file data/forb_k3.txt \
  --forbidden-induced-subgraph-file data/forb_i5.txt   # forb_i5: file "5"
```

File formats (validated empirically: the (3,5;13) and (3,7;22) enumerations
reproduce the known counts 1 and 191 exactly with these files):
- forb_k3.txt: `3 0 1 1 2 0 2` — an edge-list line (edge count, then vertex
  pairs) describing the triangle K3, forbidden as a (not necessarily induced)
  subgraph.
- forb_i10.txt / forb_i9.txt / forb_i5.txt: a single integer `N` — forbids an
  independent set of size N when passed to --forbidden-induced-subgraph-file.
Use the copies in data/ unchanged (sha256s in STATUS.md / the coordinator
message).

kissat + drat-trim (for the DRAT replay stage):

```
git clone https://github.com/arminbiere/kissat && cd kissat && ./configure && make
git clone https://github.com/marijnheule/drat-trim && cd drat-trim && make
```
