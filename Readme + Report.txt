README (report on bottom of document)
---------------------------------------------------------------------------------------------------------------------------------

clustering.py
is a clustering program. There are a total of 5 clustering methods that work in 1-dimension for this program
These methods are as follows:
	1) single linkage
	2) complete linkage
	3) average linkage
	4) k-means
	5) ward's variance minimizing clustering 

Upon running the program, it:
			asks the user for the file name
			reads the file and asks the user which attribute to cluster
			gives user option of showing histogram of attribute
			asks user which method to use to cluster and for number of clusters
			prints clusters by index
			gives option for showing histogram of clustered data
	



Clustering Methods:

singleLinkage Clustering:
	Summary: clusters data accoding to the single linkage algorithm. Distance is measured as nearest points between groups
	input: data, k
		data is a pandas series, this data will be clustered
		k is the number of clusters
	output: groups
		groups is a list of index values, these can be used to access the data in a pandas dataframe
		
		
completeLinkage Clustering: (not yet implemented)
	Summary: clusters data according to the complete linkage algorithm. Distance is measured as farthest two data points within groups
	input: data, k
		data is a pandas series, this data will be clustered
		k is the number of clusters
	output: groups
		groups is a list of index values, these can be used to access the data in a pandas dataframe
		
		
averageLinkage Clustering:
	Summary: clusters data according to the average linkage algorithm. Distance is measured between the averages of two groups
	input: data, k
		data is a pandas series, this data will be clustered
		k is the number of clusters
	output: groups
		groups is a list of index values, these can be used to access the data in a pandas dataframe
		
		
kMeans Clustering:
	Summary: iterates through the k-means algorithm until no data changes. Uses euclidian distance to group data according
		to nearest centroid, then updates centroids to mean of group. 
	input: data, k
		data is a pandas series, this data will be clustered
		k is the number of clusters
	output: groups
		groups is a list of index values, these can be used to access the data in a pandas dataframe
		

wardMethod Clustering:
	Summary: clusters data according to Ward's minimum variance clustering algorithm until the desired number of clusters (k) is met
	input: data, k
		data is a pandas series, this data will be clustered
		k is the number of clusters
	output: groups
		groups is a list of index values, these can be used to access the data in a pandas dataframe
		
		
		
		
Helper Functions:

makeDistanceMatrix:
	Summary: Creates a lower triangular matrix of distances
	input: data
		data is a pandas series. The distance matrix is calculated according to the distances between each data point in data
	output: distanceTriangle
		A lower triangular matrix of distances
		
updateMatrix
	Summary: Updates a distance matrix after joining two groups. I added functionality to work for both single and complete linkage
		depending on if you pass in 's' or 'c'.
	input distances, i, j, typee
		distances is a lower triangular distance matrix that needs to be updated
		i and j are indices of the two groups to be joined, i must be greater than or equal to j or errors will occur
		typee is a char that determines whether the method will update the matrix based on Complete or Single linkage clustering
		algorithm.
	output: distances
		distances is returned after joining the two groups
		
updateGroups
	Summary: A list of groups is kept, this function updates this list
	input: groups, i, j
		groups is a list of lists, the inner lists are index names. Each inner list is a group
	output: groups
		after updating groups, it is returned

calcVars
	Summary: combines two clusters (i and j) and returns the sum of the variances squared of each element in this new cluster. Used for 
		Ward's method
	input: groups, i, j
		groups is a list of lists, the inner lists are index names. Each inner list is a group
		i is the index of the first cluster you want to combine
		j is the index of the second cluster you are combining.
	output: tot
		tot is the sum of squaring the difference of each element subtracted from the average of the new combined group.
		


REPORT
-----------------------------------------------------------------------------------------------------------------------------------------------------
Overall, I was able to successfully attempt and complete designing the four clustering methods from the template as well as an additional 
clustering method. The five methods I tested were single linkage, complete linkage, average, k-means, and ward's variance minimizing method.
To prevent repetitiveness, I also altered the default 'updateMatrix' helper function to allow updating matrices for both 'single' and 'complete' 
linkage. Additionally, I ran all five clustering methods against the test data from the assignment and confirmed that they all worked on that specific
data.

A slight problem I ran into was with the k-means method returning an inconsistent amount of clusters (i.e the num of clusters in 'groups' != k). 
I pinpointed two causes for this problem: (1) sometimes the randomly generated guesses would be too far off and not lead to any clusters developing, 
and (2) my break condition for the while loop only relied on the previous groups == the current groups and didn't take into consideration the desired 
number of clusters. To fix problem (1), I selected my random 'guesses' only from actual data elements to ensure that no cluster would remain empty
(at the very least, each cluster would have its 'guess' in it). To fix problem (2): I added the condition, k == len(group)-group.count([]) to my if 
statement that controls whether the program breaks or not. This meant the K-means wouldn't stop iterating until I had the desired number of clusters
Since I also relied on 'len(groups)' a couple times, I had to ensure to check the condition that 'len(groups)>0' to prevent any division by zero errors.

A final issue I found was one that involved user input. If the user inputted (k) too large, then there were bound be some empty clusters. For example, if 
everything was the same number, then there would only be one cluster regardless of what (k) the user inputs.

I split many small tasks in my clustering algorithms into smaller helper functions or lambda functions. Examples include the 'calcVars' helper function
and the 'calcAvgs' lambda function. This seperation helped me focus on one part of the problem at a time and ensure that I didn't accidently mess up 
working code.

To ensure my functions work, I tried to check every possible combination of a clustering step (combining two new clusters) for the single, complete, k-means,
and ward's methods. I did this by utilizing nested for loops and also a 'minimum' variable, which I would use to find the minimum value in the entire distance 
matrix. Since, brute forcing every possibility is relatively slow, I tried to optimize it in ward's method by starting the nested for loop at 'i+1' rather than
at 0. This made it so I didn't have to check duplicates ('i' combined with 'j' is the same as 'j' combined with 'i'). For the average linkage clustering method,
I was able to sort the data, making it so I didn't need to rely on checking every possibility.

As a result of the methods mentioned in the above paragraph, I found that the single, complete, and average clustering functions were faster in practice
than the ward's and k-means methods (even after the slight optimizations). However, these differences were slight and the program was still completely
usable. Ward's and k-means were likely slower than the reset because they involved looping through 'len(groups)' again to calculate the average of a group
(for k-means) and the sum of variance of a group (for ward's)

