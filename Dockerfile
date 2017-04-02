# neuronunit
# author Rick Gerkin rgerkin@asu.edu

FROM scidash/neuron-mpi-neuroml

# Make neuronunit source directory in Travis image visible to Docker.
USER root
ADD . $HOME/neuronunit
RUN chown -R $NB_USER $HOME 
WORKDIR $HOME/neuronunit 

# Install neuronunit and dependencies.
RUN python setup.py install

# Run all unit tests.
ENTRYPOINT python -m unittest unit_test/test_*.py
