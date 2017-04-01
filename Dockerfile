# neuronunit
# author Rick Gerkin rgerkin@asu.edu

FROM scidash/neuron-mpi-neuroml

USER root
RUN chown -R $NB_USER . 
USER $NB_USER

RUN python setup.py install
ENTRYPOINT python -m unittest test_*.py
WORKDIR $WORKDIR