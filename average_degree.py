import re
import json
import networkx as nx
import itertools
from datetime import datetime,timedelta
import TweetGraph
import TruncateNum




# Define variables
tmax = datetime.strptime('Thu Mar 24 17:51:10 +0000 1900','%a %b %d %H:%M:%S +0000 %Y')
tnew = datetime.strptime('Thu Mar 24 17:51:10 +0000 1900','%a %b %d %H:%M:%S +0000 %Y')
tmin = datetime.strptime('Thu Mar 24 17:51:10 +0000 1900','%a %b %d %H:%M:%S +0000 %Y')
output_result=[]


# Input and output file path
tweets_filename = '.\\tweet_input\\tweets.txt'
output_filename = '.\\tweet_output\\output.txt'


# Data clean: open input file and remove rate_limit rows
try:
    tweets_file = open(tweets_filename, "r+")
    d = tweets_file.readlines()
    tweets_file.seek(0)
    # Remove rate-limit message from input file
    for i in d:
        if '''{"limit":{"track":''' not in i:
            tweets_file.write(i)
    tweets_file.truncate()
    tweets_file.close()
# Throw an error if the input file can not be opened. And then exit.
except IOError:
    print('File cannot be opened:',tweets_filename)
    exit()

# Create a graph object G
G = nx.Graph()

# Calculate average_degree of a vertex in a Twitter hashtag graph over a 60-second sliding window
if __name__ == '__main__':
    try:
        tweets_file = open(tweets_filename, "r+")
        try:
            # Loop through input file

            for line in tweets_file:
               # Read in one line of the file, convert it into a json object
               tweet = json.loads(line.strip())
               # Only messages contains 'text' field is a tweet
               if 'text' in tweet:
                   #Get created_at and hastags information from input file
                    created_at = tweet['created_at']
                    hashtags = []
                    for hashtag in tweet['entities']['hashtags']:
                        hashtags.append(hashtag['text'])

                    # Initiate tnew
                    tnew = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')

                    # First line message handling
                    if tmax == datetime.strptime('Thu Mar 24 17:51:10 +0000 1900','%a %b %d %H:%M:%S +0000 %Y'):
                       # Assign values to time variables
                       tmax = tnew
                       tmin = tmax-timedelta(minutes=1)

                       if len(hashtags)== 0:
                           output_result = '0.00 \n'
                           with open(output_filename, 'a') as f:
                               f.writelines(output_result)
                               f.close()
                    # Otherwise add notes and edges into graph object G, calculate average_degree
                       else:
                            tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at,'')
                            AveDegree = tweetgraph.TweetAveDegree()
                            turnum= TruncateNum.CTruncateNum(AveDegree)
                            output_result = turnum.ChopNum()
                            with open(output_filename, 'a') as f:
                                f.writelines(output_result)
                            f.close()
                # Input file message handling expect for the first line
                    # If new line's created_at time is earlier than 60 seconds window, this line won't be counted. The new output value is equal to the previous output value
                    elif tnew < tmin:
                       with open(output_filename, 'a') as f:
                           f.writelines(output_result)
                       f.close()
                    # If new line's created_at is within 60 seconds window
                    elif tmin <= tnew <= tmax:
                      # Check if there is any 'text' information in hashtags field
                        # If empty 'text', the new output value is equal to previous output value
                        if len(hashtags)== 0:
                            with open(output_filename, 'a') as f:
                                f.writelines(output_result)
                            f.close()
                        # Otherwise add notes and edges into graph object G, calculate G's average_degree
                        else:
                            tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at,'')
                            AveDegree = tweetgraph.TweetAveDegree()
                            turnum= TruncateNum.CTruncateNum(AveDegree)
                            output_result = turnum.ChopNum()
                            with open(output_filename, 'a') as f:
                                f.writelines(output_result)
                            f.close()
                    # If new line's created_at is later than 60 seconds' window. Update the 60 seconds window
                    elif tnew > tmax:
                        tmax = tnew
                        tmin = tmax-timedelta(minutes=1)
                        # Convert tmin to string data type
                        tmincompare = tmin.strftime('%a %b %d %H:%M:%S +0000 %Y')
                        tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at,tmincompare)
                        # Remove old edges if they are existed
                        old_edge = tweetgraph.TweetRemoveOldEdge()

                        # Calculate average_degree based on new graph
                        # If empty 'text' in hashtags field, calculate average_degree based on the modified graph
                        if len(hashtags) == 0:
                            degrees = tweetgraph.TweetGdegrees()
                            sum_of_edges = sum(degrees.values())
                            average_degree = sum_of_edges/tweetgraph.TweetGNoOfNodes()
                            turnum= TruncateNum.CTruncateNum(average_degree)
                            output_result = turnum.ChopNum()
                            with open(output_filename, 'a') as f:
                                f.writelines(output_result)
                            f.close()
                        # Else add new nodes and edges to the graph and calculate average_degree
                        else:
                            tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at,'')
                            AveDegree = tweetgraph.TweetAveDegree()
                            turnum= TruncateNum.CTruncateNum(AveDegree)
                            output_result = turnum.ChopNum()
                            with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                            f.close()
        # Close input file
        finally:
                tweets_file.close()
    except IOError:
        pass

