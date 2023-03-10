# required packages
from pref_voting.profiles import Profile
from pref_voting.generate_profiles import generate_profile, create_rankings_mallows 
from pref_voting.generate_profiles import prob_models
from pref_voting.margin_based_methods import split_cycle, beat_path_faster, beat_path 
from pref_voting.weighted_majority_graphs import MarginGraph
from pref_voting.other_methods import bucklin
from pref_voting.iterative_methods import coombs, plurality_with_runoff
from ownmethods import coombs_with_uniform_truncation, bucklin_with_uniform_truncation, plurality_with_runoff_profile_with_ties, truncate_profile
import csv

import matplotlib.pyplot as plt

# Writes the data to a csv file for later analysis
data_file = open("data.csv", "w")
data_writer = csv.writer(data_file)

# Variables for the simulation
times_per_permutation = 1000
candidates = [4,5,6,7]
voters = [100,200,300,400,500,600, 2000]
dispersion_values = [0.7,0.8,0.9,1]



# Nested for loops run through the various permutations of the test
for candidate_value in candidates:
    for voter_value in voters:
        for dispersion_value in dispersion_values:
            
            # The success at each length with index 0 correlating to length 1 and so on
            success_at_length_beat_path = [0,0,0,0,0,0,0,0]
            success_at_length_bucklin = [0,0,0,0,0,0,0,0]
            success_at_length_plurality_with_runoff = [0,0,0,0,0,0,0,0]
            success_at_length_coombs = [0,0,0,0,0,0,0,0]

            # Runs each permuation of variables a set amount of times
            for i in range(times_per_permutation):

                # Creates Rankings
                prof = create_rankings_mallows(candidate_value, voter_value, dispersion_value)

                # Puts the ranking into a usable form
                prof = Profile(prof[0], prof[1])

                #Records the true winners under each voting system
                true_beat_path = beat_path_faster(prof)
                true_bucklin = bucklin(prof)
                true_plurality_with_runoff = plurality_with_runoff(prof)
                true_coombs = coombs(prof)


                # Runs through the different truncation levels for each profile
                for ballot_length in range(1,candidate_value + 1):
                    new_prof = truncate_profile(prof, ballot_length)
                    new_prof.use_extended_strict_preference()

                    # Keeps track of each voting system's winners at the level of truncation
                    winners_beat_path = beat_path_faster(new_prof)
                    winners_bucklin = bucklin_with_uniform_truncation(new_prof, ballot_length)
                    winners_plurality_with_runoff = plurality_with_runoff_profile_with_ties(new_prof)
                    winners_coombs = coombs_with_uniform_truncation(new_prof)


                    # Checks if the truncated profile had the same winner under each voting system as its true winner
                    if winners_beat_path == true_beat_path:
                        success_at_length_beat_path[ballot_length - 1] += 1
                    
                    if winners_bucklin == true_bucklin:
                        success_at_length_bucklin[ballot_length - 1] += 1
                    
                    if winners_plurality_with_runoff == true_plurality_with_runoff:
                        success_at_length_plurality_with_runoff[ballot_length - 1] += 1
                    
                    if winners_coombs == true_coombs:
                        success_at_length_coombs[ballot_length - 1] += 1

            # Changes each value in the success list to be a probability
            for j in range(candidate_value):
                if not success_at_length_beat_path[j] == 0:
                    success_at_length_beat_path[j] /= times_per_permutation
                if not success_at_length_bucklin[j] == 0:
                    success_at_length_bucklin[j] /= times_per_permutation
                if not success_at_length_plurality_with_runoff[j] == 0:
                    success_at_length_plurality_with_runoff[j] /= times_per_permutation
                if not success_at_length_coombs[j] == 0:
                    success_at_length_coombs[j] /= times_per_permutation
            

            
            # Creates graph for permutation
            xbeatpath = []
            ybeatpath = []

            xbucklin = []
            ybucklin = []

            xpluralitywrunoff = []
            ypluralitywrunoff = []

            xcoombs = []
            ycoombs = []

            for ballot_length in range(1, candidate_value+1):
                xbeatpath.append(ballot_length)
                ybeatpath.append(success_at_length_beat_path[ballot_length - 1])

                xbucklin.append(ballot_length)
                ybucklin.append(success_at_length_bucklin[ballot_length - 1])

                xpluralitywrunoff.append(ballot_length)
                ypluralitywrunoff.append(success_at_length_plurality_with_runoff[ballot_length - 1])

                xcoombs.append(ballot_length)
                ycoombs.append(success_at_length_coombs[ballot_length - 1])
            
            plt.plot(xbeatpath,ybeatpath, label = "Schulze", marker = '.')
            plt.plot(xbucklin, ybucklin, label = "Bucklin", marker = '.')
            plt.plot(xpluralitywrunoff, ypluralitywrunoff, label = "Plurality With Runoff", marker = '.')
            plt.plot(xcoombs, ycoombs, label = "Coombs", marker = '.')
            plt.xlabel = "Ballot Length"
            plt.ylabel = "Probability that true winners are chosen"
            plt.title(f"Candidates: {candidate_value}, Voters: {voter_value}, Dispersion Value: {dispersion_value}")
            plt.legend()
            plt.yticks([0,0.2,0.4,0.6,0.8,1.0])
            plt.xticks([x for x in range(1, ballot_length + 1)])

            # Saves the graph of the permuation of variables
            plt.savefig(f"graphs/{candidate_value}cands-{voter_value}voters-{dispersion_value}dispersion.png", dpi=600)
            plt.clf()
            
            # Records the data into the csv
            data_writer.writerow([candidate_value, voter_value, dispersion_value, "Schulze", success_at_length_beat_path[0], success_at_length_beat_path[1],success_at_length_beat_path[2],success_at_length_beat_path[3],success_at_length_beat_path[4],success_at_length_beat_path[5],success_at_length_beat_path[6]])
            data_writer.writerow([candidate_value, voter_value, dispersion_value, "Bucklin", success_at_length_bucklin[0], success_at_length_bucklin[1],success_at_length_bucklin[2],success_at_length_bucklin[3],success_at_length_bucklin[4],success_at_length_bucklin[5],success_at_length_bucklin[6]])
            data_writer.writerow([candidate_value, voter_value, dispersion_value, "Plurality With Runoff", success_at_length_plurality_with_runoff[0], success_at_length_plurality_with_runoff[1],success_at_length_plurality_with_runoff[2],success_at_length_plurality_with_runoff[3],success_at_length_plurality_with_runoff[4],success_at_length_plurality_with_runoff[5],success_at_length_plurality_with_runoff[6]])
            data_writer.writerow([candidate_value, voter_value, dispersion_value, "Coombs", success_at_length_coombs[0], success_at_length_coombs[1],success_at_length_coombs[2],success_at_length_coombs[3],success_at_length_coombs[4],success_at_length_coombs[5],success_at_length_coombs[6]])
            




