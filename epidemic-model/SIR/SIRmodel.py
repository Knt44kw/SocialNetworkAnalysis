from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import matplotlib.pyplot as plt

G_list =  [
          nx.barabasi_albert_graph(1000, 8, seed=0), 
          nx.newman_watts_strogatz_graph(1000, k=4, p=0.12, seed=0), 
          nx.fast_gnp_random_graph(n=1000, p=0.20)
          ]

model_list = []
iteration_list = []
trend_list = []

for graph in G_list:         
    model = ep.SIRModel(graph)
    model_list.append(model)
    config = mc.Configuration()
    config.add_model_parameter('beta', 0.1)
    config.add_model_parameter('gamma', 0.1)
    config.add_model_parameter('fraction_infected', 0.01)
    model.set_initial_status(config)
    

for i in range(3):
    iterations = model_list[i].iteration_bunch(100)
    iteration_list.append(iterations)
    trends = model.build_trends(iterations)
    trend_list.append(trends)

    
visual = DiffusionTrendComparison([model_list[0], model_list[1], model_list[2]], [trend_list[0], trend_list[1], trend_list[2]], statuses=["Susceptible", "Infected", "Removed"])
plt.title(" BA vs SW vs Random")
result = visual.plot()

