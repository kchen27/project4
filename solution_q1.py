from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the structure of the Bayesian network
model = BayesianModel([('Burglary', 'Alarm'), 
                       ('Earthquake', 'Alarm'), 
                       ('Alarm', 'JohnCalls'), 
                       ('Alarm', 'MaryCalls')])

# Define the Conditional Probability Distributions (CPDs)
cpd_b = TabularCPD(variable='Burglary', variable_card=2, values=[[0.001], [0.999]])
cpd_e = TabularCPD(variable='Earthquake', variable_card=2, values=[[0.002], [0.998]])
cpd_a = TabularCPD(variable='Alarm', variable_card=2, 
                   values=[[0.95, 0.94, 0.29, 0.001], 
                           [0.05, 0.06, 0.71, 0.999]], 
                   evidence=['Burglary', 'Earthquake'], 
                   evidence_card=[2, 2])
cpd_j = TabularCPD(variable='JohnCalls', variable_card=2, 
                   values=[[0.9, 0.05], 
                           [0.1, 0.95]], 
                   evidence=['Alarm'], 
                   evidence_card=[2])
cpd_m = TabularCPD(variable='MaryCalls', variable_card=2, 
                   values=[[0.7, 0.01], 
                           [0.3, 0.99]], 
                   evidence=['Alarm'], 
                   evidence_card=[2])

# Add CPDs to the model
model.add_cpds(cpd_b, cpd_e, cpd_a, cpd_j, cpd_m)

# Verify the model
assert model.check_model()

# Perform variable elimination inference
inference = VariableElimination(model)

# Calculate the probability distribution for Burglary given that JohnCalls is true (+j)
result = inference.query(variables=['Burglary'], evidence={'JohnCalls': 0})

# Display the resulting probability distribution
result_table = result.values
result_table
