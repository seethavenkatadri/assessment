#  Given the names of students along with their physics, math and chemistry scores, store them in a nested list and print the names of students who are the bottom two in each subject.
# Note: If there are multiple students with the same grade, order their names alphabetically and print each name on the same line.
# For example,
# Input:
# John, 100, 80, 70
# Alice,  80, 90, 96
# Steve, 89, 95, 98
# Jane, 80, 88, 98
# Harry, 90, 100, 99
# Output:
# Physics:
#   Steve
#       Alice, Jane
# Math:
#   Jane
#   John
# Chemistry:
#   Alice
#   John
import pandas as pd


def get_names_of_rank(subject, rank):
    """Function get names of students who got a specific rank (from bottom) in a subject"""
    ind=subject+'_Rank'
    sorted_names=sorted(students_df['Name'][results_df[ind] == rank])
    return ', '.join(sorted_names)


if __name__ == "__main__":
    ### Input
    students = [['Name','Physics','Math','Chemistry'],['John', 100, 80, 70],['Alice',  80, 90, 96],['Steve', 89, 95, 98],['Jane', 80, 88, 98],['Harry', 90, 100, 99]]
    fetch = 2


    ## Ranking Logic
    students_df = pd.DataFrame(students[1:],columns=students[0])

    ## axis=0 for row-wise ranking
    ## method='dense' for increasing rank by 1 for each score value
    ## ascending=True - so the bottom-most will have rank 1 and last-but-one will be rank 2
    ## numeric_only=True to apply rank only on the score columns
    ranks_df=students_df.rank(axis=0,method='dense',numeric_only=True,ascending=True)

    ## adds the rank columns to the main df to make indexing easier
    ranks_df.columns=['Physics_Rank','Math_Rank','Chemistry_Rank']
    results_df = students_df.join(ranks_df)


    ## Print Logic
    for sub in students[0][1:]:
        print(sub + ':')
        currRank=fetch
        while(currRank>0):
            print('\t',get_names_of_rank(subject=sub,rank=currRank))
            currRank-=1


