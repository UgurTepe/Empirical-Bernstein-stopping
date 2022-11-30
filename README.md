# Empirical-Bernstein-stopping

Create new Bernstein object: ebs = Bernstein_simple()

Add Samples ebs.add_sample(sample) in a loop 

Let loop run while ebs.cond_check() == True
 
Stopping time via ebs.current_step

Estimate via ebs.get_estimate()

