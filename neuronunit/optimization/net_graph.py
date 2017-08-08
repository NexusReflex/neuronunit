
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import graphviz

import matplotlib as mpl
# setting of an appropriate backend.
try:
    mpl.use('Qt5Agg') # Need to do this before importing neuronunit on a Mac, because OSX backend won't work
except:
    mpl.use('Agg')

from plotly.graph_objs import *
import matplotlib.pyplot as plt
import numpy as np



def plotly_graph(history,vmhistory):
    from networkx.drawing.nx_agraph import graphviz_layout
    import plotly
    import plotly.plotly as py
    import networkx as nx
    import networkx
    G = networkx.DiGraph(history.genealogy_tree)
    G = G.reverse()
    labels = {}
    for i in G.nodes():
        labels[i] = i
    node_colors = np.log([ np.sum(history.genealogy_history[i].fitness.values) for i in G ])
    positions = graphviz_layout(G, prog="dot")

    dmin=1
    ncenter=0
    for n in positions:
        x,y=positions[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

    for edge in G.edges():
        source = G.nodes()[edge[0]-1]
        target = G.nodes()[edge[1]-1]

        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            #colorscale='YIGnBu',
            colorscale='Hot',

            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Genes summed error (absence of fitness)',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():

        x,y = positions[G.nodes()[node-1]]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    for k, node in enumerate(G):
        node_trace['marker']['color'].append(node_colors[k])
        try:
            node_info = 'gene id: {0} threshold current {1} pA model attributes {2}'.format( str(int(k)), str(vmhistory.rheobase), str(vmhistory[k].attrs))
        except:
            node_info = 'gene id: {0} threshold currrent {1} pA model attributes {2} pA '.format( str(int(k)), str(vmhistory.rheobase), str(vmhistory[k].attrs))
        node_trace['text'].append(node_info)

    fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Geneeology History made with NeuronUnit/DEAP optimizer outputing into networkx and plotly',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='the code this derives from.' \
                    https://github.com/russelljjarvis/neuronunit/blob/dev/neuronunit/optimization/net_graph.py#L470-L569</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    py.sign_in('RussellJarvis','FoyVbw7Ry3u4N2kCY4LE')
    py.iplot(fig, filename='networkx.svg',image='svg')



def best_worst(history):
    '''
    Query the GA's DEAP history object to get the worst candidate ever evaluated.

    inputs DEAP history object
    best output should be the same as the first index of the ParetoFront list (pf[0]).
    outputs best and worst candidates evaluated.
    '''
    import numpy as np
    badness = [ np.sum(ind.fitness.values) for ind in history.genealogy_history.values() if ind.fitness.valid ]
    maximumb = np.max(badness)
    minimumb = np.min(badness)
    history_dic = history.genealogy_history
    worst = []
    best = []
    # there may be multiple best and worst candidates, just take the first ones found.
    for k,v in history_dic.items():
        if np.sum(v.fitness.values) == maximumb:
            worst.append(v)
        if np.sum(v.fitness.values) == minimumb:
            best.append(v)
    return best[0], worst[0]

def pca(final_population,vmpop,td):
    import plotly
    import plotly.plotly as py
    from plotly.graph_objs import Scatter, Marker, Line, Data, Layout, Figure, XAxis, YAxis
    from sklearn.preprocessing import StandardScaler
    X_std = StandardScaler().fit_transform(pop)
    from sklearn.decomposition import PCA as sklearnPCA
    sklearn_pca = sklearnPCA(n_components=10)
    Y_sklearn = sklearn_pca.fit_transform(X_std)
    '''
    points = []
    proj0 = []
    proj1 = []

    for ind in final_population:
        proj0.append(ind * Y_sklearn[:,0])
        proj1.append(ind * Y_sklearn[:,1])
    '''
    x_points = [ ind * Y_sklearn[:,0] for ind in final_population ]
    y_points = [ ind * Y_sklearn[:,1] for ind in final_population ]

    iter_list = list(zip(x_points,y_points))

    #for counter,ind in enumerate(final_population):
    for k,v in enumerate(Y_sklearn):
        #print(Y_sklearn[k,0])
        x=Y_sklearn[k,0] #Component 1
        y=Y_sklearn[k,1] #Component 2
        print(x,y,td[k])

        point = Scatter(
        x=Y_sklearn[k,0], #Component 1
        y=Y_sklearn[k,1], #Component 2
        mode='markers',
        name = str(final_pop[counter])+str(td[k]),
        marker=Marker(
            size=12,
            line=Line(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5),
            opacity=0.8))
        points.append(point)

    data = Data(points)
    layout = Layout(xaxis=XAxis(title='PC1', showline=True),
                    yaxis=YAxis(title='PC2', showline=True))
    fig = Figure(data=data, layout=layout)
    py.iplot(fig)
    py.sign_in('RussellJarvis','FoyVbw7Ry3u4N2kCY4LE')
    py.iplot(fig, filename='improved_names.svg',image='svg')


def plot_evaluate(vms_best,vms_worst,names=['best','worst']):#This method must be pickle-able for ipyparallel to work.
    '''
    A method to plot the best and worst candidate solution waveforms side by side


    Inputs: An individual gene from the population that has compound parameters, and a tuple iterator that
    is a virtual model object containing an appropriate parameter set, zipped togethor with an appropriate rheobase
    value, that was found in a previous rheobase search.

    Outputs: This method only has side effects, not datatype outputs from the method.
    The most important side effect being a plot in eps format.

    '''
    import os
    from neuronunit.models import backends
    from neuronunit.models.reduced import ReducedModel
    import quantities as pq
    import numpy as np
    import get_neab
    from itertools import repeat
    vmslist = [vms_best, vms_worst]
    import copy
    tests = copy.copy(get_neab.tests)
    for k,v in enumerate(tests):
        import matplotlib.pyplot as plt
        plt.clf()
        plt.style.use('ggplot')
        stored_min = []
        stored_max = []
        sc_for_frame_best = []
        sc_for_frame_worst = []
        for iterator, vms in enumerate(vmslist):
            new_file_path = str(get_neab.LEMS_MODEL_PATH)+str(os.getpid())
            model = ReducedModel(new_file_path,name=str('vanilla'),backend='NEURON')
            #model.load_model()
            assert type(vms.rheobase) is not type(None)
            #tests = get_neab.suite.tests
            #model.update_run_params(vms.attrs)

            if k == 0:
                v.prediction = {}
                v.prediction['value'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['duration'] = 1000 * pq.ms
                v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['delay'] = 100 * pq.ms
                print(v.prediction)
            if k != 0:
                v.prediction = None

            if k == 1 or k == 2 or k == 3:
                # Negative square pulse current.
                v.params['injected_square_current']['duration'] = 100 * pq.ms
                v.params['injected_square_current']['amplitude'] = -10 *pq.pA
                v.params['injected_square_current']['delay'] = 30 * pq.ms
            if k == 5 or k == 6 or k == 7:
                # Threshold current.
                v.params['injected_square_current']['duration'] = 1000 * pq.ms
                v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['delay'] = 100 * pq.ms
            import neuron
            model.reset_h(neuron)
            model.load_model()
            model.update_run_params(vms.attrs)
            print(v.params)
            score = v.judge(model,stop_on_error = False, deep_error = True)
            if iterator == 0:
                sc_for_frame_best.append(score)
            else:
                sc_for_frame_worst.append(score)


            plt.plot(model.results['t'],model.results['vm'],label=str(v)+str(names[iterator])+str(score))
            plt.xlim(0,float(v.params['injected_square_current']['duration']) )
            stored_min.append(np.min(model.results['vm']))
            stored_max.append(np.max(model.results['vm']))
            plt.ylim(np.min(stored_min),np.max(stored_max))
            plt.tight_layout()
            model.results = None
            plt.ylabel('$V_{m}$ mV')
            plt.xlabel('mS')
        plt.savefig(str('test_')+str(v)+'vm_versus_t.eps', format='eps', dpi=1200)
        import pandas as pd
        sf_best = pd.DataFrame(sc_for_frame_best)
        sf_worst = pd.DataFrame(sc_for_frame_worst)



def shadow(not_optional_list,best_vm):#This method must be pickle-able for ipyparallel to work.
    '''
    A method to plot the best and worst candidate solution waveforms side by side


    Inputs: An individual gene from the population that has compound parameters, and a tuple iterator that
    is a virtual model object containing an appropriate parameter set, zipped togethor with an appropriate rheobase
    value, that was found in a previous rheobase search.

    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import os
    from neuronunit.models import backends
    from neuronunit.models.reduced import ReducedModel
    import quantities as pq
    import numpy as np
    import get_neab
    from itertools import repeat

    color='lightblue'
    not_optional_list.append(best_vm)

    import copy
    tests = copy.copy(get_neab.tests)
    for k,v in enumerate(tests):
        import matplotlib.pyplot as plt
        plt.clf()
        plt.style.use('ggplot')
        stored_min = []
        stored_max = []
        sc_for_frame_best = []
        sc_for_frame_worst = []

        #if index == plot_count - 1:

        for iterator, vms in enumerate(not_optional_list):

            if vms is not_optional_list[-1]:
                color = 'blue'
            if iterator == len(not_optional_list):
                color = 'blue'

            #new_file_path = str(get_neab.LEMS_MODEL_PATH)+str(os.getpid())
            model = ReducedModel(get_neab.LEMS_MODEL_PATH,name=str('vanilla'),backend='NEURON')
            assert type(vms.rheobase) is not type(None)
            if k == 0:
                v.prediction = {}
                v.prediction['value'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['duration'] = 1000 * pq.ms
                v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['delay'] = 100 * pq.ms
                print(v.prediction)
            if k != 0:
                v.prediction = None

            if k == 1 or k == 2 or k == 3:
                # Negative square pulse current.
                v.params['injected_square_current']['duration'] = 100 * pq.ms
                v.params['injected_square_current']['amplitude'] = -10 *pq.pA
                v.params['injected_square_current']['delay'] = 30 * pq.ms
            if k==0 or k ==4 or k == 5 or k == 6 or k == 7:
                # Threshold current.
                v.params['injected_square_current']['duration'] = 1000 * pq.ms
                v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
                v.params['injected_square_current']['delay'] = 100 * pq.ms
            import neuron
            model.reset_h(neuron)
            model.load_model()
            model.update_run_params(vms.attrs)
            print(v.params)
            score = v.judge(model,stop_on_error = False, deep_error = True)

            #if k==0 or k ==4 or k == 5 or k == 6 or k == 7:
            from neuronunit.capabilities import spike_functions
            import quantities as pq
            dt = model.results['t'][1] - model.results['t'][0]
            dt = dt*pq.s
            from neo import AnalogSignal
            vm = AnalogSignal(model.results['vm'],units=pq.V,sampling_rate=1.0/dt)
            #import pdb; pdb.set_trace()
            print(spike_functions.get_spike_waveforms(vm))
            print(spike_functions.get_spike_train(vm))
            print(model.get_spike_count())

            snippets = spike_functions.get_spike_waveforms(vm)#['vm'])
            #plt.plot(model.results['t'],snippets,label=str(v)+str(score), color=color, linewidth=1)
        #else:
            plt.plot(model.results['t'],model.results['vm'],label=str(v)+str(score), color=color, linewidth=1)

            plt.xlim(0,float(v.params['injected_square_current']['duration']) )
            stored_min.append(np.min(model.results['vm']))
            stored_max.append(np.max(model.results['vm']))
            plt.ylim(np.min(stored_min),np.max(stored_max))
            plt.tight_layout()
            model.results = None
            plt.ylabel('$V_{m}$ mV')
            plt.xlabel('mS')
        plt.savefig(str('test_')+str(v)+'vm_versus_t.eps', format='eps', dpi=1200)



def surfaces(history,td):

    all_inds = history.genealogy_history.values()
    sums = numpy.array([np.sum(ind.fitness.values) for ind in all_inds])
    keep = set()
    quads = []
    for k in range(1,9):
        for i,j in enumerate(td):
            print(i,k)
            if i+k < 10:
                quads.append((td[i],td[i+k],i,i+k))

    for q in quads:
        print(k)
        (x,y,w,z) = q
        print(x,y,w,z,i)
        xs = numpy.array([ind[w] for ind in all_inds])
        ys = numpy.array([ind[z] for ind in all_inds])
        min_ys = ys[numpy.where(sums == numpy.min(sums))]
        min_xs = xs[numpy.where(sums == numpy.min(sums))]
        plt.clf()
        fig_trip, ax_trip = plt.subplots(1, figsize=(10, 5), facecolor='white')
        trip_axis = ax_trip.tripcolor(xs,ys,sums+1,20,norm=matplotlib.colors.LogNorm())
        plot_axis = ax_trip.plot(list(xs), list(ys), 'o', color='lightblue')
        fig_trip.colorbar(trip_axis, label='sum of objectives + 1')
        ax_trip.set_xlabel('Parameter '+ str(td[w]))
        ax_trip.set_ylabel('Parameter '+ str(td[z]))
        plot_axis = ax_trip.plot(list(min_xs), list(min_ys), 'o', color='lightblue')
        fig_trip.tight_layout()
        fig_trip.savefig('surface'+str(td[w])+str(td[z])+'.eps')

def just_mean(log):
    '''
    https://github.com/BlueBrain/BluePyOpt/blob/master/examples/graupnerbrunelstdp/run_fit.py
    Input: DEAP Plot logbook

    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import matplotlib.pyplot as plt
    import numpy as np
    plt.clf()
    plt.style.use('ggplot')
    fig, axes = plt.subplots(figsize=(10, 10), facecolor='white')
    gen_numbers = log.select('gen')
    mean_many = np.array(log.select('avg'))
    axes.plot(
        gen_numbers,
        mean_many,
        color='black',
        linewidth=2,
        label='population average')
    axes.set_xlim(min(gen_numbers) - 1, max(gen_numbers) + 1)
    axes.set_xlabel('Generation #')
    axes.set_ylabel('Sum of objectives')
    axes.set_ylim([0, max(mean_many)])
    axes.legend()
    fig.tight_layout()
    fig.savefig('Izhikevich_evolution_just_mean.eps', format='eps', dpi=1200)

def plot_db(vms,name=None):
    '''
    A method to plot raw predictions
    versus observations

    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import os
    import matplotlib
    import pandas as pd

    import matplotlib.pyplot as plt
    import numpy as np
    plt.clf()
    matplotlib.use('Agg') # Need to do this before importing neuronunit on a Mac, because OSX backend won't work
    matplotlib.style.use('ggplot')
    #f, axarr = plt.subplots(2, sharex=True)
    fig, axarr = plt.subplots(5, sharex=True, figsize=(10, 10), facecolor='white')

    from neuronunit.models import backends
    from neuronunit.models.reduced import ReducedModel
    import quantities as pq
    import numpy as np
    import get_neab
    from itertools import repeat
    import copy
    from itertools import repeat
    #import net_graph
    #vmslist = [vms_best, vms_worst]
    delta = []
    scores = []
    tests = copy.copy(get_neab.tests)
    for k,v in enumerate(tests):
        new_file_path = str(get_neab.LEMS_MODEL_PATH)+str(os.getpid())
        model = ReducedModel(new_file_path,name=str('vanilla'),backend='NEURON')
        #model.load_model()
        assert type(vms.rheobase) is not type(None)
        #tests = get_neab.suite.tests
        #model.update_run_params(vms.attrs)

        if k == 0:
            v.prediction = {}
            v.prediction['value'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['duration'] = 1000 * pq.ms
            v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['delay'] = 100 * pq.ms
            print(v.prediction)
        if k != 0:
            v.prediction = None

        if k == 1 or k == 2 or k == 3:
            # Negative square pulse current.
            v.params['injected_square_current']['duration'] = 100 * pq.ms
            v.params['injected_square_current']['amplitude'] = -10 *pq.pA
            v.params['injected_square_current']['delay'] = 30 * pq.ms
        if k == 5 or k == 6 or k == 7:
            # Threshold current.
            v.params['injected_square_current']['duration'] = 1000 * pq.ms
            v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['delay'] = 100 * pq.ms
        import neuron
        model.reset_h(neuron)
        model.load_model()
        model.update_run_params(vms.attrs)
        print(v.params)
        score = v.judge(model,stop_on_error = False, deep_error = True)
        scores.append(score)


        if 'mean' in v.observation.keys():
            unit_observations = v.observation['mean']

        if 'value' in v.observation.keys():
            unit_observations = v.observation['value']

        if 'mean' in v.prediction.keys():
            unit_predictions = v.prediction['mean']

        if 'value' in v.prediction.keys():
            unit_predictions = v.prediction['value']

        print('observations: {0} predictions: {1}'.format(unit_observations, unit_predictions))

        #if unit_observations.units == unit_predictions.units:
        try:
            to_r_s = unit_observations.units
            unit_predictions = unit_predictions.rescale(to_r_s)
            unit_delta = np.abs(np.abs(unit_observations)-np.abs(unit_predictions))
        except:
            unit_delta = 0.0
        delta.append(unit_delta)
        print('observation {0} versus prediction {1}'.format(unit_observations,unit_predictions))
        print('unit delta', unit_delta)
        sv = score.sort_key


        if k == 0:
            axarr[3].scatter(k, sv,  c='black', label = 'the score')
            axarr[4].scatter(k,0.0,  c='w',label ='the score')

            axarr[k].scatter(k,float(unit_delta),label = 'difference')
            axarr[k].scatter(k,float(unit_observations),label = 'observation')
            axarr[k].scatter(k,float(unit_predictions),label = 'prediction')

            #axarr[k].legend()
        elif k ==1:
            axarr[3].scatter(k, sv,  c='black', label = 'the score')
            axarr[4].scatter(k,0.0,  c='w',label ='the score')

            axarr[k].scatter(k,float(unit_delta),label = 'difference')
            axarr[k].scatter(k,float(unit_observations),label = 'observation')
            axarr[k].scatter(k,float(unit_predictions),label = 'prediction')
            #axarr[k].legend()

        else:
            axarr[4].scatter(k, float(sv),  c='black', label = 'the score')

            axarr[2].scatter(k,float(unit_delta),label = 'difference')
            axarr[2].scatter(k,float(unit_observations),label = 'observation')
            axarr[2].scatter(k,float(unit_predictions),label = 'prediction')



    vms.delta.append(np.mean(delta))

    labels = [ '{0}_{1}'.format(str(t),str(t.observation['value'].units)) for t in tests if 'mean' not in t.observation.keys() ]
    labels.extend([ '{0}_{1}'.format(str(t),str(t.observation['mean'].units))  for t in tests if 'mean' in t.observation.keys() ])
    labels = tuple(labels)
    plt.xlabel('test type')
    plt.ylabel('observation versus prediction')
    tick_locations = tuple(range(0,len(tests)))
    plt.xticks(tick_locations , labels)
    plt.xticks(rotation=25)
    plt.tight_layout()

    plt.savefig('obsevation_versus_prediction_{0}.eps'.format(name), format='eps', dpi=1200)
    #import pandas as pd
    #pd.DataFrame(scores).plot(kind='bar', stacked=True)
    #df2.plot(kind='bar', stacked=True);

    return vms

def prep_bar_chart(vms,name=None):

    import plotly.plotly as py
    from plotly.graph_objs import Bar
    '''
    A method to plot raw predictions
    versus observations

    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import os
    import matplotlib
    import pandas as pd

    #import matplotlib.pyplot as plt
    import numpy as np

    from neuronunit.models import backends
    from neuronunit.models.reduced import ReducedModel
    import quantities as pq
    import numpy as np
    import get_neab
    from itertools import repeat
    import copy
    from itertools import repeat
    os.system('conda install pandas')
    os.system('conda install cufflinks')
    import cufflinks as cf
    import pandas as pd
    traces = []

    delta = []
    scores = []
    tests = copy.copy(get_neab.tests)
    labels = [ '{0}_{1}'.format(str(t),str(t.observation['value'].units)) for t in tests if 'mean' not in t.observation.keys() ]
    labels.extend([ '{0}_{1}'.format(str(t),str(t.observation['mean'].units))  for t in tests if 'mean' in t.observation.keys() ])
    test_dic = {}
    for k,v in enumerate(tests):

        new_file_path = str(get_neab.LEMS_MODEL_PATH)+str(os.getpid())
        model = ReducedModel(get_neab.LEMS_MODEL_PATH,name=str('vanilla'),backend='NEURON')
        #model.load_model()
        assert type(vms.rheobase) is not type(None)
        #tests = get_neab.suite.tests
        #model.update_run_params(vms.attrs)

        if k == 0:
            v.prediction = {}
            v.prediction['value'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['duration'] = 1000 * pq.ms
            v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['delay'] = 100 * pq.ms
            print(v.prediction)
        if k != 0:
            v.prediction = None

        if k == 1 or k == 2 or k == 3:
            # Negative square pulse current.
            v.params['injected_square_current']['duration'] = 100 * pq.ms
            v.params['injected_square_current']['amplitude'] = -10 *pq.pA
            v.params['injected_square_current']['delay'] = 30 * pq.ms
        if k == 5 or k == 6 or k == 7:
            # Threshold current.
            v.params['injected_square_current']['duration'] = 1000 * pq.ms
            v.params['injected_square_current']['amplitude'] = vms.rheobase * pq.pA
            v.params['injected_square_current']['delay'] = 100 * pq.ms
        import neuron
        model.reset_h(neuron)
        model.load_model()
        model.update_run_params(vms.attrs)
        print(v.params)
        score = v.judge(model,stop_on_error = False, deep_error = True)
        scores.append(score)


        if 'mean' in v.observation.keys():
            unit_observations = v.observation['mean']

        if 'value' in v.observation.keys():
            unit_observations = v.observation['value']

        if 'mean' in v.prediction.keys():
            unit_predictions = v.prediction['mean']

        if 'value' in v.prediction.keys():
            unit_predictions = v.prediction['value']

        print('observations: {0} predictions: {1}'.format(unit_observations, unit_predictions))

        #if unit_observations.units == unit_predictions.units:
        try:
            to_r_s = unit_observations.units
            unit_predictions = unit_predictions.rescale(to_r_s)
            unit_delta = np.abs(np.abs(unit_observations)-np.abs(unit_predictions))
        except:
            unit_delta = 0.0
        delta.append(unit_delta)
        print('observation {0} versus prediction {1}'.format(unit_observations,unit_predictions))
        print('unit delta', unit_delta)
        sv = score.sort_key
        test_dic[str(v)] = (float(unit_observations), float(unit_predictions), unit_delta)
        #py.iplot(fig)

        #df = cf.datagen.lines()
    columns1 = []
    threed = []
    for k,v in test_dic.items():
        columns1.append(str(k))
        threed.append((float(v[0]),float(v[1]),float(v[2])))

    trans = np.transpose(np.array(threed))
    stacked = np.column_stack(trans)
    with open('for_pandas.p','wb') as handle:
        pickle.dump([stacked,columns1],handle)
    df = pd.DataFrame(stacked, columns=columns1)
    py.sign_in('RussellJarvis','FoyVbw7Ry3u4N2kCY4LE')

    df.iplot(kind='bar', filename='grouped-bar-chart',image='svg')

    #py.iplot(fig, filename='improved_names.svg',image='svg')
    '''
    traces.append(Bar(x=float(unit_observations),
                      y=float(unit_predictions),
                      name=labels[k],
                      marker=dict(color='#ffcdd2')))

    data = traces#[trace_rheobase, trace_test1, trace_test2]
    layout = Layout(title="Experimental Observations, Versus Model Predictions",
                    xaxis=dict(title='Test Type'),
                    yaxis=dict(title='Agreement'))
    fig = Figure(data=data, layout=layout)
    py.iplot(fig, filename='obs_pred_tests.svg')
    '''
    return test_dic


def plot_log(log):
    '''
    https://github.com/BlueBrain/BluePyOpt/blob/master/examples/graupnerbrunelstdp/run_fit.py
    Input: DEAP Plot logbook
    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import matplotlib.pyplot as plt
    import numpy as np
    plt.clf()
    plt.style.use('ggplot')


    fig, axes = plt.subplots(figsize=(10, 10), facecolor='white')

    gen_numbers = log.select('gen')
    mean = np.array(log.select('avg'))
    std = np.array(log.select('std'))
    minimum = log.select('min')
    # maximum = log.select('max')
    import get_neab
    objective_labels = [ str(t) for t in get_neab.tests ]

    stdminus = mean - std
    stdplus = mean + std
    axes.plot(
        gen_numbers,
        mean,
        color='black',
        linewidth=2,
        label='population average')

    axes.fill_between(
        gen_numbers,
        stdminus,
        stdplus,
        color='lightgray',
        linewidth=2,
        label='population standard deviation')

    axes.plot(
        gen_numbers,
        minimum,
        linewidth=2,
        label='population objectives')
        # want objective labels to be label.
        # problem is vector scalar mismatch.



    axes.set_xlim(min(gen_numbers) - 1, max(gen_numbers) + 1)
    axes.set_xlabel('Generation #')
    axes.set_ylabel('Sum of objectives')
    axes.set_ylim([0, max(stdplus)])
    axes.legend()

    fig.tight_layout()
    fig.savefig('Izhikevich_history_evolution.eps', format='eps', dpi=1200)


def plot_objectives_history(log):
    '''
    https://github.com/BlueBrain/BluePyOpt/blob/master/examples/graupnerbrunelstdp/run_fit.py
    Input: DEAP Plot logbook
    Outputs: This method only has side effects, not datatype outputs from the method.

    The most important side effect being a plot in eps format.

    '''
    import matplotlib.pyplot as plt
    import numpy as np
    plt.clf()
    plt.style.use('ggplot')


    fig, axes = plt.subplots(figsize=(10, 10), facecolor='white')

    gen_numbers = log.select('gen')
    minimum = log.select('min')
    import get_neab
    objective_labels = [ str(t) for t in get_neab.tests ]
    mins_components_plot = log.select('min')
    components = {}
    for i in range(0,7):
        components[i] = []
        for l in mins_components_plot:
            components[i].append(l[i])
    maximum = 0.0
    for keys in components:

        axes.semilogy(
            gen_numbers,
            components[keys],
            linewidth=2,
            label=str(objective_labels[keys])
            )
        if np.max(components[keys]) > maximum:
            maximum = np.max(components[keys])

    axes.set_xlim(min(gen_numbers) - 1, max(gen_numbers) + 1)
    axes.set_xlabel('Generation #')
    axes.set_ylabel('Sum of objectives')
    #axes.set_ylim([0, max(maximum[0])])
    axes.legend()

    fig.tight_layout()
    fig.savefig('Izhikevich_evolution_components.eps', format='eps', dpi=1200)
